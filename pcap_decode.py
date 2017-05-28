from datetime import datetime
from scapy.all import *
from dvlt_decode import DevialetDecoder
from pprint import pprint

class PcapDecoder(DevialetDecoder):
    def __init__(self, filename, spark_addr, phantom_addr):
        DevialetDecoder.__init__(self)
        self.filename = filename
        self.spark_addr = spark_addr
        self.phantom_addr = phantom_addr

        capture = scapy.all.rdpcap(filename)
        self.sessions = capture[TCP].sessions()

    def packet_iter(self, session_name):
        i = 0
        for scapy_packet in self.sessions[session_name]:
            # print(scapy_packet[IP].src, self.phantom_addr)
            try:
                raw = scapy_packet[TCP].load
            except AttributeError:
                raw = b''
            packet = {
                'time': datetime.fromtimestamp(scapy_packet.time),
                'direction': 1 if scapy_packet[IP].src == self.phantom_addr else 0,
                'number': i,
                'length': len(raw),
                'merged': 1,
                'data': raw,
            }
            i += 1
            yield packet

    def get_direction(self, desc):
        direction, spark_port, phantom_port = (-1, -1, -1)
        res = re.match('^TCP {}:([0-9]+) > {}:([0-9]+)$'.format(
            self.spark_addr, self.phantom_addr), desc)
        if res is not None: # Spark to Phantom
            direction = 0
            spark_port, phantom_port = res.groups()
        else:
            res = re.match('^TCP {}:([0-9]+) > {}:([0-9]+)$'.format(
            self.phantom_addr, self.spark_addr), desc)
            if res is not None: # Phantom to Spark
                direction = 1
                phantom_port, spark_port = res.groups()
        return (direction, spark_port, phantom_port)

    def decode_sessions(self):
        grouped_streams = []
        while self.sessions:
            stream_desc, stream = self.sessions.popitem()
            direction, spark_port, phantom_port = self.get_direction(stream_desc)

            if direction != -1:
                grouped_streams.append([(stream_desc, stream)])
                for second_desc in list(self.sessions.keys()):
                    direction2, spark_port2, phantom_port2 = self.get_direction(second_desc)
                    if spark_port == spark_port2 and phantom_port == phantom_port2 and direction == 1 - direction2:
                        grouped_streams[-1].append((second_desc, self.sessions.pop(second_desc)))

        # print(self.sessions)
        # pprint(grouped_streams)
                # print(stream_desc, self.get_direction(stream_desc))

        for group in grouped_streams:
            group_name = ''
            packet_list = []
            for stream_desc, stream in group:
                group_name += ' ' + stream_desc
                packet_list += stream
            self.sessions[group_name] = packet_list

        print(self.sessions)
        session = {
            'name': self.filename,
            'captures': [{
                'name': capture,
                'port': self.sessions[capture][0].sport,
                'start_time': datetime.fromtimestamp(self.sessions[capture][0].time),
                'packets': self.decode_capture(self.packet_iter(capture))
            } for capture in self.sessions]
        }
        session['start_time'] = min(capture['start_time'] for capture in session['captures'])
        session['number_of_captures'] = len(session['captures'])

        return [session]

if __name__ == '__main__':

    decoder = PcapDecoder('../spark_mp3_streaming.pcapng', '192.168.178.37', '192.168.178.133')
    sessions = decoder.decode_sessions()
    # pprint(sessions)

    dump_file = open('pcap_decode.pickle', 'wb')
    pickle.dump(sessions, dump_file)