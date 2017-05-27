import pickle
from collections import Counter
from pprint import pprint
from protobuf_to_dict import protobuf_to_dict

import SaveMe.SaveMe_pb2
import WhatsUp_pb2
import google.protobuf.descriptor_pb2
import MasterOfPuppets.Configuration_pb2
import AppleAirPlay.Playback_pb2
import LeftAlone.Configuration_pb2
import TwerkIt.SoundDesign_pb2
import TheSoundOfSilence.Playlist_pb2
import TheSoundOfSilence.OnlineSource_pb2
import TheSoundOfSilence.Artist_pb2
import TheSoundOfSilence.LiveSource_pb2
import TheSoundOfSilence.Session_pb2
import TheSoundOfSilence.Subcategory_pb2
import TheSoundOfSilence.Source_pb2
import TheSoundOfSilence.Node_pb2
import TheSoundOfSilence.TrackDetails_pb2
import TheSoundOfSilence.Collection_pb2
import TheSoundOfSilence.Picture_pb2
import TheSoundOfSilence.Album_pb2
import TheSoundOfSilence.Category_pb2
import TheSoundOfSilence.Track_pb2
import TooManyFlows.Playback_pb2
import TooManyFlows.Playlist_pb2
import TooManyFlows.History_pb2
import TooManyFlows.SoundControl_pb2
import TooManyFlows.Configuration_pb2
import TooManyFlows.Metadata_pb2
import TooManyFlows.SoundDesign_pb2
import TooManyFlows.Identifier_pb2
import Fresh.Fresh_pb2
import IMASlave4U.SoundControl_pb2
import IMASlave4U.Configuration_pb2
import IMASlave4U.SoundDesign_pb2
import RPCMessages_pb2
import SpotifyConnect.SpotifyConnect_pb2
import CallMeMaybe.CallMeMaybe_pb2
import CallMeMaybe.CommonMessages_pb2
import GetThePartyStarted.Player_pb2
import GetThePartyStarted.GetThePartyStarted_pb2
import GetThePartyStarted.Logging_pb2
import GetThePartyStarted.Aerobase_pb2

from dvlt_messages import all_msgs
from dvlt_services import all_services




dump_file = open('../all_decoded.pickle', 'rb')
sessions = pickle.load(dump_file)

# Show stats about ports in each session
# pprint([{
#           "session": session['name'],
#           "port_stats": sorted(Counter([
#               capture['port'] for capture in session['captures']
#           ]).items())
#       } for session in sessions])

# Direction == 0 is from Spark to Phantom
outgoing_packets = [packet['decoded'] for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 0]
incoming_packets = [packet['decoded'] for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 1]

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
                return protobuf_to_dict(proto['msg'])
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

# def heuristic_search_name(raw_protobuf, filter=""):
#     for i in range(len(all_msgs)):
#         if all_msgs[i]['name'].startswith(filter):
#             try:
#                 all_msgs[i]['msg'].ParseFromString(raw_protobuf)
#                 all_msgs[i]['length'] = full_len(protobuf_to_dict(all_msgs[i]['msg']))
#             except:
#                 all_msgs[i]['length'] = -1
#                 pass
#         else:
#             all_msgs[i]['length'] = -1
#     return [ test['name'] for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 2 or test['length'] == max(
#         result['length'] for result in all_msgs
#     )]

# pprint(heuristic_search(incoming_packets[0][0]['protobufs'][1]['raw']))

# this may cut out some protobufs at the end (shortest of incoming or outgoing)
i = 0
for (incoming, outgoing) in zip(read_protobuf_raw_in_order(incoming_packets), read_protobuf_raw_in_order(outgoing_packets)):
    possible_out = heuristic_search(outgoing, filter="Devialet.CallMeMaybe")
    possible_in  = heuristic_search(incoming, filter="Devialet.CallMeMaybe")

    if i % 2 == 0 and "Devialet.CallMeMaybe.Request" in [
        x['name'] for x in possible_out] and "Devialet.CallMeMaybe.Reply" in [
        x['name'] for x in possible_in]:
        print("")
        req = interpret_as(outgoing, "Devialet.CallMeMaybe.Request")
        rep = interpret_as(incoming, "Devialet.CallMeMaybe.Reply")
        if rep['requestId'] != req['requestId']:
            print("Error: Inconstistent requestId, maybe protobufs not in lockstep")
        pprint({
               'isMultipart': rep['isMultipart'],
               # 'requestId': b'3\nC\x02\x97\x0cO\xad\x97Y\xf0\xafS\x84\xbf\xda',
               # 'serverId': b'\x19\xf4\x06\xd4I~@\x93\xa3\x9a\xb0\xf1'
               #             b'\x01\xfb\x08J',
               'serviceId': rep['serviceId'],
               'subTypeId': rep['subTypeId'],
               'type': rep['type']
        })
    else:
        pprint({
            "0outgoing": possible_out if outgoing else "empty protobuf",
            "1incoming": possible_in if incoming else "empty protobuf" 
        })

    i += 1