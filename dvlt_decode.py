import sys, os, re, pickle, struct
from datetime import datetime
from io import BytesIO
from pprint import pprint

from protobuf_to_dict import protobuf_to_dict

from dvlt_messages import interpret_as, heuristic_search, raw_decode
from dvlt_services import find_method, process_rpc

import RPCMessages_pb2

class DevialetSection:
    def __init__(self, raw_section, time=None):
        self.warnings = []
        self.raw_protobufs = []
        self.raw_fields = raw_section
        self.time = time

        try:
            self.magic = raw_section[0]['firstbyte']
            # Delimiter, always empty
            if len(raw_section[0]['data']) != 0:
                self.warnings.append('Field 0 of length {} instead of 0'.format(
                    len(raw_section[0]['data'])))

            i = 1
            # Extra field (+ delimiter) that doesnt decode into protobuf, some kind of uid?
            if self.magic == 0xC3:
                self.uid = raw_section[i]['data']
                i += 2
            else:
                self.uid = b''

            # Remaining fields should all be protobufs
            for raw_field in raw_section[i:]:
                self.raw_protobufs.append(raw_field['data'])
                if raw_field['firstbyte'] != self.magic:
                    self.warnings.append('Magic mismatch {} != {}'.format(
                        raw_field['firstbyte'], self.magic))
            if self.warnings:
                print(self.warnings)
        except Exception as e:
            print("Error in Section decode: {} {}".format(type(e), e))
            pass

class DevialetFlow:
    def __init__(self, name='', phantom_port=0, spark_port=0, start_time=datetime.now()):
        self.name = name
        self.phantom_port = phantom_port
        self.spark_port = spark_port
        self.start_time = start_time

        self.incoming_buf = BytesIO()
        self.outgoing_buf = BytesIO()
        self.incoming_sections = []
        self.outgoing_sections = []
        self.magics = [0xC2, 0xC3]
        self.warnings = []

    # def read_interleaved

    def read_one_section(self, buf, dest, time=None):
        pos = buf.tell()
        raw_section = []
        firstbyte = self.magics[0]
        same_section = 1
        try:
            while firstbyte in self.magics and same_section == 1:
                # when second byte of section header is 0, next field is part of new section
                field_header = buf.read(6)
                firstbyte, same_section, field_length = struct.unpack('>BBL', field_header)
                field = {
                    'firstbyte': firstbyte,
                    'data': buf.read(field_length),
                }
                if len(field['data']) != field_length:
                    raise struct.error
                raw_section.append(field)

        except struct.error as e:
            buf.seek(pos)
            return False

        # print('.')
        dest.append(DevialetSection(raw_section, time=(time if time else self.start_time)))
        return True


    def decode(self, raw=b'', incoming=True, time=None):
        if incoming:
            buf = self.incoming_buf
            dest = self.incoming_sections
        else:
            buf = self.outgoing_buf
            dest = self.outgoing_sections
        pos = buf.tell()
        buf.write(raw)
        buf.seek(pos)
        # print('Decoding {}'.format(self.name))
        while self.read_one_section(buf, dest, time=time):
            pass

    def close(self):
        # Check no remaining bytes in bufs, seek, truncate

        rest_incoming = self.incoming_buf.read()
        rest_outgoing = self.outgoing_buf.read()

        if rest_incoming:
            self.warnings.append('Found garbage at end of incoming flow: {}'.format(
                ' '.join('{:02x}'.format(x) for x in rest_incoming)))

        if rest_outgoing:
            self.warnings.append('Found garbage at end of outgoing flow: {}'.format(
                ' '.join('{:02x}'.format(x) for x in rest_outgoing)))

        if self.warnings:
            print(self.warnings)

        print('flow {} has {} incoming and {} outgoing sections'.format(
            self.name, len(self.incoming_sections), len(self.outgoing_sections)))

        self.incoming_buf.close()
        self.outgoing_buf.close()

    def rpc_walk(self):
        # Each section should correspond to a RPC request/reply,
        # with 2 protobufs each time

        # The "uid" parameter in the section, when present (== when magic is C3, and only on incoming packets)
        # is apparently equal to the first member of a 4 element protobuf in the same section

        service_list = RPCMessages_pb2.ServicesList().services
        incoming_iterator = iter(self.incoming_sections)
        outgoing_iterator = iter(self.outgoing_sections)

        print("Walking {}".format(self.name))
        # this may cut out some protobufs at the end (shortest of incoming or outgoing)
        # for (incoming_section, outgoing_section) in zip(incoming_iterator, outgoing_iterator):
        for incoming_section in incoming_iterator:
            print("")
            incoming_pb = incoming_section.raw_protobufs

            if incoming_section.magic == 0xC3:
                # Event?
                evt = interpret_as(incoming_pb[0], "Devialet.CallMeMaybe.Event")

                # service_name, package, service, method = find_method(evt, service_list)
                process_rpc(evt, service_list, outgoing_pb[1], incoming_pb[1:], is_event=True)
                print("out_time:{} in_time:{} evt:{} {}/{:>10d}/{:>12d}{:31s} {} {}E".format(
                    outgoing_section.time, incoming_section.time,
                    evt.serverId[:4].hex(), evt.type, evt.subTypeId, evt.serviceId,
                    '',
                    incoming_section.uid[:4].hex(),
                    'M' if rep.isMultipart else ' ',
                    # 'u' if incoming_section.uid else ' ',
                ))

            else:
                outgoing_section = next(outgoing_iterator)
                outgoing_pb = outgoing_section.raw_protobufs
                try:
                    req = interpret_as(outgoing_pb[0], "Devialet.CallMeMaybe.Request")
                    rep = interpret_as(incoming_pb[0], "Devialet.CallMeMaybe.Reply")
                except:
                    print("Error: Looks like we are out of sync or something")

                if rep.requestId != req.requestId:
                    # print("Error: Inconstistent requestId, maybe protobufs not in lockstep. requestId/type/subTypeId/serviceId: req:{}/{}/{}/{}, rep:{}/{}/{}/{}".format(
                    #     req.requestId.hex(), req.type, req.subTypeId, req.serviceId, rep.requestId.hex(), rep.type, rep.subTypeId, rep.serviceId,
                    # ))
                    print("Dropping request {}".format(req.requestId.hex()))
                    try:
                        next(outgoing_iterator)
                    except StopIteration:
                        pass

                # TODO: handle multipart
                if rep.isMultipart:
                    print("WARNING multipart")
                    if len(incoming_pb) == 2:
                        print("Error: multipart but only 2 incoming protobufs")
                    # pprint(protobuf_to_dict(rep))
                elif len(incoming_pb) > 2:
                    print("Error: we got more incoming protobufs than we should have, not Multipart")

                if len(outgoing_pb) > 2:
                    print("Error: we got more than 2 outgoing protobufs")

                if len(outgoing_pb) < 2:
                    print("Error: we got less than 2 outgoing protobufs")

                if len(incoming_pb) < 2:
                    print("Error: we got less than 2 incoming protobufs")
                # service_name, package, service, method = find_method(rep, service_list)
                service, method, input_pb, outputs_pb = process_rpc(rep, service_list, outgoing_pb[1], incoming_pb[1:])

                print("out_time:{} in_time:{} req:{}/{}/{:>10d}/{:>12d}, rep:{}/{}/{:>10d}/{:>12d} {}{}{}".format(
                    outgoing_section.time, incoming_section.time,
                    req.requestId[:4].hex(), req.type, req.subTypeId, req.serviceId, rep.requestId[:4].hex(), rep.type, rep.subTypeId, rep.serviceId,
                    'M' if rep.isMultipart else ' ',
                    ' ' if method.name == 'ping' else 'C' if method.name == 'openConnection' else '.',
                    # 'u' if incoming_section.uid else ' ',
                    '<' if rep.requestId != req.requestId else ' ',
                ))

                try:
                    if outputs_pb[0].DESCRIPTOR.full_name == "Devialet.CallMeMaybe.ConnectionReply":
                        service_list = outputs_pb[0].services
                    else:
                        print(outputs_pb[0].DESCRIPTOR.full_name)
                except Exception as e:
                    # print("Error: response empty: {} {}".format(type(e), e))
                    pass

                # pprint({
                #     "rpc_input_unknown": heuristic_search(outgoing_pb[1]),
                #     "rpc_output_unknown": [heuristic_search(x) for x in incoming_pb[1:]],
                #     "service_name": service_name,
                #     "exception": [type(e), e],
                #     "raw_decode_input": raw_decode(outgoing_pb[1]),
                #     "raw_decode_output": [raw_decode(x) for x in incoming_pb[1:]],
                #     "service_list": service_list,
                #     "magic": incoming_section.magic
                # })

        i = 0
        for incoming in incoming_iterator:
            i += 1

        if i != 0:
            print("Error: There were {} incoming sections remaining".format(i))

        i = 0
        for outgoing in outgoing_iterator:
            i += 1

        if i != 0:
            print("Error: There were {} outgoing sections remaining".format(i))


class DevialetManyFlows:
    def __init__(self, name=''):
        self.name = name
        self.flows = {}

    def add_flow(self, flow, phantom_port=0, spark_port=0):
        self.flows[(phantom_port, spark_port)] = flow

# class DevialetDecoder:
#     def __init__(self):
#         self.magics = [0xc2, 0xc3]
#         self.magic_headers = [b'\xc2\x01\x00\x00\x00\x00', b'\xc3\x01\x00\x00\x00\x00']

#     def decode_sessions(self):
#         raise NotImplementedError()

class AndroidFlows(DevialetManyFlows):
    def __init__(self, dirname):
        DevialetManyFlows.__init__(self)
        self.dirname = dirname

        for capture in sorted(os.listdir(self.dirname)):
            time, port = re.match('^([0-9]+)_([0-9]+).dat$', capture).groups()
            if (port, port) in self.flows:
                flow = self.flows[(port, port)]
            else:
                flow = DevialetFlow(name=capture, phantom_port=port, spark_port=port, start_time=datetime.fromtimestamp(int(time)/1000))
                self.add_flow(flow, phantom_port=port, spark_port=port)

            for packet in self.packet_iter(os.path.join(self.dirname, capture)):
                flow.decode(packet['data'], time=packet['time'], incoming=packet['direction'])

        for key in self.flows:
            self.flows[key].close()
            self.flows[key].rpc_walk()

    def packet_iter(self, filename):
        i = 0
        with open(filename, 'rb') as file:
            header = file.read(16)
            while len(header) == 16:
                tstamp, direction, pad1, pad2, length, pad3 = struct.unpack('<qBBHhH', header)
                packet = {
                    'time': datetime.fromtimestamp(tstamp / 1000),
                    'direction': direction, #'->' if direction else '<-'
                    'number': i,
                    'length': length,
                    'merged': 1,
                    'data': file.read(length)
                }
                header = file.read(16)
                i += 1
                yield packet


    # def decode_sessions(self):
    #     for dir in self.dirs:
    #         self.decode_session(dir)
    #     return [self.decode_session(dir) for dir in self.dirs]

if __name__ == '__main__':
    flows = AndroidFlows('/path/to/android_capture/tmp/sess1')

    # decoder = AndroidCaptureDecoder(['sess' + str(i+1) for i in range(5)])
    # sessions = decoder.decode_sessions()

    # dump_file = open('all_decoded2.pickle', 'wb')
    # pickle.dump(sessions, dump_file)