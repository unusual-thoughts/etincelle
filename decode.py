import sys
import struct
from datetime import datetime
from io import BytesIO
import subprocess
from pprint import pprint

magics = [0xc2, 0xc3]

def decode_protobuf(data):
    process = subprocess.Popen(['protoc', '--decode_raw'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.stdin.write(data)
    process.stdin.close()
    ret = process.wait()
    if ret == 0:
        return process.stdout.read().decode()
    else:
        return 'Failed parsing: ' + ' '.join('{:02x}'.format(x) for x in data)

def decode_packet(packet):
    field_header = packet.read(6)
    firstbyte = magics[0]
    new_section = True
    sections = []
    ret = {'decoded': []}

    while len(field_header) == 6 and firstbyte in magics:
        firstbyte, same_section, field_length = struct.unpack('>BBL', field_header)
        field_data = packet.read(field_length)
        field = { 'firstbyte': firstbyte, 'data': field_data }

        if new_section:
            sections.append([field])
        else:
            sections[-1].append(field)           

        field_header = packet.read(6)
        # when second byte of section header is 0, next field is part of new section
        new_section = not same_section

    rest = packet.read()
    if len(field_header) != 0 or firstbyte not in magics or rest:
         ret.setdefault('error', []).append('Found garbage at end of packet: header={} rest={}'.format(
            field_header.hex(), rest.hex()))

    for section in sections:
        i = 0
        obj = {'magic': section[0]['firstbyte']} #{'fields': [sub.hex() for sub in section]}

        # Delimiter, always empty
        if len(section[i]['data']) != 0:
            obj.setdefault('error', []).append('Weird, field {}/{} of length {} instead of {}'.format(
                i, len(section), len(section[i]['data']), 0))
        i += 1

        # Extra field (+ delimiter) that doesnt decode into protobuf, some kind of uid?
        if len(section) == 5 and len(section[i]['data']) == 16 and len(section[i+1]['data']) == 0:
            obj['uid'] = section[i]['data'].hex()
            i += 2
        
        # Remaining fields should all be protobufs
        while i < len(section):
            obj.setdefault('protobufs', []).append(decode_protobuf(section[i]['data']))
            if section[i]['firstbyte'] != obj['magic']:
                obj.setdefault('error', []).append('Weird, magic mismatch {} != {}'.format(
                    section[i]['firstbyte'], obj['magic']))
            i += 1

        ret['decoded'].append(obj)

    return ret

def is_whole_packet(packet):
    field_header = packet.read(6)
    firstbyte = magics[0]

    while len(field_header) == 6 and firstbyte in magics:
        firstbyte, same_section, field_length = struct.unpack('>BBL', field_header)
        field = packet.read(field_length)

        field_header = packet.read(6)

    return (field_length == len(field))

print('')
print(sys.argv[1])

packets = []

with open(sys.argv[1], 'rb') as file:
    header = file.read(16)
    packets = []
    last_packet_whole = True

    while len(header) == 16:
        tstamp, direction, pad1, pad2, length, pad3 = struct.unpack('<qBBHhH', header)
        packet = {
            'time': datetime.fromtimestamp(tstamp / 1000),
            'direction': direction, #'->' if direction else '<-'
            'number': len(packets),
            'length': length,
            'merged': 1,
            'data': file.read(length)
        }

        if not last_packet_whole:
            packets[-1]['data'] += packet['data']
            packets[-1]['merged'] += 1
            last_packet_whole = is_whole_packet(BytesIO(packets[-1]['data']))

        elif packet['data'][:6] == b'\xc2\x01\x00\x00\x00\x00' or packet['data'][:6] == b'\xc3\x01\x00\x00\x00\x00':
            packets.append(packet)
            last_packet_whole = is_whole_packet(BytesIO(packet['data']))

        else:
            packet['error'] = 'Unknown packet {}... '.format(
                    ' '.join('{:02x}'.format(x) for x in packet['data']))

        header = file.read(16)

for packet in packets:
    packet.update(decode_packet(BytesIO(packet.pop('data'))))

pprint(packets)