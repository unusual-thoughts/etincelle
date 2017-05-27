import pickle
from collections import Counter
from pprint import pprint
from protobuf_to_dict import protobuf_to_dict
# import itertools

from dvlt_messages import all_msgs
from dvlt_services import all_services

import RPCMessages_pb2

dump_file = open('../all_decoded.pickle', 'rb')
sessions = pickle.load(dump_file)

# Show stats about ports in each session
# pprint([{
#           "session": session['name'],
#           "port_stats": sorted(Counter([
#               capture['port'] for capture in session['captures']
#           ]).items())
#       } for session in sessions])

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


# Direction == 0 is from Spark to Phantom
outgoing_packets = [packet['decoded'] for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 0]
incoming_packets = [packet['decoded'] for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 1]

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
        req = interpret_as(outgoing, "Devialet.CallMeMaybe.Request")
        rep = interpret_as(incoming, "Devialet.CallMeMaybe.Reply")

        if rep.requestId != req.requestId:
            print("Error: Inconstistent requestId, maybe protobufs not in lockstep")

        method = {}
        service = {}
        package = {}

        # if not(service_list):
        if rep.serviceId == req.serviceId == 0 and not service_list:
            # Assume initial service is CallmeMaybe.Connection, which is placed first
            package = all_services[0]
            service = package['services'][req.type]
            method = service['methods'][req.subTypeId]

        elif rep.serviceId in [service.id for service in service_list]:
            service_name = [service.name for service in service_list if service.id == rep.serviceId][0]
            package_name = '.'.join(service_name.split('.')[1:-2])
            service_name = '.'.join(service_name.split('.')[-2:-1])
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
                            method = service['methods'][req.subTypeId]
        else:
            print("Unknown service ID {}".format(rep.serviceId))

        pprint(rep)

        # TODO: handle multipart
        rpc_input = next(outgoing_iterator)
        rpc_output = next(incoming_iterator)

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

        except KeyError:
            pprint({
                "rpc_input_unknown": heuristic_search(rpc_input) if rpc_input else "empty protobuf",
                "rpc_output_unknown": heuristic_search(rpc_output) if rpc_output else "empty protobuf" 
            })            
            pass
        except Exception as e:
            print(type(e), e)

    else:
        print("Looks like we are out of sync or something")
        pprint({
            "0outgoing": possible_out if outgoing else "empty protobuf",
            "1incoming": possible_in if incoming else "empty protobuf" 
        })

    i += 1