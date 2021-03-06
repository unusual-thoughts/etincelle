import os
import xml.etree.ElementTree as etree
from functools import partial
from collections import deque

from dvlt_decode import DevialetManyFlows, DevialetFlow
from dvlt_output import *
import dateutil.parser


# Decode streams generated by tcpflow command eg: tcpflow -v -r file.pcapng -o dirname
# another possibility would be tshark -r file.pcapng -z follow,tcp,raw,1 -q
class TCPFlows(DevialetManyFlows):
    def __init__(self, dirname, spark_addr, phantom_addr):
        DevialetManyFlows.__init__(self)
        self.dirname = dirname
        self.spark_addr = spark_addr
        self.phantom_addr = phantom_addr
        self.bufsize = 4096

        with open(os.path.join(dirname, 'report.xml')) as xmlfile:
            tree = etree.parse(xmlfile)

            for file in tree.findall('.//fileobject'):
                filename = file.find('filename')

                if filename is not None:
                    details = file.find('tcpflow')
                    time = dateutil.parser.parse(details.attrib['startime'])

                    spark_port = -1
                    if details.attrib['src_ipn'] == self.spark_addr and details.attrib['dst_ipn'] == self.phantom_addr:
                        spark_port = int(details.attrib['srcport'])
                        phantom_port = int(details.attrib['dstport'])
                        is_incoming = False
                    elif details.attrib['src_ipn'] == self.phantom_addr and details.attrib['dst_ipn'] == self.spark_addr:
                        spark_port = int(details.attrib['dstport'])
                        phantom_port = int(details.attrib['srcport'])
                        is_incoming = True
                    if spark_port >= 0:
                        with open(os.path.join(dirname, os.path.basename(filename.text)), 'rb') as datafile:
                            print_info('Decoding {}', filename.text)
                            if (phantom_port, spark_port) in self.flows:
                                flow = self.flows[(phantom_port, spark_port)]

                                # Find flows where Spark is the RPC server
                                if flow.outgoing_sections and not flow.incoming_sections and flow.start_time > time and is_incoming:
                                    print_info('Found flow where Spark appears to be RPC server')
                                    flow.incoming_sections = flow.outgoing_sections
                                    flow.outgoing_sections = deque()
                                    is_incoming = False
                                    flow.rpc_server_is_phantom = False
                                if flow.incoming_sections and not flow.outgoing_sections and flow.start_time < time and not is_incoming:
                                    print_info('Found flow where Spark appears to be RPC server')
                                    flow.outgoing_sections = flow.incoming_sections
                                    flow.incoming_sections = deque()
                                    is_incoming = True
                                    flow.rpc_server_is_phantom = False
                            else:
                                flow = DevialetFlow(name=datafile.name, phantom_port=phantom_port, spark_port=spark_port, start_time=time)
                                self.add_flow(flow)
                            for buf in iter(partial(datafile.read, self.bufsize), b''):
                                # print_info('Partial decode')
                                flow.decode(buf, time=time, incoming=is_incoming)

    def decode_all(self):
        for (phantom_port, spark_port), flow in sorted(self.flows.items(), key=lambda x: x[1].start_time):
            flow.close()
            flow.rpc_walk()

if __name__ == '__main__':
    flows = TCPFlows('/path/to/captures/mp3streaming_tcpflow', '192.168.178.37', '192.168.178.133')
    #flows = TCPFlows('/path/to/captures/arpspoof_update', '192.168.178.87', '192.168.178.133')
    # flows = TCPFlows('/path/to/captures/boot_phantom_then_spark2', '192.168.178.66', '192.168.178.43')
    flows.decode_all()
