import pickle
from collections import Counter
from pprint import pprint
# from protobuf_to_dict import protobuf_to_dict
# import itertools

# from dvlt_messages import all_msgs
# from dvlt_services import all_services

# import RPCMessages_pb2

dump_file = open('../all_decoded.pickle', 'rb')
sessions = pickle.load(dump_file)

# Show stats about ports in each session
# pprint([{
#           "session": session['name'],
#           "port_stats": sorted(Counter([
#               capture['port'] for capture in session['captures']
#           ]).items())
#       } for session in sessions])

# Show stats about magic, direction, and presence of UID
number_of_uid = {
    0xc2: {"incoming": {True: 0, False: 0}, "outgoing": {True: 0, False: 0}},
    0xc3: {"incoming": {True: 0, False: 0}, "outgoing": {True: 0, False: 0}}
}
for session in sessions:
    for capture in session['captures']:
        for packet in capture['packets']:
            for section in packet['decoded']:
                number_of_uid[section['magic']]['incoming' if packet['direction'] else 'outgoing'][('uid' in section.keys())] += 1

# UID is present if and only if magic is C3
pprint(number_of_uid)

# Show stats about number of protobufs
number_of_protobufs_c2 = []
number_of_protobufs_c3 = []
for session in sessions:
    for capture in session['captures']:
        for packet in capture['packets']:
            for section in packet['decoded']:
                if section['magic'] == 0xc2:
                    number_of_protobufs_c2.append(len(section['protobufs']))
                elif section['magic'] == 0xc3:
                    number_of_protobufs_c3.append(len(section['protobufs']))

# All packets of magic C3 have exactly 2 protobufs
# Packets of magic C2 have varying length, but usually 2
pprint({
    "frequency of number of protobufs when magic is C2": sorted(Counter(number_of_protobufs_c2).items()),
    "frequency of number of protobufs when magic is C3": sorted(Counter(number_of_protobufs_c3).items()),
}   )

# All the packets with more than 2 protobufs are the third packet in a capture
ports = []
for session in sessions:
    for capture in session['captures']:
        capture['nb_protobufs'] = []
        capture['packet_numbers'] = []
        for p, packet in enumerate(capture['packets']):
            for section in packet['decoded']:
                if len(section['protobufs']) != 2:
                    capture['nb_protobufs'].append(len(section['protobufs']))
                    capture['packet_numbers'].append(p)
                    # pprint(section)

        capture['packets'] = []
        if capture['nb_protobufs']:
            pprint(capture)
            ports.append(capture['port'])

pprint(sorted(Counter(ports).items()))
# [('33161', 6),
#  ('34075', 18),
#  ('35236', 36),
#  ('38521', 59),
#  ('39905', 12),
#  ('42713', 39),
#  ('42833', 12),
#  ('47963', 18),
#  ('50476', 42),
#  ('53750', 6),
#  ('53776', 6),
#  ('53841', 19),
#  ('55822', 19),
#  ('55833', 58),
#  ('57985', 18),
#  ('60830', 12)]
