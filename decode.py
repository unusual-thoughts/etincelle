import sys
import struct
from datetime import datetime
from io import BytesIO
import subprocess
from pprint import pprint

def decode_packet(packet, magic):
    section_header = packet.read(6)
    firstbyte = magic
    sections = []
    same_section = False

    while len(section_header) == 6 and firstbyte == magic:
        firstbyte, same_section, section_length = struct.unpack('>BBL', section_header)
        section = packet.read(section_length)


        sections.append({
            "is_protobuf": is_notprotobuf,
            "data": section
        })

        section_header = packet.read(6)

    return sections

def is_whole_packet(packet, magic):
    section_header = packet.read(6)
    firstbyte = magic

    while len(section_header) == 6 and firstbyte == magic:
        firstbyte, is_notprotobuf, section_length = struct.unpack('>BBL', section_header)
        section = packet.read(section_length)

        section_header = packet.read(6)

    return (section_length == len(section))

print('')
print(sys.argv[1])

packets = []

with open(sys.argv[1], 'rb') as file:
    header = file.read(16)
    packets = []
    last_packet_whole = True

    while len(header) == 16:
        tstamp, direction, pad1, pad2, length, pad3 = struct.unpack('<qBBHhH', header)
        tstamp = datetime.fromtimestamp(tstamp / 1000)
        #print(datetime.fromtimestamp(tstamp/1000))
        content = file.read(length)
        #print(''.join('{:02x}'.format(x) for x in content))

        if not last_packet_whole:
            magic = packets[-1]["data"][0]
            packets[-1]["data"] += content

            last_packet_whole = is_whole_packet(BytesIO(packets[-1]["data"]), magic)
            print("Split packet id={}, len={}".format(len(packets), len(content)))

        elif content[:6] == b'\xc2\x01\x00\x00\x00\x00' or content[:6] == b'\xc3\x01\x00\x00\x00\x00':
            magic = content[0]
            packets.append({
                "time": tstamp,
                "direction": direction,
                "data": content
            })

            last_packet_whole = is_whole_packet(BytesIO(content), magic)
            if not last_packet_whole:
                print("Split packet id={}, len={}".format(len(packets), len(content)))

        else:
            print("Unknown packet #{}: {}... (len={})".format(len(packets), ' '.join('{:02x}'.format(x) for x in content[:16]), len(content)))
            # print('{:03d} {} {} {}'.format(id, '->' if direction else '<-', length, sys.argv[1]))
            # print(''.join('{:02x}'.format(x) for x in content[:10]))
        #print(length, direction)

        header = file.read(16)


    # print(len(packets))

decoded = [ {
    "time": packet["time"],
    "direction": packet["direction"],
    "magic": packet["data"][0],
    "decoded": decode_packet(BytesIO(packet["data"]), packet["data"][0])
} for packet in packets ]

# pprint(decoded)
# print()
# print(packets)

# def decode_dvlt(packet, magic):
#     i = 0
#     magic = b'\xc2'
#     while i <= len(packet)-6 and magic == b'\xc2':
#         print('* {}/{}'.format(i, len(packet)))
#         print(''.join('{:02x}'.format(x) for x in packet[i:i+6]))
#         magic, is_notprotobuf, section_length = struct.unpack('>ccL', packet[i:i+6])

#         i += section_length + 6

#         # print(packet[i+2:i+6])
#     print('* {}/{}'.format(i, len(packet)))
#     print(''.join('{:02x}'.format(x) for x in packet[i:]))
#     # print(section_length, len(packet)-i)
#     print("")
#     # print(''.join('{:02x}'.format(x) for x in packet[i:]))

#     return

for packet in decoded:
    for section in packet['decoded']:
        if len(section['data']): #section['is_protobuf'] and 
            process = subprocess.Popen(['protoc', '--decode_raw'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write(section['data'])
            process.stdin.close()
            ret = process.wait()
            if ret == 0:
                section['data'] = process.stdout.read().decode()
            else:
                section['data'] = 'Failed parsing: ' + ' '.join('{:02x}'.format(x) for x in section['data'])
            # print(protod.decode())
            # print()
        # else:
        #     print("HEX"+section['data'].hex())
        #     section['data'] = ' '.join('{:02x}'.format(x) for x in section['data'])

pprint(decoded)
