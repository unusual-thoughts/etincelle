import socket
import struct
import uuid
import sys
import time
from threading import Thread
from datetime import datetime
from select import select
from dvlt_client import DevialetClient
from dvlt_decode import DevialetFlow
from dvlt_pool import dvlt_pool, Devialet, DevialetController
# from dvlt_service import DevialetController
from dvlt_output import print_error, print_warning, print_info, print_data, print_errordata

dvltServiceOptions = dvlt_pool.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
dvltMethodOptions = dvlt_pool.FindExtensionByName('Devialet.CallMeMaybe.dvltMethodOptions')


# Implements RpcChannel
class DevialetServer(DevialetClient, Thread):
    def __init__(self, *args, addr=socket.gethostname(), port=0, analyze=False, **kwargs):
        Thread.__init__(self)
        DevialetFlow.__init__(self, *args, phantom_port=port, **kwargs)  # Do we really need this?

        self.analyze = analyze
        self.sock = None
        # self.file = None
        self.serverId = uuid.uuid4().bytes
        self.request_queue = {}  # {requestid: (method_descriptor response_class, controller, callback)}
        # self.event_callbacks = {}  # {method_descriptor.full_name: (response_class, callback)}
        # self.blocking_reponse = None
        self.addr = addr
        self.port = port
        # self.conn = None  # Connection Service
        self.service_list = Devialet.CallMeMaybe.ServicesList()
        self.services = {}  # {id: DevialetService}
        self.srv_max_id = 0
        self.clientsocks = {}  # {(addr, port): (sock, file, is_connected)}
        self.shutdown_signal = False

    def open(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Port 0 means system-chosen port
            self.sock.bind((self.addr, self.port))
            self.addr, self.port = self.sock.getsockname()
            self.sock.listen(5)

            conn = Devialet.CallMeMaybe.Connection(self)
            # ctrl = DevialetController(conn)
            self.register_service(conn)

            # # No Callback - does a blocking RPC
            # conn_reply = self.conn.openConnection(ctrl, Devialet.CallMeMaybe.ConnectionRequest(version=1), None)
            # self.serverId = conn_reply.serverId
            # self.service_list = Devialet.CallMeMaybe.ServicesList(services=conn_reply.services)
            # # Register event callbacks for added/deleted services
            # self.conn.serviceAdded(ctrl, None, self.add_service)
            # self.conn.serviceRemoved(ctrl, None, self.remove_service)
            # self.conn.serverQuit(ctrl, None, self.close)
            print_info('Listening on port {}', self.port)
            return True
        except ConnectionRefusedError:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print_error("Can't Connect to {} on port {}, error {}",
                        self.addr, self.port, exc_obj)
            self.sock = None
            return False

    def run(self):
        # self.open()
        while not self.shutdown_signal:
            # print_info('One spin of SERVER loop...')
            socks = [s for s, f, c in self.clientsocks.values()] + [self.sock]
            readable, writable, errored = select(socks, [], [])
            if self.shutdown_signal:
                break
            # if errored:
            #     print_warning('Shutting down server on port {}', self.port)
            #     break
            # print_info('One spin of SERVER loop!')
            for s in readable:
                if s is self.sock:
                    clientsock, clientaddr = self.sock.accept()
                    clientfile = clientsock.makefile(mode='wb')
                    self.clientsocks[clientaddr] = (clientsock, clientfile, False)
                    print_info('Client {} connected to us!', clientaddr)
                else:
                    addr = [a for a, (ss, f, c) in self.clientsocks.items() if ss is s][0]
                    data = s.recv(2048)
                    # print_warning('data from {}: {}', addr, data)
                    if data:
                        print_info('Received {} on server socket', data.hex())
                    else:
                        self.close_client(addr)

    def register_service(self, srv):
        srv_id = self.srv_max_id + 1
        srv_name = srv.serviceName + '.' + uuid.uuid4().hex
        self.service_list.services.add(id=srv_id, name=srv_name)
        self.services[srv_id] = srv

        # TODO: send serviceadded event

        self.srv_max_id = srv_id

    def deregister_service(self, srv_id):
        # TODO
        pass

    def close_client(self, addr):
        sock, file, c = self.clientsocks.pop(addr)
        print_warning('Closing Connection to Client {} on port {}', addr[0], addr[1])
        sock.shutdown(2)
        sock.close()
        file.close()

    def shutdown(self):
        self.shutdown_signal = True
        for client in list(self.clientsocks.keys()):
            self.close_client(client)
        self.close()

    def close(self, arg=None):
        # if self.sock is not None:
        print_warning('Closing Server Connection on port {}', self.port)
        self.sock.shutdown(2)
        self.sock.close()
            # self.file.close()
            # self.sock = None
            # self.file = None
