import sys
from datetime import datetime
from collections import deque
from dvlt_output import print_warning, print_info, print_error, print_data
from dvlt_decode import DevialetManyFlows, DevialetFlow

print_info('Loading scapy...')
from scapy.all import *


class SeqData:
    def __init__(self):
        self.seq = 0
        self.isn = 0
        self.ood = deque()


class PcapFlows(DevialetManyFlows):
    def __init__(self, filename, spark_addr, phantom_addr, decode_by_flow=False):
        DevialetManyFlows.__init__(self)
        self.filename = filename
        self.spark_addr = spark_addr
        self.phantom_addr = phantom_addr
        self.decode_by_flow = decode_by_flow

        # print_info('Loading file...')
        # capture = scapy.all.rdpcap(filename)
        # self.sessions = capture[TCP].sessions()
        with PcapReader(filename) as pcap_reader:
            for packet in pcap_reader:
                # print(packet)
                if packet.haslayer(TCP):
            # for packet in capture[TCP]:
                    time = datetime.fromtimestamp(packet.time)
                    # print(packet)
                    # if packet.
                    spark_port = -1
                    if packet[IP].src == self.spark_addr and packet[IP].dst == self.phantom_addr:
                        spark_port = packet[TCP].sport
                        phantom_port = packet[TCP].dport
                        phantom_to_spark = False
                    elif packet[IP].src == self.phantom_addr and packet[IP].dst == self.spark_addr:
                        spark_port = packet[TCP].dport
                        phantom_port = packet[TCP].sport
                        phantom_to_spark = True
                    if spark_port >= 0:
                        if (phantom_port, spark_port) in self.flows:
                            flow = self.flows[(phantom_port, spark_port)]
                        else:
                            print_warning('New Flow phantom {}, spark {}, time {}', phantom_port, spark_port, time)
                            flow = DevialetFlow(name='phantom {}, spark {}'.format(phantom_port, spark_port),
                                                phantom_port=phantom_port, spark_port=spark_port, start_time=time)
                            flow.phantom = SeqData()
                            flow.spark = SeqData()
                            # if first packet is from phantom to spark, rpc server is probably spark
                            if phantom_to_spark:
                                print_info('Found flow where Spark appears to be RPC server: phantom {}, spark {}',
                                           phantom_port, spark_port)
                                flow.rpc_server_is_phantom = False
                            self.add_flow(flow)
                        # Reverse direction if rpc server is Spark
                        srv_to_client = phantom_to_spark ^ (not flow.rpc_server_is_phantom)
                        tcplen = packet[IP].len - packet[IP].ihl*4 - packet[TCP].dataofs*4
                        sending = (flow.phantom if phantom_to_spark else flow.spark)
                        receiving = (flow.spark if phantom_to_spark else flow.phantom)

                        if 'S' in packet.sprintf('%TCP.flags%') or 'F' in packet.sprintf('%TCP.flags%'):
                            # if SYN, synchronize sequence numbers
                            print_info('Sp {:6d} {} Ph {:6d} Len {:5d} Seq {:12d} Ack {:12d} Diff {:12d} Flags {}',
                                       spark_port, '<- ' if phantom_to_spark else ' ->', phantom_port, tcplen,
                                       packet[TCP].seq - sending.isn,
                                       packet[TCP].ack - receiving.isn,
                                       0, packet.sprintf('%TCP.flags%'),
                                       color='red')
                            sending.isn = packet[TCP].seq
                            sending.seq = packet[TCP].seq + 1
                            if sending.ood:
                                print_error('{} remaining in {} OOD queue', len(sending.ood),
                                            'Phantom' if phantom_to_spark else 'Spark')
                                sending.ood.clear()
                        else:
                            # print(packet[TCP].load[:12].hex())
                            diff = packet[TCP].seq - sending.seq
                            print_info('Sp {:6d} {} Ph {:6d} Len {:5d} Seq {:12d} Ack {:12d} Diff {:12d} Flags {}',
                                       spark_port, '<- ' if phantom_to_spark else ' ->', phantom_port, tcplen,
                                       packet[TCP].seq - sending.isn,
                                       packet[TCP].ack - receiving.isn,
                                       diff, packet.sprintf('%TCP.flags%'),
                                       color='blue' if phantom_to_spark else 'green',
                                       reverse=(diff != 0))
                            if diff == 0:
                                sending.seq = packet[TCP].seq + tcplen
                                if tcplen:
                                    flow.decode(packet[TCP].load[:tcplen], time=time, incoming=srv_to_client)
                                    if not self.decode_by_flow:
                                        flow.rpc_walk(verbose=False)
                                for p in list(sending.ood):
                                    l = p[IP].len - p[IP].ihl*4 - p[TCP].dataofs*4
                                    d = p[TCP].seq - sending.seq
                                    if d == 0:
                                        sending.seq = p[TCP].seq + l
                                        if l:
                                            flow.decode(p[TCP].load[:l], time=time, incoming=srv_to_client)
                                            if not self.decode_by_flow:
                                                flow.rpc_walk(verbose=False)
                                        sending.ood.remove(p)
                                        print_info('Sp {:6d} {} Ph {:6d} Len {:5d} Seq {:12d} Ack {:12d} Diff {:12d} Flags {:3} Reordered',
                                                   spark_port, '<- ' if phantom_to_spark else ' ->', phantom_port, l,
                                                   p[TCP].seq - sending.isn, p[TCP].ack - receiving.isn,
                                                   d, p.sprintf('%TCP.flags%'), color='magenta')
                                    else:
                                        # print_warning('{:6d} {} Ph {:6d} Len {:5d} Seq {:12d} Ack {:12d} Diff {:12d} Flags {:3} OOD',
                                        #               spark_port, '<- ' if phantom_to_spark else ' ->', phantom_port, l,
                                        #               p[TCP].seq - sending.isn, p[TCP].ack - receiving.isn,
                                        #               d, p.sprintf('%TCP.flags%'))
                                        pass
                            else:
                                sending.ood.append(packet)


if __name__ == '__main__':
    if len(sys.argv) > 3:
        filename, spark_addr, phantom_addr = sys.argv[1:4]
        flows = PcapFlows(filename, spark_addr, phantom_addr, decode_by_flow=False)
        if flows.decode_by_flow:
            for flow in sorted([f for f in flows.flows.values()], key=lambda x: x.start_time):
                flow.rpc_walk(verbose=False)
        print_data('Pcap Flow stats', sorted(
            [{
                # 'phantom port': pp,
                # 'spark port': sp,
                'ports': f.name,
                'start time': str(f.start_time),
                'incoming bytes': len(f.incoming_buf.getbuffer()),
                'outgoing bytes': len(f.outgoing_buf.getbuffer())
            } for (pp, sp), f in flows.flows.items()],
            key=lambda x: x['start time'])
        )
    else:
        print_error('Usage: pcap_decode.py [file.pcapng] [spark_addr] [phantom_addr]')
