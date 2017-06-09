import os
import re
import struct
from datetime import datetime
from io import BytesIO
from collections import deque

from dvlt_output import print_error, print_warning, print_info, print_data
from dvlt_pool import dvlt_pool


class DevialetSection:
    def __init__(self, raw_section, time=None):
        self.warnings = []
        self.raw_protobufs = []
        self.raw_fields = raw_section
        self.time = time

        # Sanity Checks
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
                print_warning(self.warnings)
        except Exception as e:
            print_error('in Section decode: {} {}', type(e), e)
            pass


class DevialetFlow:
    def __init__(self, name='', phantom_port=0, spark_port=0, start_time=datetime.now()):
        self.name = name
        self.phantom_port = phantom_port
        self.spark_port = spark_port
        self.start_time = start_time

        self.incoming_buf = BytesIO()
        self.outgoing_buf = BytesIO()
        self.incoming_sections = deque()
        self.outgoing_sections = deque()
        self.magics = [0xC2, 0xC3]
        self.warnings = []
        self.rpc_server_is_phantom = True
        self.service_list = dvlt_pool.messages['Devialet.CallMeMaybe.ServicesList']().services

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
            # print_error('bad section: {}, seeking back to {}', field_header, pos)
            return False

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
        buf.seek(0, 2)
        buf.write(raw)
        buf.seek(pos)
        while self.read_one_section(buf, dest, time=time):
            pass
        # if buf.tell() > pos:
        #     print_info('Succesfully decoded {} bytes', buf.tell() - pos)

    def close(self):
        rest_incoming = self.incoming_buf.read()
        rest_outgoing = self.outgoing_buf.read()

        if rest_incoming:
            self.warnings.append('Found garbage at end of incoming flow: {}...'.format(
                ' '.join('{:02x}'.format(x) for x in rest_incoming[:50])))

        if rest_outgoing:
            self.warnings.append('Found garbage at end of outgoing flow: {}...'.format(
                ' '.join('{:02x}'.format(x) for x in rest_outgoing[:50])))

        if self.warnings:
            print_warning(self.warnings)

        print_info('flow {} has {} incoming and {} outgoing sections',
                   self.name, len(self.incoming_sections), len(self.outgoing_sections))

        self.incoming_buf.close()
        self.outgoing_buf.close()

    def find_service(self, rep):
        service_name = 'com.devialet.callmemaybe.connection'
        try:
            if rep.serviceId != 0 or self.service_list:
                service_lowercase_name = [service.name for service in self.service_list if service.id == rep.serviceId][0]
                # PlayThatFunkyMusic is nowhere in protobufs
                # service_lowercase_name = service_lowercase_name.replace('playthatfunkymusic', 'toomanyflows')
                service_name = '.'.join(service_lowercase_name.split('.')[:-1])
                while service_name not in dvlt_pool.service_by_name and len(service_name.split('.')) > 1:
                    service_name = '.'.join(service_name.split('.')[:-1])
                    print_info('truncating {} to {}'.format(service_lowercase_name, service_name))
        except IndexError:
            print_error('Service ID {} not in list {}', rep.serviceId, ' '.join(str(self.service_list).split('\n')))
        return service_name

    def rpc_walk(self):
        # Each section should correspond to a RPC request/reply,
        # with 2 outgoing protobufs and 2 (or more for propertyget/multipart) incoming,
        # or an RPC event, with 2 (or more?) incoming, and no outgoing

        print_info('Walking {}', self.name)
        if not self.rpc_server_is_phantom:
            print_warning('RPC server appears to be Spark here')

        print_data('=' * 32)

        for i in range(len(self.incoming_sections)):
            print_data('-' * 16)
            incoming_section = self.incoming_sections.popleft()
            incoming_pb = incoming_section.raw_protobufs

            if incoming_section.magic == 0xC3:
                # Event?
                try:
                    evt = dvlt_pool.interpret_as(incoming_pb[0], 'Devialet.CallMeMaybe.Event')
                    service_name = self.find_service(evt)

                    method, input_pb, outputs_pb = dvlt_pool.process_rpc(service_name, evt, incoming_pb[1], incoming_pb[1:], is_event=True)
                    if method.containing_service.full_name == 'Devialet.CallMeMaybe.Connection':
                        if method.name == 'serviceAdded':
                            print_info('Extending list of services')
                            self.service_list.add(name=input_pb.name, id=input_pb.id)

                    # The 'uid' parameter in the section, when present (== when magic is C3, and only on incoming packets)
                    # should be equal to the server ID
                    print_info('in_time:{} evt:{} {}/{:>10d}/{:>12d}{:31s} {} E',
                               incoming_section.time,
                               evt.serverId[:4].hex(), evt.type, evt.subTypeId, evt.serviceId,
                               '',
                               incoming_section.uid[:4].hex())
                except IndexError:
                    print_error('not enough incoming protos for event ({}) < 2', len(incoming_pb))
                except AttributeError:
                    pass

            else:
                try:
                    outgoing_section = self.outgoing_sections.popleft()
                    outgoing_pb = outgoing_section.raw_protobufs
                    req = dvlt_pool.interpret_as(outgoing_pb[0], 'Devialet.CallMeMaybe.Request')
                    rep = dvlt_pool.interpret_as(incoming_pb[0], 'Devialet.CallMeMaybe.Reply')
                    bad_reqs = deque()

                    # (First two bytes (or more) of request id appear to be sequential)
                    while rep.requestId != req.requestId:
                        bad_reqs.appendleft(outgoing_section)
                        print_warning('Request id {} out of order', req.requestId.hex())
                        try:
                            outgoing_section = self.outgoing_sections.popleft()
                            outgoing_pb = outgoing_section.raw_protobufs
                            req = dvlt_pool.interpret_as(outgoing_pb[0], 'Devialet.CallMeMaybe.Request')
                        except IndexError:
                            # Reached end of outgoing_sections
                            break
                    self.outgoing_sections.extendleft(bad_reqs)

                    if not rep.isMultipart and len(incoming_pb) > 2:
                        print_warning('we got more incoming protobufs than we should have, not Multipart')

                    if len(outgoing_pb) > 2:
                        print_error('we got more than 2 outgoing protobufs')

                    if len(outgoing_pb) < 2:
                        print_error('we got less than 2 outgoing protobufs')

                    if len(incoming_pb) < 2:
                        print_error('we got less than 2 incoming protobufs')

                    service_name = self.find_service(rep)
                    method, input_pb, outputs_pb = dvlt_pool.process_rpc(
                        service_name, rep, outgoing_pb[1], incoming_pb[1:])

                    if method.containing_service.full_name == 'Devialet.CallMeMaybe.Connection':
                        if method.name == 'openConnection':
                            self.service_list = outputs_pb[0].services

                    print_info('out_time:{} in_time:{} req:{}/{}/{:>10d}/{:>12d}, rep:{}/{}/{:>10d}/{:>12d} {}{}{}',
                               outgoing_section.time, incoming_section.time,
                               req.requestId[:4].hex(), req.type, req.subTypeId, req.serviceId, rep.requestId[:4].hex(), rep.type, rep.subTypeId, rep.serviceId,
                               'M' if rep.isMultipart else ' ',
                               ' ' if method.name == 'ping' else 'C' if method.name == 'openConnection' else '.',
                               '<' if rep.requestId != req.requestId else ' ')

                except IndexError:
                    print_error('Stream ended prematurely, missing outgoing section')
                except Exception as e:
                    print_error('Unexpected {} {}', type(e), e)

        if len(self.incoming_sections) != 0:
            print_error('There were {} incoming sections remaining', len(self.incoming_sections))

        if len(self.outgoing_sections) != 0:
            print_error('There were {} outgoing sections remaining', len(self.outgoing_sections))


class DevialetManyFlows:
    def __init__(self, name=''):
        self.name = name
        self.flows = {}

    def add_flow(self, flow):
        self.flows[(flow.phantom_port, flow.spark_port)] = flow


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
                self.add_flow(flow)

            it = self.packet_iter(os.path.join(self.dirname, capture))
            try:
                first_packet = next(it)
                # If first packet is incoming, then rpc server is Spark
                flow.rpc_server_is_phantom = not first_packet['direction']
                flow.decode(first_packet['data'], time=first_packet['time'], incoming=False)
                if not flow.rpc_server_is_phantom:
                    print_info('Found flow where Spark appears to be RPC server')
                for packet in it:
                    # Switch incoming/outgoing if rpc server is spark
                    is_incoming = packet['direction'] ^ (not flow.rpc_server_is_phantom)
                    flow.decode(packet['data'], time=packet['time'], incoming=is_incoming)
            except:
                # Empty flow
                pass

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
                    'direction': direction,
                    'number': i,
                    'length': length,
                    'merged': 1,
                    'data': file.read(length)
                }
                header = file.read(16)
                i += 1
                yield packet

if __name__ == '__main__':
    flows = AndroidFlows('/path/to/android_capture/tmp/sess1')

    # decoder = AndroidCaptureDecoder(['sess' + str(i+1) for i in range(5)])
    # sessions = decoder.decode_sessions()

    # dump_file = open('all_decoded2.pickle', 'wb')
    # pickle.dump(sessions, dump_file)
