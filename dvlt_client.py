import socket
import struct
import uuid
import re
import sys
import time
import google.protobuf.service
from datetime import datetime
from threading import Thread
from select import select
from dvlt_decode import DevialetFlow
from dvlt_pool import dvlt_pool, Devialet, DevialetController
# from dvlt_service import DevialetController
from dvlt_output import print_error, print_warning, print_info, print_data, print_errordata

dvltServiceOptions = dvlt_pool.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
dvltMethodOptions = dvlt_pool.FindExtensionByName('Devialet.CallMeMaybe.dvltMethodOptions')


# Implements RpcChannel
class DevialetClient(DevialetFlow, Thread):
    def __init__(self, *args, addr='127.0.0.1', port=24242, analyze=False, **kwargs):
        Thread.__init__(self)
        DevialetFlow.__init__(self, *args, phantom_port=port, **kwargs)
        self.analyze = analyze
        self.sock = None
        self.file = None
        self.serverId = b'\x00'*16
        self.request_queue = {}  # {requestid: (method_descriptor response_class, controller, callback)}
        self.event_callbacks = {}  # {method_descriptor.full_name: (response_class, callback)}
        self.blocking_reponse = None
        self.addr = addr
        self.port = port
        self.conn = None  # Connection Service
        self.service_list = Devialet.CallMeMaybe.ServicesList()
        self.shutdown_signal = False

    def open(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.addr, self.port))
            self.file = self.sock.makefile(mode='wb')

            self.conn = Devialet.CallMeMaybe.Connection(self)
            ctrl = DevialetController(self.conn)
            # No Callback - does a blocking RPC
            conn_reply = self.conn.openConnection(ctrl, Devialet.CallMeMaybe.ConnectionRequest(version=1), None)
            self.serverId = conn_reply.serverId
            self.service_list = Devialet.CallMeMaybe.ServicesList(services=conn_reply.services)
            # Register event callbacks for added/deleted services
            self.conn.serviceAdded(ctrl, None, self.add_service)
            self.conn.serviceRemoved(ctrl, None, self.remove_service)
            self.conn.serverQuit(ctrl, None, self.close)
            print_info('Opened connection to {} on port {}', self.addr, self.port)
            return True
        except ConnectionRefusedError:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print_error("Can't Connect to {} on port {}, error {}",
                        self.addr, self.port, exc_obj)
            self.sock = None
            return False

    def close(self, arg=None):
        if self.sock is not None:
            print_warning('Closing Connection to {} on port {}', self.addr, self.port)
            self.sock.shutdown(2)
            self.sock.close()
            self.file.close()
            self.sock = None
            self.file = None

    def shutdown(self):
        self.shutdown_signal = True
        self.close()
        DevialetFlow.close(self)

    def reconnect(self, timeout=3):
        count = 0
        while not self.open() and count < timeout*10:
            time.sleep(.1)
            count += 1
        if count == timeout*10:
            print_error('Could not reconnect on port {}', self.port)

    def receive(self, timeout=None):
        try:
            if timeout is not None:
                ready = select([self.sock], [], [], timeout)
                if self.shutdown_signal:
                    return False
                if ready[0]:
                    data = self.sock.recv(2048)
                else:
                    print_warning('Timed out on port {}', self.port)
                    return False
            else:
                data = self.sock.recv(2048)
            if self.shutdown_signal:
                return False
            if self.analyze:
                print_data("Raw response", data.hex())
            if not data:
                print_error("Got 0 bytes from socket")
                # self.close()
                return False
            else:
                self.decode(data)
                if self.analyze:
                    self.rpc_walk(consume_incoming=False, verbose=False)
                self.find_responses()
                return True
        except ConnectionResetError:
            print_error('Server hung up during receive')
            return False

    def keep_receiving(self, timeout=None):
        while not self.shutdown_signal and self.receive(timeout):
            pass
        # self.close()

    def run(self):
        self.keep_receiving()

    def add_service(self, service):
        print_info("New Service added: {}", service.name)
        self.service_list.services.extend([service])

    def remove_service(self, service):
        print_info("Service {} removed", service.name)
        self.service_list.services.remove(service)

    def write_field(self, raw_field, firstbyte, same_section):
        field_header = struct.pack('>BBL', firstbyte, same_section, len(raw_field))
        field = field_header + raw_field
        self.file.write(field)
        if self.analyze:
            # Place outgoing data in queue for rpc_walk to see
            self.decode(raw=field, incoming=False, time=datetime.now())

    def write_rpc(self, raw_request, raw_input):
        firstbyte = 0xC2
        self.write_field(b'', firstbyte, 1)
        self.write_field(raw_request, firstbyte, 1)
        self.write_field(raw_input, firstbyte, 0)
        self.file.flush()

    def find_service_id(self, service_desc):
        lowercase_name = service_desc.GetOptions().Extensions[dvltServiceOptions].serviceName
        matching_services = [service.id for service in self.service_list.services if '.'.join(service.name.split('.')[:-1]) == lowercase_name]
        try:
            # Service list not yet populated
            if lowercase_name == "com.devialet.callmemaybe.connection" and not self.service_list.services:
                return 0
            return matching_services[0]
        except IndexError:
            print_error('Service name {} not in list {}', lowercase_name, ' '.join(str(self.service_list.services).split('\n')))
        return 0

    def unblock_call(self, response):
        self.blocking_response = response

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        # For event methods, only register callback, don't send anything
        if method_descriptor.GetOptions().Extensions[dvltMethodOptions].isNotification:
            # For events, response class is always empty, request class is the actual class of the event
            self.event_callbacks[method_descriptor.full_name] = (
                dvlt_pool.messages[method_descriptor.input_type.full_name], done)
        else:
            reqUUID = uuid.uuid4().bytes
            serviceId = rpc_controller.parent_service.service_id if hasattr(
                rpc_controller.parent_service, 'service_id') else self.find_service_id(method_descriptor.containing_service)
            typeId, subTypeId = (1, 0xFFFFFFFF) if method_descriptor.name == 'propertyGet' else (0, method_descriptor.index)
            cmm_request = Devialet.CallMeMaybe.Request(
                serverId=self.serverId,
                serviceId=serviceId,
                requestId=reqUUID,
                type=typeId, subTypeId=subTypeId)
            self.request_queue[reqUUID] = (method_descriptor, response_class, rpc_controller, done if done else self.unblock_call)
            self.write_rpc(cmm_request.SerializeToString(), request.SerializeToString())

            if done is None:
                # Blocking call
                self.blocking_response = None
                while self.blocking_response is None and self.receive():
                    pass
                if self.blocking_response is None:
                    self.close()
                    print_error("Server hung up before response")
                return self.blocking_response

    def CallUnknownMethod(self, serviceId, subTypeId, request, done, typeId=0):
        print_info('Calling unknown method #{} from service #{} on port {}', subTypeId, serviceId, self.port)
        reqUUID = uuid.uuid4().bytes
        cmm_request = Devialet.CallMeMaybe.Request(
            serverId=self.serverId,
            serviceId=serviceId,
            requestId=reqUUID, type=typeId,
            subTypeId=subTypeId)
        self.request_queue[reqUUID] = (None, None, DevialetController(self.conn), done if done else self.unblock_call)
        self.write_rpc(cmm_request.SerializeToString(), request.SerializeToString())

        if done is None:
            # Blocking call
            self.blocking_response = None
            while self.blocking_response is None and self.receive():
                # print_info("Waiting for response on unknown method (serviceId {}, subTypeId {})",
                #            serviceId, subTypeId)
                # time.sleep(1)
                pass
            if self.blocking_response is None:
                self.close()
                print_error("Server hung up before response")
            return self.blocking_response

    def find_responses(self):
        for i in range(len(self.incoming_sections)):
            incoming_section = self.incoming_sections.popleft()
            incoming_pb = incoming_section.raw_protobufs

            if incoming_section.magic == 0xC3:
                print_warning("Found Event")
                # try:
                evt = Devialet.CallMeMaybe.Event.FromString(incoming_pb[0])
                service_name = self.find_service(evt)

                method, input_pb, outputs_pb = dvlt_pool.process_rpc(service_name, evt, incoming_pb[1], incoming_pb[1:], is_event=True)
                try:
                    (response_class, callback) = self.event_callbacks[method.full_name]
                    if evt.type == 1:
                        # PropertyUpdate special event
                        callback(evt.subTypeId, incoming_pb[1])
                    else:
                        callback(response_class.FromString(incoming_pb[1]))
                except KeyError:
                    print_error('Unhandled event {}', method.full_name)
                    print_errordata('Registered Callbacks', self.event_callbacks)
                except AttributeError:  # method can be none eg when service name not in db
                    pass

                if incoming_section.uid != self.serverId:
                    print_error('Oops, event from different server Id ?!')
                # except IndexError:
                #     print_error('not enough incoming protos for event ({}) < 2', len(incoming_pb))

            else:
                try:
                    rep = Devialet.CallMeMaybe.Reply.FromString(incoming_pb[0])

                    method_descriptor, response_class, controller, callback = self.request_queue.pop(rep.requestId)

                    if rep.errorCode != 0:
                        # print_warning("Got error code: {} ({})", controller.parent_service.get_error(rep.errorCode), rep.errorCode)
                        controller.SetFailed(rep.errorCode)
                        # use errorEnumName, controller...

                    # None is used for unknown method calls
                    if response_class is not None:
                        # PropertyGet special "method"
                        if rep.subTypeId == 0xFFFFFFFF and rep.type == 1:
                            # response = {}
                            # for i, raw in enumerate(incoming_pb[1:]):
                            #     name, prop = dvlt_pool.get_property(method_descriptor.containing_service, i, raw)
                            #     response[name] = prop
                            response = incoming_pb[1:]
                        else:
                            response = response_class.FromString(incoming_pb[1])
                        # print_data("Found Response", response)
                        callback(response)
                    else:
                        # print_data('Response with unknown message type:',
                        #            dvlt_pool.heuristic_search(incoming_pb[1]))
                        if rep.subTypeId == 0xFFFFFFFF and rep.type == 1:
                            callback([dvlt_pool.heuristic_search(x) for x in incoming_pb[1:]])
                        else:
                            callback(dvlt_pool.heuristic_search(incoming_pb[1]))

                    if not rep.isMultipart and len(incoming_pb) > 2:
                        print_warning('we got more incoming protobufs than we should have, not Multipart')

                    if len(incoming_pb) < 2:
                        print_error('we got less than 2 incoming protobufs')

                    # print_info('out_time:{} in_time:{} req:{}/{}/{:>10d}/{:>12d}, rep:{}/{}/{:>10d}/{:>12d} {}{}{}',
                    #            outgoing_section.time, incoming_section.time,
                    #            req.requestId[:4].hex(), req.type, req.subTypeId, req.serviceId,
                    #            rep.requestId[:4].hex(), rep.type, rep.subTypeId, rep.serviceId,
                    #            'M' if rep.isMultipart else ' ',
                    #            ' ' if method.name == 'ping' else 'C' if method.name == 'openConnection' else '.',
                    #            '<' if rep.requestId != req.requestId else ' ')
                except KeyError:
                    print_error('Response to unknown request id {}', rep.requestId.hex())
                    print_errordata('Request queue', self.request_queue)
                # except Exception as e:
                #     print_error('Unexpected {} {}', type(e), e)


class WhatsUpClient(DevialetClient):
    def __init__(self, *args, **kwargs):
        DevialetClient.__init__(self, *args, **kwargs)
        self.wu_service_list = Devialet.WhatsUp.WhatsUpServicesList()
        self.reg = None
        self.connections = {self.port: self}
        self.services_by_port = {}
        self.ports_by_service = {}
        self.discovered_services = {(self.port, "com.devialet.whatsup.registry")}

    def open(self):
        DevialetClient.open(self)
        self.reg = Devialet.WhatsUp.Registry(self)
        wu_ctrl = DevialetController(self.reg)
        # self.reg.getNetworkConfiguration(wu_ctrl, Devialet.CallMeMaybe.Empty(), callback_test)
        self.reg.listServices(wu_ctrl, Devialet.CallMeMaybe.Empty(), self.update_wu_services)
        self.reg.servicesAdded(wu_ctrl, None, self.add_wu_services)
        self.reg.servicesUpdated(wu_ctrl, None, self.update_wu_services)
        self.reg.servicesRemoved(wu_ctrl, None, self.remove_wu_services)
        self.reg.watch_properties()
        # self.reg.listServices(wu_ctrl, Devialet.CallMeMaybe.Empty(), self.service_discovery)

    def add_wu_services(self, wu_services):
        self.wu_service_list.services.extend(wu_services.services)
        for wu_service in wu_services.services:
            m = re.match('tcp://127.0.0.1:([0-9]+)', wu_service.endpoint)
            truncated_name = '.'.join(wu_service.name.split('.')[:-1])
            if m is not None:
                port = int(m.groups()[0])
                self.services_by_port.setdefault(port, []).append(truncated_name)
                self.ports_by_service.setdefault(truncated_name, []).append(port)
        print_info("New WhatsUp services added: {}", wu_services)
        # self.service_discovery()

    def remove_wu_services(self, wu_removal):
        for srv in wu_removal.services:
            try:
                self.wu_service_list.services.remove(srv)
                m = re.match('tcp://127.0.0.1:([0-9]+)', srv.endpoint)
                truncated_name = '.'.join(srv.name.split('.')[:-1])
                if m is not None:
                    port = int(m.groups()[0])
                    self.services_by_port[port].remove(truncated_name)
                    self.ports_by_service[truncated_name].remove(port)
                    if not self.services_by_port[port]:
                        self.services_by_port.pop(port)
                    if not self.ports_by_service[truncated_name]:
                        self.ports_by_service.pop(truncated_name)
                print_info('WhatsUp service "{}" removed', srv.name)
            except ValueError:
                print_errordata('WhatsUp service could not be removed', srv)
                print_errordata('From list', self.wu_service_list)

    def update_wu_services(self, wu_update):
        self.wu_service_list = Devialet.WhatsUp.WhatsUpServicesList(services=wu_update.services)
        self.services_by_port = {}
        self.ports_by_service = {}
        for wu_service in wu_update.services:
            m = re.match('tcp://127.0.0.1:([0-9]+)', wu_service.endpoint)
            truncated_name = '.'.join(wu_service.name.split('.')[:-1])
            if m is not None:
                port = int(m.groups()[0])
                self.services_by_port.setdefault(port, []).append(truncated_name)
                self.ports_by_service.setdefault(truncated_name, []).append(port)
        print_data("WhatsUp services updated", wu_update)
        # self.service_discovery()

    def connect_to_service(self, service_name, port=None):
        pass

    def service_discovery(self):
                # if truncated_name not in dvlt_pool.service_by_name:
                #     ports_by_unknown_service.setdefault(truncated_name, []).append(port)

        # print_data("Services by port", services_by_port)
        # print_data("Ports by Service", ports_by_service)
        # print_data("Ports by (Unknown) Service", ports_by_unknown_service)

        for port, services in self.services_by_port.items():
            # if [0 for srvname in services if srvname not in dvlt_pool.service_by_name]:
            # for service in services:
            #     if srvname not in dvlt_pool.service_by_name:
            if port not in self.connections:
                new_conn = DevialetClient(name='Port ' + str(port), addr=self.addr, port=port, start_time=datetime.now())
                new_conn.open()
                self.connections[port] = new_conn

                # Connect to unknown service
                for service in new_conn.service_list.services:
                    # Reopen if connection failed
                    if new_conn.sock is None:
                        res = new_conn.reconnect()
                        if not res:
                            break
                    truncated_name = '.'.join(service.name.replace('playthatfunkymusic', 'toomanyflows').split('.')[:-1])
                    while truncated_name not in dvlt_pool.service_by_name and truncated_name.endswith('-0'):
                        truncated_name = '.'.join(truncated_name.split('.')[:-1])
                        print_warning('truncating {} to {}', '.'.join(service.name.split('.')[:-1]), truncated_name)
                    # if truncated_name not in dvlt_pool.service_by_name:  # and truncated_name.endswith('-0'):
                    # if (port, truncated_name) not in self.discovered_services and truncated_name not in dvlt_pool.service_by_name:
                        # print_info('Testing 10 methods from service {}', service.name)
                        # for subTypeId in range(10):
                        #     result = new_conn.CallUnknownMethod(service.id, subTypeId, Devialet.CallMeMaybe.Empty(), None)
                        #     print_data("Response from method id {} from service {}".format(subTypeId, service.name),
                        #                result)
                        #     if result is None:
                        #         break
                    if (port, truncated_name) not in self.discovered_services:
                        if truncated_name in dvlt_pool.service_by_name:
                            srv = dvlt_pool.service_by_name[truncated_name]._concrete_class(new_conn)
                            srv.watch_properties(service_id=service.id, service_name=service.name)
                            # srv.service_id = service.id
                            # srv.service_name_unique = service.name
                            # srv.propertyGet(DevialetController(srv), Devialet.CallMeMaybe.Empty(), srv.set_properties)
                            # new_conn.keep_receiving(timeout=2)
                        else:
                            result = new_conn.CallUnknownMethod(service.id, 0xFFFFFFFF, Devialet.CallMeMaybe.Empty(), None, typeId=1)
                            print_data("Unknown properties from service {}".format(service.name),
                                       result)
                            pass
                # new_conn.keep_receiving(timeout=2)
                new_conn.close()
                self.connections.pop(port)
                # except ConnectionRefusedError:
                #     exc_type, exc_obj, exc_tb = sys.exc_info()
                #     print_error("Can't Connect to {} on port {}, open connections: {}, line {}, error {}",
                #         self.addr, port, sorted(list(self.connections.keys())), exc_tb.tb_lineno, exc_obj)
                    # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    # print(exc_type, fname, exc_tb.tb_lineno)
