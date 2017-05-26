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
    raw_fields = []

    while len(section_header) == 6 and firstbyte == magic:
        firstbyte, same_section, field_length = struct.unpack('>BBL', section_header)
        field = packet.read(field_length)
        raw_fields.append([same_section, field.hex()])

        if new_section:
            sections.append([field])
        else:
            sections[-1].append(field)           

        section_header = packet.read(6)
        # when second byte of section header is 0, next field is part of new section
        new_section = not same_section

    rest = packet.read()
    if len(section_header) != 0 or firstbyte != magic or rest:
        print("Found garbage at end of packet: magic={} header={} rest={}".format(magic, section_header.hex(), rest.hex()))

    decoded = []
    for section in sections:
        i = 0
        obj = {} #{"fields": [sub.hex() for sub in section]}

        # Delimiter, always empty
        if len(section[i]) != 0:
            obj.setdefault('error', []).append("Weird, field {}/{} of length {} instead of {}".format(
                i, len(section), len(section[i]), 0))
        i += 1

        # Extra field (+ delimiter) that doesnt decode into protobuf, some kind of uid?
        if len(section) == 5 and len(section[i]) == 16 and len(section[i+1]) == 0:
            obj['uid'] = section[i].hex()
            i += 2
        
        # Remaining fields should all be protobufs
        while i < len(section):
            obj.setdefault('protobufs', []).append(decode_protobuf(section[i]))
            i += 1

        decoded.append(obj)

    return decoded #{'raw_fields': raw_fields, 'decoded': decoded} #decoded

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
        content = file.read(length)

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

        header = file.read(16)

decoded = [ {
    "time": packet["time"],
    "direction": packet["direction"],
    "magic": packet["data"][0],
    "decoded": decode_packet(BytesIO(packet["data"]), packet["data"][0])
} for packet in packets ]

pprint(decoded)