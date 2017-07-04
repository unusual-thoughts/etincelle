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
class DevialetServer(Thread):
    def __init__(self, *args, addr=socket.gethostname(), port=0, analyze=False, **kwargs):
        Thread.__init__(self)
        # DevialetFlow.__init__(self, *args, phantom_port=port, **kwargs)  # Do we really need this?

        self.analyze = analyze
        self.sock = None
        # self.file = None
        self.serverId = uuid.uuid4().bytes
        self.request_queue = {}  # {requestid: (method_descriptor response_class, controller, callback)}
        self.request_callbacks = {}  # {method_descriptor.full_name: (response_class, callback)}
        # self.blocking_reponse = None
        self.addr = addr
        self.port = port
        # self.conn = None  # Connection Service
        self.service_list = Devialet.CallMeMaybe.ServicesList()
        self.services = {}  # {id: DevialetService}
        self.srv_max_id = -1
        self.clientsocks = {}  # {(addr, port): (sock, file, is_connected)}
        self.shutdown_signal = False
        self.rpc_server_is_phantom = False
        self.flows = {}  # {(addr, port): flow}

    # Callback
    def open_connection(self, conn_request):
        print_info('Client trying to open connection, ver {}', conn_request.version)
        return Devialet.CallMeMaybe.ConnectionReply(
            serverId=self.serverId,
            services=self.service_list.services)

    def open(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Port 0 means system-chosen port
            self.sock.bind((self.addr, self.port))
            self.addr, self.port = self.sock.getsockname()
            self.sock.listen(5)

            conn = Devialet.CallMeMaybe.Connection(self)
            self.register_service(conn)
            ctrl = DevialetController(conn)
            # Register callback for client connection requests
            conn.openConnection(ctrl, None, self.open_connection)

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
        timeout = 2
        while not self.shutdown_signal:
            # print_info('One spin of SERVER loop...')
            socks = [s for s, f, c in self.clientsocks.values()] + [self.sock]
            readable, writable, errored = select(socks, [], [], timeout)
            if self.shutdown_signal:
                break
            # if errored:
            #     print_warning('Shutting down server on port {}', self.port)
            #     break
            # print_info('One spin of SERVER loop!')
            for s in readable:
                if s is self.sock:
                    clientsock, (clientaddr, clientport) = self.sock.accept()
                    if self.shutdown_signal:
                        break
                    clientfile = clientsock.makefile(mode='wb')
                    self.clientsocks[(clientaddr, clientport)] = (clientsock, clientfile, False)
                    self.flows[(clientaddr, clientport)] = DevialetFlow(
                        name='{}:{}'.format(clientaddr, clientport),
                        spark_port=self.port, phantom_port=clientport)
                    print_info('Client {} on port {} connected to us!', clientaddr, clientport)
                else:
                    addrport = [a for a, (ss, f, c) in self.clientsocks.items() if ss is s][0]
                    data = s.recv(2048)
                    # print_warning('data from {}: {}', addr, data)
                    if data:
                        print_info('Received {} on client socket {}', data.hex(), addrport)
                        self.flows[addrport].decode(data, incoming=False)
                        self.find_requests(addrport)
                    else:
                        self.close_client(addrport)

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

    def close_client(self, addrport):
        sock, file, c = self.clientsocks.pop(addrport)
        print_warning('Closing Connection to Client {} on port {}', addrport[0], addrport[1])
        sock.shutdown(2)
        sock.close()
        file.close()

    def shutdown(self):
        self.shutdown_signal = True
        for client in list(self.clientsocks.keys()):
            # Close Client sockets
            self.close_client(client)
            # Close Flow objects (buffers)
            self.flows[client].close()
        # Close server socket
        self.close()

    def close(self, arg=None):
        # if self.sock is not None:
        print_warning('Closing Server Connection on port {}', self.port)
        self.sock.shutdown(2)
        self.sock.close()
            # self.file.close()
            # self.sock = None
            # self.file = None

    def write_field_to_file(self, file, raw_field, firstbyte, same_section):
        field_header = struct.pack('>BBL', firstbyte, same_section, len(raw_field))
        field = field_header + raw_field
        file.write(field)
        if self.analyze:
            # Place data in queue for rpc_walk to see
            self.decode(raw=field, incoming=True, time=datetime.now())

    def write_event_to_addr(self, addrport, raw_cmmevent, raw_event):
        firstbyte = 0xC3
        sock, file, is_connected = self.clientsocks[addrport]

        # if is_connected:
        self.write_field_to_file(file, b'', firstbyte, 1)
        self.write_field_to_file(file, self.serverId, firstbyte, 1)
        self.write_field_to_file(file, b'', firstbyte, 1)
        self.write_field_to_file(file, raw_cmmevent, firstbyte, 1)
        self.write_field_to_file(file, raw_event, firstbyte, 0)
        file.flush()

    def write_response_to_addr(self, addrport, raw_cmmreply, raw_reponse):
        firstbyte = 0xC2
        sock, file, is_connected = self.clientsocks[addrport]

        # if is_connected:
        self.write_field_to_file(file, b'', firstbyte, 1)
        self.write_field_to_file(file, raw_cmmreply, firstbyte, 1)
        self.write_field_to_file(file, raw_reponse, firstbyte, 0)
        file.flush()

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        # Handle events and requests differently: events broadcast to every client;
        # Requests just register callback for later use
        # (Opposite of DevialetClient)

        if method_descriptor.GetOptions().Extensions[dvltMethodOptions].isNotification:
            # For events, broadcast immediately, don't use callback
            serviceId = rpc_controller.parent_service.service_id if hasattr(
                rpc_controller.parent_service, 'service_id') else self.find_service_id(method_descriptor.containing_service)
            # Special PropertyUpdate event: how do we get the property id???
            typeId, subTypeId = (1, request.id) if method_descriptor.name == 'propertyUpdate' else (0, method_descriptor.index)
            cmm_event = Devialet.CallMeMaybe.Event(
                serverId=self.serverId,
                serviceId=serviceId,
                type=typeId, subTypeId=subTypeId)

            for addrport in self.clientsocks.keys():
                self.write_event_to_addr(cmm_event.SerializeToString(), request.SerializeToString())
        else:
            # For request methods, only register callback, don't send anything
            self.request_callbacks[method_descriptor.full_name] = (
                dvlt_pool.messages[method_descriptor.input_type.full_name], done)

    def find_requests(self, addrport):
        for outgoing_section in self.flows[addrport].outgoing_sections:
            # incoming_section = self.incoming_sections.popleft()
            outgoing_section = outgoing_section.raw_protobufs

            print_warning("Found Request")
            # try:
            req = Devialet.CallMeMaybe.Request.FromString(outgoing_section[0])
            if req.serverId != self.serverId:
                print_warning('Oops, this request is not for us (unless this is inital conenction request): we are {}, sent to {}',
                              self.serverId.hex(), req.serverId.hex())
            try:
                srv = self.services[req.serviceId]
                if req.type == 0:
                    try:
                        method_desc = srv.methods_by_id[req.subTypeId]
                        if method_desc.full_name in self.request_callbacks:
                            (request_class, callback) = self.request_callbacks[method_desc.full_name]
                            response = callback(request_class.FromString(outgoing_section[1]))
                            rep = Devialet.CallMeMaybe.Reply(
                                serverId=self.serverId,
                                serviceId=req.serviceId,
                                requestId=req.requestId,
                                type=0,
                                subTypeId=req.subTypeId,
                                errorCode=0,
                                isMultipart=False)
                            self.write_response_to_addr(addrport, rep.SerializeToString(), response.SerializeToString())
                        else:
                            print_error('Unhandled method {} from {}', method_desc.full_name, addrport)

                    except KeyError:
                        print_errordata('Method id {} not in service method dict:'.format(req.subTypeId),
                                        {k: v.full_name for (k, v) in srv.methods_by_id.items()})
                elif req.type == 1:
                    # PropertySet special request
                    # TODO
                    print_error('Unhandled propertyset')
                    pass
                else:
                    print_error('Unknown request type {}', req.type)
            except KeyError:
                print_error('Service ID {} not in list {}', req.serviceId, ' '.join(str(self.service_list.services).split('\n')))

        self.flows[addrport].outgoing_sections.clear()
