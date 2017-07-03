import socket
import struct
import uuid
from select import select
from dvlt_output import print_info, print_data, print_warning
from threading import Thread


# Broadcast receiver/sender - Discovery protocol
class DevialetDiscovery(Thread):
    def __init__(self, queue, serial=uuid.uuid4().bytes, callback=None, port=24242, period=2, advertise=False):
        Thread.__init__(self)
        self.serial = serial
        self.port = port
        self.period = period
        self.advertise = advertise
        self.callback = callback
        self.queue = queue

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('', self.port))

        self.database = {}  # {serial: addr}
        # MCAST_GRP = '224.1.1.1'
        # mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def run(self):
        print_info('Searching for Devialet Device...')
        while True:
            ready = select([self.sock], [], [], self.period)
            if self.advertise:
                self.sock.sendto(b'DVL\x01HERE\x00\x00\x00' + bytes([len(self.serial)]) + self.serial,
                                ('255.255.255.255', self.port))
            if ready[0]:
                data, (sender_addr, sender_port) = self.sock.recvfrom(1024)

                if len(data) >= 12:
                    magic, serial_len = struct.unpack('>8sI', data[:12])
                    serial = data[12:]
                    if magic == b'DVL\x01HERE' and len(data) == 12 + serial_len:
                        if serial not in self.database or self.database[serial] != sender_addr:
                            self.database[serial] = sender_addr
                            print_info('Found Devialet Device with serial {} at address {}'.format(serial, sender_addr))
                            self.queue.put((serial, sender_addr))
                            if self.callback is not None:
                                self.callback(serial, sender_addr)
                    else:
                        print_warning('Unknown data: {}', data.hex())
                elif data == b'DVL\x01WHO?':
                    print_info('Got Discovery request')
                else:
                    print_warning('Discovery message too short: {}', data.hex())

    def start_advertising(self):
        self.advertise = True

    def stop_advertising(self):
        self.advertise = False
