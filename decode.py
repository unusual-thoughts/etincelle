import sys
import struct
from datetime import datetime
from io import BytesIO
import subprocess
from pprint import pprint

def decode_protobuf(data):
    process = subprocess.Popen(['protoc', '--decode_raw'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.stdin.write(data)
    process.stdin.close()
    ret = process.wait()
    if ret == 0:
        return process.stdout.read().decode()
    else:
        return'Failed parsing: ' + ' '.join('{:02x}'.format(x) for x in data)

def decode_packet(packet, magic):
    section_header = packet.read(6)
    firstbyte = magic
    new_section = True
    sections = []
    raw_subsections = []

    while len(section_header) == 6 and firstbyte == magic:
        firstbyte, same_section, subsection_length = struct.unpack('>BBL', section_header)
        subsection = packet.read(subsection_length)
        raw_subsections.append([same_section, subsection.hex()])

        if new_section:
            sections.append([subsection])
        else:
            sections[-1].append(subsection)           

        section_header = packet.read(6)
        new_section = not same_section

    decoded = []
    for section in sections:
        i = 0
        obj = {} #{"subsections": [sub.hex() for sub in section]}

        if len(section[i]) != 0:
            obj.setdefault('error', []).append("Weird, subsection {}/{} of length {} instead of {}".format(
                i, len(section), len(section[i]), 0))
        i += 1

        if len(section) == 5 and len(section[i]) == 16 and len(section[i+1]) == 0:
            obj['uid'] = section[i].hex() #struct.unpack('>BBL', section_header)
            # elif :
            #     obj.setdefault('error', []).append("Weird, subsections {}/{} and {}/{} are length {} and {} instead of 16 and 0".format(
            #         i, len(section), i+1, len(section), len(section[i]), len(section[i+1])))
            i += 2
        
        while i < len(section):
            obj.setdefault('protobufs', []).append(decode_protobuf(section[i]))
            i += 1

        decoded.append(obj)

    return decoded #{'raw_subsections': raw_subsections, 'decoded': decoded} #decoded

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

pprint(decoded)
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

# for packet in decoded:
#     for section in packet['decoded']:
#         if len(section['data']): #section['is_protobuf'] and 
#             process = subprocess.Popen(['protoc', '--decode_raw'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#             process.stdin.write(section['data'])
#             process.stdin.close()
#             ret = process.wait()
#             if ret == 0:
#                 section['data'] = process.stdout.read().decode()
#             else:
#                 section['data'] = 'Failed parsing: ' + ' '.join('{:02x}'.format(x) for x in section['data'])
            # print(protod.decode())
            # print()
        # else:
        #     print("HEX"+section['data'].hex())
        #     section['data'] = ' '.join('{:02x}'.format(x) for x in section['data'])

# pprint(decoded)
