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

def read_protobuf_sections_in_order(packets):
    for packet in packets:
        for section in packet:
                yield section

def interpret_as(raw_protobuf, proto_name):
    for proto in all_msgs:
        if proto['name'] == proto_name:
            try:
                proto['msg'].ParseFromString(raw_protobuf)
                return proto['msg'].__deepcopy__()
            except:
                pass
    return None

def full_len(d):
    if type(d) == dict:
        return 1 + sum(full_len(v) for v in d.values())
    elif type(d) == list:
        return 1 + sum(full_len(v) for v in d)
    else:
        return 1
    
def heuristic_search(raw_protobuf, filter="", strict=True):
    if len(raw_protobuf) == 0:
        return { "empty protobuf" }
    for proto in all_msgs:
        if proto['name'].startswith(filter):
            try:
                tmp = proto['msg'].__deepcopy__()
                tmp.ParseFromString(raw_protobuf)
                proto['length'] = full_len(protobuf_to_dict(tmp))
                if strict and len(tmp.FindInitializationErrors()) > 0:
                    proto['length'] = -1
            except Exception as e:
                # print("Error in heuristic:", type(e), e)
                proto['length'] = -1
                # pass
        else:
            proto['length'] = -1
    return [{
            'name': test['name'],
            'length': test['length'],
            # 'msg': protobuf_to_dict(test['msg'])
        } for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 0 and (test['length'] > 2 or test['length'] == max(
        result['length']) for result in all_msgs
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

def find_method(rep, service_list):
    method = {}
    service = {}
    package = {}
    service_name = ""

    # if not(service_list):
    if rep.serviceId == 0 and not service_list:
        # Assume initial service is CallmeMaybe.Connection, which is placed first
        package = all_services[0]
        service = package['services'][rep.type]
        method = service['methods'][rep.subTypeId]

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
                            service_name, package_name, rep.type
                        ))
                        try:
                            method = service['methods'][rep.subTypeId]
                        except IndexError:
                            print("Error: subTypeId {} too big for package {}, service {}".format(
                                rep.subTypeId, package_name, service_name
                            ))
        if package == {} or service == {}:
            print('Error: service "{}" or package "{}" not found in database'.format(service_name, package_name))
    else:
        print("Error: Unknown service ID {}".format(rep.serviceId))

    return (package, service, method)


def rpc_walk(sessionId, captureId):
    # Actually the iterator could be made to simply iterate over sections,
    # as each section should correspond to a RPC request/reply, 
    # with 2 protobufs each time

    # Yes this is probably the only way to correctly handle multiparts

    # The "uid" parameter in the section, when present (== when magic is C3, and only on incoming packets)
    # is apparently equal to the first member of a 4 element protobuf in the same section

    # Direction == 0 is from Spark to Phantom
    outgoing_packets = [packet['decoded'] for packet in sessions[sessionId]['captures'][captureId]['packets'] if packet['direction'] == 0]
    incoming_packets = [packet['decoded'] for packet in sessions[sessionId]['captures'][captureId]['packets'] if packet['direction'] == 1]

    incoming_iterator = read_protobuf_sections_in_order(incoming_packets)
    outgoing_iterator = read_protobuf_sections_in_order(outgoing_packets)

    service_list = RPCMessages_pb2.ServicesList().services

    # this may cut out some protobufs at the end (shortest of incoming or outgoing)
    for (incoming_section, outgoing_section) in zip(incoming_iterator, outgoing_iterator):
        print("")

        try:
            req = interpret_as(outgoing_section['protobufs'][0]['raw'], "Devialet.CallMeMaybe.Request")
            rep = interpret_as(incoming_section['protobufs'][0]['raw'], "Devialet.CallMeMaybe.Reply")
        except:
            print("Error: Looks like we are out of sync or something")
            pprint({
                "0utgoing_notrequest": heuristic_search(outgoing_section['protobufs'][0]['raw'], filter="Devialet"),
                "1ncoming_notreply": heuristic_search(incoming_section['protobufs'][0]['raw'], filter="Devialet"),
                "raw_decode_0utgoing": decode_protobuf(outgoing),
                "raw_decode_1ncoming": decode_protobuf(incoming),
            })

        if rep.requestId != req.requestId:
            print("Error: Inconstistent requestId, maybe protobufs not in lockstep. type/subTypeId/serviceId: rep:{}/{}/{}, req:{}/{}/{}".format(
                rep.type, rep.subTypeId, rep.serviceId, req.type, req.subTypeId, req.serviceId,
            ))

        package, service, method = find_method(rep, service_list)

        # TODO: handle multipart
        if rep.isMultipart:
            print("WARNING multipart")
            if len(incoming_section['protobufs']) == 2:
                print("Error: multipart but only 2 incoming protobufs")
            pprint(protobuf_to_dict(rep))

        if len(incoming_section['protobufs']) > 2 and not rep.isMultipart:
            print("Error: we got more incoming protobufs than we should have, not Multipart")

        if len(outgoing_section['protobufs']) > 2:
            print("Error: we got more than 2 outgoing protobufs")

        if len(outgoing_section['protobufs']) < 2:
            print("Error: we got less than 2 outgoing protobufs")

        if len(incoming_section['protobufs']) < 2:
            print("Error: we got less than 2 incoming protobufs")


        rpc_output = []
        last_output = {'raw': b''}
        try:
            
            for output_proto in incoming_section['protobufs'][1:]:
            
                rpc_input = interpret_as(outgoing_section['protobufs'][1]['raw'], method['input_type'])
                rpc_output.append(interpret_as(output_proto['raw'], method['output_type']))

                if method['output_type'] == "Devialet.CallMeMaybe.ConnectionReply":
                    service_list = rpc_output[0].services

                last_output = output_proto

            rpc_decoded = {
                "package_name": package['package_name'],
                "service_name": service['name'],
                "rpc_name": method['name'],
                "rpc_input": protobuf_to_dict(rpc_input),
                "rpc_output": [ protobuf_to_dict(pb) for pb in rpc_output],
                "rpc_input_type": method['input_type'],
                "rpc_output_type": method['output_type'],
            }

            if incoming_section['magic'] == 0xC3:
                rpc_decoded['uid'] = incoming_section['uid']

            # pprint(rpc_decoded)
        except KeyError as e:
            # If method/service is empty, meaning that not found in database
            print("Error: no package, service or method")
            pprint({
                "rpc_input_unknown": heuristic_search(outgoing_section['protobufs'][1]['raw']),
                "rpc_output_unknown": [heuristic_search(x['raw']) for x in incoming_section['protobufs'][1:]],
                "service_name": [service.name for service in service_list if service.id == rep.serviceId][0],
                "exception": [type(e), e],
                "raw_decode_input": decode_protobuf(outgoing_section['protobufs'][1]['raw']),
                "raw_decode_output": [decode_protobuf(x['raw']) for x in incoming_section['protobufs'][1:]],
                "service_list": service_list,
                "magic": incoming_section['magic']
            })
            pass
        except Exception as e:
            print("Error:", type(e), e)

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

if __name__ == '__main__':

    dump_file = open('../all_decoded.pickle', 'rb')
    sessions = pickle.load(dump_file)


    sessionId = 0
    for captureId in range(len(sessions[sessionId]['captures'])):
        capture_without_packets = sessions[sessionId]['captures'][captureId].copy()
        capture_without_packets['packets'] = []
        print(capture_without_packets)
        rpc_walk(sessionId, captureId)