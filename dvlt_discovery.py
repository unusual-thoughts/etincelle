import socket
import struct
import uuid
import time
import re
from datetime import datetime
from select import select
from dvlt_decode import DevialetFlow
from dvlt_pool import dvlt_pool, Devialet
from dvlt_output import *

from google.protobuf.service import RpcController

dvltServiceOptions = dvlt_pool.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')

class DevialetConnection(DevialetFlow):
    def __init__(self, *args, addr='127.0.0.1', port=24242, analyze=False, **kwargs):
        DevialetFlow.__init__(self, *args, phantom_port=port, **kwargs)
        self.analyze = analyze
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((addr, port))
        self.file = self.sock.makefile(mode='wb')
        self.serverId = b'\x00'*16
        self.request_queue = {}  # {requestid: (method_descriptor response_class, controller, callback)}
        self.blocking_reponse = None
        self.addr = addr
        self.port = port

    def close(self):
        # self.sock.shutdown()
        self.sock.close()

    def update_services(self, conn_reply):
        self.serverId = conn_reply.serverId
        self.service_list = conn_reply.services

    def write_field(self, raw_field, firstbyte, same_section):
        field_header = struct.pack('>BBL', firstbyte, same_section, len(raw_field))
        field = field_header + raw_field
        self.file.write(field)
        if self.analyze:
            # Place outgoing data in queue for rpc_walk to see
            self.decode(raw=field, incoming=False, time=datetime.now())

    def write_rpc(self, raw_request, raw_input, is_event=False):
        firstbyte = 0xC3 if is_event else 0xC2

        self.write_field(b'', firstbyte, 1)
        self.write_field(raw_request, firstbyte, 1)
        self.write_field(raw_input, firstbyte, 0)
        self.file.flush()

    def find_service_id(self, service_desc):
        lowercase_name = service_desc.GetOptions().Extensions[dvltServiceOptions].serviceName
        matching_services = [service.id for service in self.service_list if '.'.join(service.name.split('.')[:-1]) == lowercase_name]
        try:
            # Service list not yet populated
            if lowercase_name == "com.devialet.callmemaybe.connection" and not self.service_list:
                return 0
            return matching_services[0]
        except IndexError:
            print_error('Service name {} not in list {}', lowercase_name, ' '.join(str(self.service_list).split('\n')))
        return 0

    def unblock_call(self, response):
        self.blocking_response = response

    def receive(self):
        data = self.sock.recv(2048)
        if self.analyze:
            print_data("Raw response", data.hex())
        if not data:
            print_error("Got 0 bytes from socket")
            return False
        else:
            self.decode(data)
            if self.analyze:
                self.rpc_walk(consume_incoming=False, verbose=False)
            self.find_responses()
            return True

    def CallMethod(self, method_descriptor, rpc_controller, request, response_class, done):
        reqUUID = uuid.uuid4().bytes
        typeId, subTypeId = (1, 0xFFFFFFFF) if method_descriptor.name == 'propertyGet' else (0, method_descriptor.index)
        cmm_request = Devialet.CallMeMaybe.Request(
            serverId=self.serverId,
            serviceId=self.find_service_id(method_descriptor.containing_service),
            requestId=reqUUID,
            type=typeId, subTypeId=subTypeId)
        self.write_rpc(cmm_request.SerializeToString(), request.SerializeToString())

        if done is None:
            # Blocking call
            self.blocking_response = None
            self.request_queue[reqUUID] = (method_descriptor, response_class, rpc_controller, self.unblock_call)
            while self.blocking_response is None:
                self.receive()
            return self.blocking_response
        else:
            self.request_queue[reqUUID] = (method_descriptor, response_class, rpc_controller, done)

    def CallUnknownMethod(self, serviceId, subTypeId, request, done):
        reqUUID = uuid.uuid4().bytes
        cmm_request = Devialet.CallMeMaybe.Request(
            serverId=self.serverId,
            serviceId=serviceId,
            requestId=reqUUID, type=0,
            subTypeId=subTypeId)
        self.write_rpc(cmm_request.SerializeToString(), request.SerializeToString())

        # rep.subTypeId == 0xFFFFFFFF and rep.type == 1: Propertyget
        if done is None:
            # Blocking call
            self.blocking_response = None
            self.request_queue[reqUUID] = (None, None, DevialetController(), self.unblock_call)
            while self.blocking_response is None and self.receive():
                print_info("Waiting for response on unknown method (serviceId {}, subTypeId {})",
                           serviceId, subTypeId)
                # time.sleep(1)
            return self.blocking_response
        else:
            self.request_queue[reqUUID] = (None, None, DevialetController(), done)

    def find_responses(self):
        for i in range(len(self.incoming_sections)):
            incoming_section = self.incoming_sections.popleft()
            incoming_pb = incoming_section.raw_protobufs

            if incoming_section.magic == 0xC3:
                print_warning("Found Event")
                try:
                    evt = dvlt_pool.interpret_as(incoming_pb[0], 'Devialet.CallMeMaybe.Event')
                    service_name = self.find_service(evt)

                    method, input_pb, outputs_pb = dvlt_pool.process_rpc(service_name, evt, incoming_pb[1], incoming_pb[1:], is_event=True)
                    if method.containing_service.full_name == 'Devialet.CallMeMaybe.Connection':
                        if method.name == 'serviceAdded':
                            print_info('Extending list of services')
                            self.service_list.add(name=input_pb.name, id=input_pb.id)

                    # The 'uid' parameter in the section, when present (== when magic is C3, and only on incoming packets)
                    # should be equal to the server ID
                    print_info('in_time:{} evt:{} {}/{:>10d}/{:>12d}{:31s} {} E',
                               incoming_section.time,
                               evt.serverId[:4].hex(), evt.type, evt.subTypeId, evt.serviceId,
                               '',
                               incoming_section.uid[:4].hex())
                except IndexError:
                    print_error('not enough incoming protos for event ({}) < 2', len(incoming_pb))
                except AttributeError:
                    pass
                pass

            else:
                try:
                    rep = Devialet.CallMeMaybe.Reply.FromString(incoming_pb[0])

                    method_descriptor, response_class, controller, callback = self.request_queue.pop(rep.requestId)

                    if rep.errorCode != 0:
                        print_warning("Got error code {}", rep.errorCode)
                        # use errorEnumName, controller...

                    # None is used for unknown method calls
                    if response_class is not None:
                        # PropertyGet special "method"
                        if rep.subTypeId == 0xFFFFFFFF and rep.type == 1:
                            response = [dvlt_pool.get_property(method_descriptor.containing_service, i, raw) for i, raw in enumerate(incoming_pb[1:])]
                        else:
                            response = response_class.FromString(incoming_pb[1])
                        print_data("Found Response", response)
                        callback(response)
                    else:
                        # print_data('Response with unknown message type:',
                        #            dvlt_pool.heuristic_search(incoming_pb[1]))
                        callback(dvlt_pool.heuristic_search(incoming_pb[1]))

                    if not rep.isMultipart and len(incoming_pb) > 2:
                        print_warning('we got more incoming protobufs than we should have, not Multipart')

                    if len(incoming_pb) < 2:
                        print_error('we got less than 2 incoming protobufs')

                    # service_name = self.find_service(rep)
                    # method, input_pb, outputs_pb = dvlt_pool.process_rpc(
                    #     service_name, rep, outgoing_pb[1], incoming_pb[1:])

                    # if method.containing_service.full_name == 'Devialet.CallMeMaybe.Connection':
                    #     if method.name == 'openConnection':
                    #         self.service_list = outputs_pb[0].services

                    # print_info('out_time:{} in_time:{} req:{}/{}/{:>10d}/{:>12d}, rep:{}/{}/{:>10d}/{:>12d} {}{}{}',
                    #            outgoing_section.time, incoming_section.time,
                    #            req.requestId[:4].hex(), req.type, req.subTypeId, req.serviceId, rep.requestId[:4].hex(), rep.type, rep.subTypeId, rep.serviceId,
                    #            'M' if rep.isMultipart else ' ',
                    #            ' ' if method.name == 'ping' else 'C' if method.name == 'openConnection' else '.',
                    #            '<' if rep.requestId != req.requestId else ' ')
                except KeyError:
                    print_error('Response to unknown request id {}', rep.requestId.hex())
                # except Exception as e:
                #     print_error('Unexpected {} {}', type(e), e)


class WhatsUpConnection(DevialetConnection):
    def service_discovery(self, wu_list):
        services_by_port = {}
        ports_by_service = {}
        ports_by_unknown_service = {}
        for wu_service in wu_list.services:
            m = re.match('tcp://127.0.0.1:([0-9]+)', wu_service.endpoint)
            truncated_name = '.'.join(wu_service.name.split('.')[:-1])
            if m is not None:
                port = int(m.groups()[0])
                services_by_port.setdefault(port, []).append(truncated_name)
                ports_by_service.setdefault(truncated_name, []).append(port)
                if truncated_name not in dvlt_pool.service_by_name:
                    ports_by_unknown_service.setdefault(truncated_name, []).append(port)

        print_data("Services by port", services_by_port)
        print_data("Ports by Service", ports_by_service)
        # print_data("Ports by (Unknown) Service", ports_by_unknown_service)

        # for port, services in services_by_port.items():
        #     if [0 for srvname in services if srvname not in dvlt_pool.service_by_name]:
        #     # for service in services:
        #     #     if srvname not in dvlt_pool.service_by_name:
        #         new_conn = DevialetConnection(name='Port ' + str(port), addr=self.addr, port=port, start_time=datetime.now())
        #         cmm_ctrl = DevialetController()

        #         conn = Devialet.CallMeMaybe.Connection(new_conn)
        #         conn_reply = conn.openConnection(cmm_ctrl, Devialet.CallMeMaybe.ConnectionRequest(version=1), None)
        #         new_conn.serverId = conn_reply.serverId
        #         new_conn.service_list = conn_reply.services

        #         # Connect to unknown service
        #         for service in new_conn.service_list:
        #             truncated_name = '.'.join(service.name.split('.')[:-1])
        #             if truncated_name not in dvlt_pool.service_by_name:
        #                 for subTypeId in range(10):
        #                     result = new_conn.CallUnknownMethod(service.id, subTypeId, Devialet.CallMeMaybe.Empty(), None)
        #                     print_data("Response from method id {} from service {}".format(subTypeId, truncated_name),
        #                                result)
        #                     if result is None:
        #                         break
        #         new_conn.close()


class DevialetController(RpcController):
    def __init__(self):
        self.failed = False
        self.canceled = False
        self.cancel_callback = None
        self.error = ""

    def Reset(self):
        # Resets the RpcController to its initial state.
        self.__init__()

    def Failed(self):
        # Returns true if the call failed.
        return self.failed

    def ErrorText(self):
        # If Failed is true, returns a human-readable description of the error.
        return self.error

    def StartCancel(self):
        # Initiate cancellation.
        self.canceled = True
        if self.cancel_callback is not None:
            self.cancel_callback()

    def SetFailed(self, reason):
        # Sets a failure reason.
        self.failed = True
        self.error = reason

    def IsCanceled(self):
        # Checks if the client cancelled the RPC.
        return self.canceled

    def NotifyOnCancel(self, callback):
        # Sets a callback to invoke on cancel.
        self.cancel_callback = callback


# MultiCast receiver - Discovery protocol
# Put this in a separate thread eventually

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 24242

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

database = {}
print_info('Searching for Devialet Device...')
while not database:
    data, (sender_addr, sender_port) = sock.recvfrom(1024)
    if len(data) >= 12:
        magic, serial_len = struct.unpack('>8sI', data[:12])
        if magic == b'DVL\x01HERE' and len(data) == 12 + serial_len:
            database[data[12:]] = sender_addr
            print_info('Found Devialet Device with serial {} at address {}'.format(data[12:], sender_addr))

serial, dvlt_addr = database.popitem()


def callback_test(arg):
    print_data("Callback with", arg)

# Open a WhatsUp connection
wu_conn = WhatsUpConnection(name="WhatsUp", addr=dvlt_addr, port=24242, start_time=datetime.now())
cmm_ctrl = DevialetController()

conn = Devialet.CallMeMaybe.Connection(wu_conn)
# No Callback - does a blocking RPC
conn_reply = conn.openConnection(cmm_ctrl, Devialet.CallMeMaybe.ConnectionRequest(version=1), None)
wu_conn.serverId = conn_reply.serverId
wu_conn.service_list = conn_reply.services

Devialet.WhatsUp.Registry(wu_conn).getNetworkConfiguration(cmm_ctrl, Devialet.CallMeMaybe.Empty(), callback_test)
Devialet.WhatsUp.Registry(wu_conn).listServices(cmm_ctrl, Devialet.CallMeMaybe.Empty(), wu_conn.service_discovery)
# Devialet.WhatsUp.Registry(wu_conn).propertyGet(cmm_ctrl, Devialet.CallMeMaybe.Empty(), callback_test)


def pingback(arg):
    print_info("Pong <--")

while True:  # ~ 20 ms round-trip for pings
    # time.sleep(1)
    ready = select([wu_conn.sock], [], [], 1)
    print_info("One spin of the loop")
    if ready[0]:
        wu_conn.receive()
    else:
        print_info("Ping -->")
        conn.ping(DevialetController(), Devialet.CallMeMaybe.Empty(), pingback)
