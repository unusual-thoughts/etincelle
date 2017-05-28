import pickle, re
# from collections import Counter
from pprint import pprint
from protobuf_to_dict import protobuf_to_dict
# import itertools

from dvlt_messages import all_msgs
from dvlt_services import all_services

import RPCMessages_pb2

def read_protobuf_raw_in_order(packets):
    for packet in packets:
        for section in packet:
            for protobuf in section['protobufs']:
                yield protobuf['raw']

def interpret_as(raw_protobuf, proto_name):
    for proto in all_msgs:
        if proto['name'] == proto_name:
            try:
                proto['msg'].ParseFromString(raw_protobuf)
                return proto['msg']
            except:
                pass
    return None

def full_len(d):
    if type(d) == dict:
        return sum(full_len(v) for v in d.values())
    elif type(d) == list:
        return sum(full_len(v) for v in d)
    else:
        return 1
    
def heuristic_search(raw_protobuf, filter=""):
    for i in range(len(all_msgs)):
        if all_msgs[i]['name'].startswith(filter):
            try:
                all_msgs[i]['msg'].ParseFromString(raw_protobuf)
                all_msgs[i]['length'] = full_len(protobuf_to_dict(all_msgs[i]['msg']))
            except:
                all_msgs[i]['length'] = -1
                pass
        else:
            all_msgs[i]['length'] = -1
    return [{
            'name': test['name'],
            'length': test['length'],
            # 'msg': protobuf_to_dict(test['msg'])
        } for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 2 or test['length'] == max(
        result['length'] for result in all_msgs
    )]

# pprint(heuristic_search(incoming_packets[0][0]['protobufs'][1]['raw']))

import subprocess
def decode_protobuf(data):
    process = subprocess.Popen(['protoc', '--decode_raw'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.stdin.write(data)
    process.stdin.close()
    ret = process.wait()
    if ret == 0:
        return {
            "raw": data,
            "protoc": process.stdout.read().decode()
        }
    else:
        return {
            "raw": data,
            "protoc": "",
            "error": 'Failed to parse: ' + ' '.join('{:02x}'.format(x) for x in data)
        }

def rpc_walk(sessionId, captureId):
    # Actually the iterator could be made to simply iterate over sections,
    # as each section should correspond to a RPC request/reply, 
    # with 2 protobufs each time

    # Yes this is probably the only way to correctly handle multiparts

    # The "uid" parameter in the section, when present, 
    # is apparently equal to the first member of a 4 element protobuf in the same section

    # Direction == 0 is from Spark to Phantom
    outgoing_packets = [packet['decoded'] for packet in sessions[sessionId]['captures'][captureId]['packets'] if packet['direction'] == 0]
    incoming_packets = [packet['decoded'] for packet in sessions[sessionId]['captures'][captureId]['packets'] if packet['direction'] == 1]

    incoming_iterator = read_protobuf_raw_in_order(incoming_packets)
    outgoing_iterator = read_protobuf_raw_in_order(outgoing_packets)

    i = 0
    service_list = RPCMessages_pb2.ServicesList().services

    # this may cut out some protobufs at the end (shortest of incoming or outgoing)
    for (incoming, outgoing) in zip(incoming_iterator, outgoing_iterator):
        possible_out = heuristic_search(outgoing, filter="Devialet.CallMeMaybe")
        possible_in  = heuristic_search(incoming, filter="Devialet.CallMeMaybe")

        if "Devialet.CallMeMaybe.Request" in [
            x['name'] for x in possible_out] and "Devialet.CallMeMaybe.Reply" in [
            x['name'] for x in possible_in]:

            print("")
            req = RPCMessages_pb2.Request()
            rep = RPCMessages_pb2.Reply()
            req.CopyFrom(interpret_as(outgoing, "Devialet.CallMeMaybe.Request"))
            rep.CopyFrom(interpret_as(incoming, "Devialet.CallMeMaybe.Reply"))

            if rep.requestId != req.requestId:
                print("Error: Inconstistent requestId, maybe protobufs not in lockstep")

            method = {}
            service = {}
            package = {}
            service_name = ""

            # if not(service_list):
            if rep.serviceId == req.serviceId == 0 and not service_list:
                # Assume initial service is CallmeMaybe.Connection, which is placed first
                package = all_services[0]
                service = package['services'][req.type]
                method = service['methods'][req.subTypeId]

            elif rep.serviceId in [service.id for service in service_list]:
                service_name = [service.name for service in service_list if service.id == rep.serviceId][0]
                # package_name = '.'.join(service_name.split('.')[1:-2])
                # service_name = '.'.join(service_name.split('.')[-2:-1])
                package_name, service_name = re.match(
                    '^[^\.]+\.(.*?)(?:-0)?\.([^\.]+?)(?:-0)?\.[^\.]+$', service_name).groups()
                # this isnt perferc, apparently sometimes more than one service: com.devialet.getthepartystarted.configuration-0.player-0.ece3ce2e

                # print(package_name, service_name)
                
                for p in all_services:
                    if p['package_name'].lower() == package_name:
                        for s in p['services']:
                            if s['name'].lower() == service_name:
                                # for m in s['methods']:
                                #     if m['name'] == 
                                service = s
                                package = p
                                print('service {} from {} appears to correspond to type {}'.format(
                                    service_name, package_name, req.type
                                ))
                                try:
                                    method = service['methods'][req.subTypeId]
                                except IndexError:
                                    print("Error: subTypeId {} too big for package {}, service {}".format(
                                        req.subTypeId, package_name, service_name
                                    ))
                if package == {} or service == {}:
                    print('Error: service "{}" or package "{}" not found in database'.format(service_name, package_name))
            else:
                print("Error: Unknown service ID {}".format(rep.serviceId))


            # TODO: handle multipart
            if rep.isMultipart:
                while rep.isMultipart:
                    print("WARNING multipart")
                    pprint(protobuf_to_dict(rep))
                    rep = RPCMessages_pb2.Reply()
                    try:
                        new_incoming = next(incoming_iterator)
                        rep.CopyFrom(interpret_as(new_incoming, "Devialet.CallMeMaybe.Reply"))
                    except StopIteration:
                        print("Error: ran out of incoming packets in multipart handling")
                        pass
            else:
                try:
                    rpc_input = next(outgoing_iterator)
                except StopIteration:
                    print("Error: ran out of outgoing packets for RPC input")

                try:
                    rpc_output = next(incoming_iterator)
                except StopIteration:
                    print("Error: ran out of incoming packets for RPC output")

                try:
                    rpc_input_pb = interpret_as(rpc_input, method['input_type'])
                    rpc_output_pb = interpret_as(rpc_output, method['output_type'])
                    pprint({
                        "package_name": package['package_name'],
                        "service_name": service['name'],
                        "rpc_name": method['name'],
                        "rpc_input": protobuf_to_dict(rpc_input_pb),
                        "rpc_output": protobuf_to_dict(rpc_output_pb),
                        "rpc_input_type": method['input_type'],
                        "rpc_output_type": method['output_type'],
                    })

                    if method['output_type'] == "Devialet.CallMeMaybe.ConnectionReply":
                        service_list = rpc_output_pb.services

                except KeyError as e:
                    # If method/service is empty, meaning that not found in database
                    pprint({
                        "rpc_input_unknown": heuristic_search(rpc_input) if rpc_input else "empty protobuf",
                        "rpc_output_unknown": heuristic_search(rpc_output) if rpc_output else "empty protobuf",
                        "service_name": service_name,
                        "exception": [type(e), e],
                        "raw_decode_input": decode_protobuf(rpc_input),
                        "raw_decode_output": decode_protobuf(rpc_input),
                        "service_list": service_list,
                    })
                    pass
                except Exception as e:
                    print(type(e), e)

        else:
            print("Looks like we are out of sync or something")
            pprint({
                "0utgoing": heuristic_search(outgoing, filter="Devialet") if outgoing else "empty protobuf",
                "1ncoming": heuristic_search(incoming, filter="Devialet") if incoming else "empty protobuf",
                "raw_decode_0utgoing": decode_protobuf(outgoing),
                "raw_decode_1ncoming": decode_protobuf(incoming),
            })

        i += 1

    i = 0
    for incoming in incoming_iterator:
        i += 1

    if i != 0:
        print("Error: There were {} incoming packets remaining".format(i))

    i = 0
    for outgoing in outgoing_iterator:
        i += 1

    if i != 0:
        print("Error: There were {} outgoing packets remaining".format(i))

if __name__ == '__main__':

    dump_file = open('../all_decoded.pickle', 'rb')
    sessions = pickle.load(dump_file)


    sessionId = 0
    for captureId in range(len(sessions[sessionId]['captures'])):
        capture_without_packets = sessions[sessionId]['captures'][captureId].copy()
        capture_without_packets['packets'] = []
        print(capture_without_packets)
        rpc_walk(sessionId, captureId)