import os
import sys
import types
import subprocess

from google.protobuf.internal import api_implementation
api_implementation._SetType("python")

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message_factory import MessageFactory
from google.protobuf.descriptor_pb2 import FileDescriptorProto, ServiceOptions
from google.protobuf.service_reflection import GeneratedServiceStubType
from google.protobuf.json_format import MessageToDict
import google.protobuf.service
import google.protobuf.descriptor
import google.protobuf.message

from dvlt_output import print_warning, print_error, print_info, print_data, print_errordata

sys.modules['Devialet'] = types.ModuleType('Devialet')
import Devialet


def raw_decode(data):
    process = subprocess.Popen(['protoc', '--decode_raw'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.stdin.write(data)
    process.stdin.close()
    ret = process.wait()
    if ret == 0:
        return {
            'raw': data,
            'protoc': process.stdout.read().decode()
        }
    else:
        return {
            'raw': data,
            'protoc': '',
            'error': 'Failed to parse: ' + ' '.join('{:02x}'.format(x) for x in data)
        }


class DevialetDescriptorPool(DescriptorPool):
    def __init__(self):
        DescriptorPool.__init__(self)
        # Needed by Extensions
        self.AddDescriptor(ServiceOptions.DESCRIPTOR)

        protoc_filenames = [
            'AppleAirPlay_Playback.protoc',
            # 'CallMeMaybe_CallMeMaybe.protoc',
            'CallMeMaybe_CommonMessages.protoc',
            'Fresh_Fresh.protoc',
            'GetThePartyStarted_Aerobase.protoc',
            'GetThePartyStarted_GetThePartyStarted.protoc',
            'GetThePartyStarted_Logging.protoc',
            'GetThePartyStarted_Player.protoc',
            # 'google_protobuf_descriptor.protoc',
            'IMASlave4U_Configuration.protoc',
            'IMASlave4U_SoundControl.protoc',
            'IMASlave4U_SoundDesign.protoc',
            'LeftAlone_Configuration.protoc',
            'MasterOfPuppets_Configuration.protoc',
            'RPCMessages.protoc',
            'SaveMe_SaveMe.protoc',
            'SpotifyConnect_SpotifyConnect.protoc',
            'TheSoundOfSilence_Album.protoc',
            'TheSoundOfSilence_Artist.protoc',
            'TheSoundOfSilence_Category.protoc',
            'TheSoundOfSilence_Collection.protoc',
            'TheSoundOfSilence_LiveSource.protoc',
            'TheSoundOfSilence_Node.protoc',
            'TheSoundOfSilence_OnlineSource.protoc',
            'TheSoundOfSilence_Picture.protoc',
            'TheSoundOfSilence_Playlist.protoc',
            'TheSoundOfSilence_Session.protoc',
            'TheSoundOfSilence_Source.protoc',
            'TheSoundOfSilence_Subcategory.protoc',
            'TheSoundOfSilence_TrackDetails.protoc',
            'TheSoundOfSilence_Track.protoc',
            'TooManyFlows_Configuration.protoc',
            'TooManyFlows_History.protoc',
            'TooManyFlows_Identifier.protoc',
            'TooManyFlows_Metadata.protoc',
            'TooManyFlows_Playback.protoc',
            'TooManyFlows_Playlist.protoc',
            'TooManyFlows_SoundControl.protoc',
            'TooManyFlows_SoundDesign.protoc',
            'TwerkIt_SoundDesign.protoc',
            'UniversallySpeakingRenderer_UniversallySpeakingRenderer.protoc',
            'WhatsUp.protoc'
        ]

        proto_filenames = []
        self.packages = []

        factory = MessageFactory(pool=self)
        self.messages = {}

        def import_protoc(filename):
            pb_raw = open(os.path.join('protoc', filename), 'rb').read()
            filedesc = FileDescriptorProto()
            filedesc.ParseFromString(pb_raw)
            # print_data(filedesc.name, filedesc)
            self.Add(filedesc)
            proto_filenames.append(filedesc.name)
            if filedesc.package not in self.packages:
                self.packages.append(filedesc.package)
            # self.messages.update(factory.GetMessages([filedesc.name]))

        # Need to import dvltServiceOptions first
        import_protoc('CallMeMaybe_CallMeMaybe.protoc')
        self.messages.update(factory.GetMessages(proto_filenames))

        # Import the rest
        for filename in protoc_filenames:
            import_protoc(filename)
        self.messages.update(factory.GetMessages(proto_filenames))

        # Define modules and submodules
        for pkgname in self.packages:
            mod = Devialet
            path = "Devialet"
            for submodname in pkgname.split('.')[1:]:
                path += '.' + submodname
                if hasattr(mod, submodname):
                    submod = getattr(mod, submodname)
                else:
                    submod = sys.modules[path] = types.ModuleType(path)
                    setattr(mod, submodname, submod)
                mod = submod

        # Import message classes into modules
        for msgname, msg in self.messages.items():
            setattr(self.get_mod(msgname), msgname.split('.')[-1], msg)

        # lowercase names with -0 for inheritance
        self.service_by_name = {}

        # Extend service descriptors with parent methods and properties,
        # and create service stub classes
        self.extend_services()

    # Get module object from fully-qualified message or service name
    def get_mod(self, objname):
        mod = Devialet
        for submodname in objname.split('.')[1:-1]:
            mod = getattr(mod, submodname)
        return mod

    def extend_services(self):
        service_options_ext = self.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
        method_options_ext = self.FindExtensionByName('Devialet.CallMeMaybe.dvltMethodOptions')
        service_properties_msg = Devialet.CallMeMaybe.ServiceProperties.DESCRIPTOR
        empty_msg = Devialet.CallMeMaybe.Empty.DESCRIPTOR

        # Extend services with base service props and methods, and define service classes
        for service_name, service in self._service_descriptors.items():
            opts = service.GetOptions().\
                Extensions[service_options_ext]
            service_properties = opts.properties

            self.service_by_name[opts.serviceName] = service

            service.methods_by_id = {1000 + id: method for (id, method) in enumerate(service.methods)}
            method_id_offset = 2000

            baseservice_name = opts.baseService
            while baseservice_name in self._service_descriptors:
                # Extending Properties from base service
                baseservice_opts = self._service_descriptors[baseservice_name]\
                    .GetOptions()\
                    .Extensions[service_options_ext]
                base_props = baseservice_opts.properties

                new_props = Devialet.CallMeMaybe.ServiceProperties()
                new_props.MergeFrom(base_props)
                # new_props.property.extend(service_properties.property)
                for prop in service_properties.property:
                    if prop.name not in [p.name for p in new_props.property]:
                        new_props.property.add()
                        new_props.property[-1].MergeFrom(prop)
                    else:
                        # Should probably replace old with new instead
                        # print_warning('Duplicate property {} not added', prop.name)
                        pass

                service_properties.CopyFrom(new_props)

                # Extending Methods from base service
                baseservice_methods = self._service_descriptors[baseservice_name].methods
                new_methods = []
                for method_id, method in enumerate(baseservice_methods):
                    new_method = google.protobuf.descriptor.MethodDescriptor(
                        method.name, method.full_name,
                        len(service.methods),
                        service, method.input_type,
                        method.output_type, options=method.GetOptions())
                    service.methods_by_name[method.name] = new_method
                    new_methods.append(new_method)
                    service.methods_by_id[method_id_offset + method_id] = method
                service.methods = new_methods + service.methods

                # Moving up in base service tree
                baseservice_name = baseservice_opts.baseService
                method_id_offset += 1000

            # Fix for PlaylistSaved
            for prop in service_properties.property:
                if prop.type not in self.messages:
                    prop.type = service.file.package + '.' + prop.type

            # self.method_offset_by_full_name[service_name] = len(service.methods) - original_amount_of_methods
            # if self.method_offset_by_full_name[service_name] != 0:
            #     print_info('Added {} inherited methods left of original {} to {}',
            #                self.method_offset_by_full_name[service_name],
            #                original_amount_of_methods, service_name)

            # Add 3 special methods
            # They don't actually return this...
            propertyget = google.protobuf.descriptor.MethodDescriptor(
                'propertyGet', service_name + '.propertyGet',
                len(service.methods), service, empty_msg, service_properties_msg)
            service.methods.append(propertyget)
            service.methods_by_name['propertyGet'] = propertyget

            propertyupdate = google.protobuf.descriptor.MethodDescriptor(
                'propertyUpdate', service_name + '.propertyUpdate',
                len(service.methods), service, service_properties_msg, empty_msg,
                options={})
            propertyupdate.GetOptions().Extensions[method_options_ext].isNotification = True
            service.methods.append(propertyupdate)
            service.methods_by_name['propertyUpdate'] = propertyupdate

            propertyset = google.protobuf.descriptor.MethodDescriptor(
                'propertySet', service_name + '.propertySet',
                len(service.methods), service, service_properties_msg, empty_msg)
            service.methods.append(propertyset)
            service.methods_by_name['propertySet'] = propertyset

            # Add regular method ids
            for method_id, method in enumerate(service.methods):
                service.methods_by_id[method_id] = method

            # Define service class and add it to module
            srvtype = GeneratedServiceStubType(service_name, (DevialetService,), {
                'DESCRIPTOR': service,
                'serviceName': opts.serviceName,
                'baseService': opts.baseService,
                'errorEnumName': opts.errorEnumName,
                'methods_by_id': service.methods_by_id,
                'property_descs_by_id': list(service_properties.property),
                'property_descs_by_name': {prop.name: prop for prop in service_properties.property},
                '__module__': '.'.join(service_name.split('.')[:-1])
            })
            setattr(self.get_mod(service_name), service_name.split('.')[-1], srvtype)
            # Link to class in service descriptor
            service._concrete_class = srvtype

    def interpret_as(self, raw_protobuf, proto_name):
        try:
            ret = self.messages[proto_name]()
            ret.ParseFromString(raw_protobuf)
            if ret.FindInitializationErrors():
                print_warning('There were uninitialized fields in pb of type {}: {}, raw {}',
                              proto_name, ret.FindInitializationErrors(),
                              ' '.join(raw_decode(raw_protobuf)['protoc'].split('\n')))
                print_errordata("Possible matches:", self.heuristic_search(raw_protobuf))
            return ret
        except Exception as e:
            print_error("Can't interpret protobuf {{{}}} as {}: {}",
                        ' '.join(raw_decode(raw_protobuf)['protoc'].split('\n')), proto_name, e)
            print_errordata("Possible matches:", self.heuristic_search(raw_protobuf))
            pass
        return Devialet.CallMeMaybe.Empty()

    def heuristic_search(self, raw_protobuf, filter='', strict=True):
        def full_len(d):
            if type(d) == dict:
                return 1 + sum(full_len(v) for v in d.values())
            elif type(d) == list:
                return 1 + sum(full_len(v) for v in d)
            else:
                return 1
        results = {}
        if len(raw_protobuf) == 0:
            return {'empty protobuf'}
        for proto in self.messages:
            if proto.startswith(filter):
                try:
                    tmp = self.messages[proto].FromString(raw_protobuf)
                    results[proto] = full_len(MessageToDict(tmp))
                    if strict and (tmp.FindInitializationErrors() or
                                   tmp._unknown_fields or
                                   tmp.SerializeToString() != raw_protobuf):
                        results[proto] = -1
                except Exception as e:
                    # print('Error in heuristic:',    type(e), e)
                    results[proto] = -1
            else:
                results[proto] = -1
        return [raw_decode(raw_protobuf)] + sorted([
            (proto, length) for (proto, length) in results.items() if length > 2 or (length > 0 and length >= max(results[x] for x in results)/2)
        ], key=lambda x: x[1])

    def get_property(self, service_desc, property_id, output_raw):
        service_options_ext = self.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
        props = service_desc.GetOptions().Extensions[service_options_ext].properties.property
        try:
            # Fix for PlaylistSaved
            # if props[property_id].type not in self.messages:
            #     props[property_id].type = service_desc.file.package + '.' + props[property_id].type
            prop = self.interpret_as(output_raw, props[property_id].type)
            print_data('property {}:'.format(props[property_id].name), prop)
            return props[property_id].name, prop
        except IndexError:
            print_error('Too many multiparts for propertyget({}), {} >= {}, raw {}',
                        service_desc.full_name, property_id, len(props),
                        ' '.join(raw_decode(output_raw)['protoc'].split('\n')))
            return '', Devialet.CallMeMaybe.Empty()

    def process_rpc(self, service_name, rep, input_raw, outputs_raw, is_event=False):
        empty = Devialet.CallMeMaybe.Empty()
        try:
            service_desc = self.service_by_name[service_name]

            if rep.subTypeId == 0xFFFFFFFF and rep.type == 1:
                # Get Properties / No actual method
                # Usually Multipart is set
                print_info('PropertyGet details: {} / {} outputs, type={} subtype={}',
                           service_name, len(outputs_raw), rep.type, rep.subTypeId, color='cyan')
                if len(input_raw):
                    print_error('PropertyGet but input type not empty')
                outputs_pb = []
                for i, output_raw in enumerate(outputs_raw):
                    name, prop = self.get_property(service_desc, i, output_raw)
                    outputs_pb.append(prop)
                    # print_data(prop.name, interpret_as(output_raw, prop.type))
                return (service_desc.methods_by_name['propertyGet'], empty, outputs_pb)
            elif rep.type == 1 and is_event:
                # Property Update Event
                print_info('PropertyUpdate details: {}, type={} subtype={}',
                           service_name, rep.type, rep.subTypeId, color='cyan')
                name, prop = self.get_property(service_desc, rep.subTypeId, input_raw)
                return (service_desc.methods_by_name['propertyUpdate'], prop, empty)
            elif rep.type == 1 and not is_event:
                # Property Set Request
                print_info('PropertySet details: {}, type={} subtype={}',
                           service_name, rep.type, rep.subTypeId, color='cyan')
                name, prop = self.get_property(service_desc, rep.subTypeId, input_raw)
                return (service_desc.methods_by_name['propertySet'], prop, empty)
            else:
                if rep.type != 0:
                    print_error('Got strange response type {}', rep.type)
                # Regular RPC Method, Response + Request (including regular events where output type = CmmEmpty)
                try:
                    method = service_desc.methods_by_id[rep.subTypeId]

                    print_info('RPC/Event details: {} [{} -> {}]', method.full_name[9:],
                               method.input_type.full_name[9:], method.output_type.full_name[9:], color='magenta')

                    # input_pb = service.GetRequestClass(method)()
                    # input_pb.ParseFromString(input_raw)
                    # output_pb = service.GetResponseClass(method)()
                    # output_pb.ParseFromString(outputs_raw[0])

                    input_pb = self.interpret_as(input_raw, method.input_type.full_name)
                    output_pb = self.interpret_as(outputs_raw[0], method.output_type.full_name)

                    print_data('input  ({}):'.format(method.input_type.full_name), input_pb)
                    print_data('output ({}):'.format(method.output_type.full_name), output_pb)

                    return(method, input_pb, [output_pb])
                except IndexError as e:
                    print_error('{} too big for {} that has only {} methods: {}', rep.subTypeId, service_desc.full_name, len(service_desc.methods), e)
                except (google.protobuf.message.DecodeError, UnicodeDecodeError) as e:
                    print_error('Failed to decode incoming or outgoing protobuf: {}', e)
        except KeyError:
            print_error("Can't find service {} in database", service_name)
        return (None, empty, [])

    def print_graph(self):
        service_options_ext = self.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
        links = set()
        print('digraph proto {')
        print('\trankdir=LR;')
        print('\tnode [shape=Mrecord, fontname = "roboto mono"];')
        for package in self.packages:
            print('\tsubgraph "cluster_{}" {{'.format(package))
            for filename, filedesc in self._file_descriptors.items():
                if filedesc.package == package:
                    # print(package, filename)
                    print('\t\tsubgraph "cluster_{}" {{'.format(filename))
                    # print()
                    # label = ''
                    for i, srv in enumerate(filedesc.services_by_name.values()):
                        opts = srv.GetOptions().Extensions[service_options_ext]
                        # print(srv.full_name, opts.baseService, opts.serviceName)
                        print('\t\t\t"{}";'.format(srv.full_name))
                        if opts.baseService:
                            links.add((srv.full_name, opts.baseService))
                            # base = self._service_descriptors[opts.baseService]
                            # links.add(('"{}":"{}"'.format(filename, srv.name), '"{}":"{}"'.format(base.file.name, base.name)))
                            # print('\t\t"{}" -> "{}";'.format(srv.full_name, opts.baseService))

                        # parent_servicename = '.'.join(opts.serviceName.split('.')[:-1])
                        # if parent_servicename in self.service_by_name:
                        #     # if opts.baseService != self.service_by_name[parent_servicename].full_name:
                        #     links.add((srv.full_name, self.service_by_name[parent_servicename].full_name))
                        #     # parent = self.service_by_name[parent_servicename]
                        #     # links.add(('"{}":"{}"'.format(filename, srv.name), '"{}":"{}"'.format(parent.file.name, parent.name)))
                        #         # print('\t\t"{}" -> "{}";'.format(srv.full_name, self.service_by_name[parent_servicename].full_name))
                    # for dep in filedesc.dependencies:
                    #     links.add(('"{}"'.format(filename), '"{}"'.format(dep.name)))
                    print('\t\t}')
                    # print('\t\t"{}" [label="{}|{}"];'.format(filename, filename, '|'.join([
                    #     '<{}> {}'.format(srv.name, srv.full_name) for srv in filedesc.services_by_name.values()
                    # ])))
            print('\t}')
        for (left, right) in links:
            # print('\t{} -> {};'.format(left, right))
            print('\t"{}" -> "{}";'.format(left, right))
        print('}')


class DevialetController(google.protobuf.service.RpcController):
    def __init__(self, parent_service):
        self.failed = False
        self.canceled = False
        self.cancel_callback = None
        self.error = ""
        self.parent_service = parent_service

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
        self.error = self.parent_service.get_error(reason)
        print_error("Got error code: {} ({})", self.error, reason)

    def IsCanceled(self):
        # Checks if the client cancelled the RPC.
        return self.canceled

    def NotifyOnCancel(self, callback):
        # Sets a callback to invoke on cancel.
        self.cancel_callback = callback


class DevialetService(google.protobuf.service.Service):
    serviceName = ''
    baseService = ''
    errorEnumName = ''
    methods_by_id = {}
    property_descs_by_name = {}
    property_descs_by_id = []

    # Overriden, doesn't do anything
    # def __init__(self, *args, **kwargs):
        # google.protobuf.service.Service.__init__(self, *args, **kwargs)
        # self.properties = {}
        # # self.service_id = self.rpc_channel.find_service_id(self.serviceName)
        # # self.unique_name = [srv.name for srv in self.rpc_channel.service_list.services if srv.id == self.service_id][0]
        # print_info('Getting properties')
        # self.propertyGet(DevialetController(self), None, self.set_properties)
        # self.propertyGet(controller, Devialet.CallMeMaybe.Empty(), callback_test)
        # self.rpc_channel.

    def set_properties(self, raw_property_list):
        # print_info('Found {} properties for {}', len(raw_property_list),
        #            self.service_name_unique if hasattr(self, 'service_name_unique') else self.serviceName)
        for property_id, raw_property in enumerate(raw_property_list):
            self.set_property(property_id, raw_property)

    def set_property(self, property_id, output_raw):
        try:
            prop = self.property_descs_by_id[property_id]
            prop_pb = dvlt_pool.interpret_as(output_raw, prop.type)
            print_data('property {} from {}:'.format(prop.name,
                       self.service_name_unique if hasattr(self, 'service_name_unique') else self.serviceName), prop_pb)
            self.properties[prop.name] = prop_pb
        except IndexError:
            print_error('Too many multiparts for propertyget({}), {} >= {}',
                        self.DESCRIPTOR.full_name, property_id, len(self.property_descs_by_id))
            print_errordata('Raw output', output_raw.hex())

    # def set_property_by_pb(self, property_pb)

    def get_property(self, property_name):
        return self.properties[property_name]

    def get_properties(self):
        try:
            return [self.properties[desc.name] for i, desc in enumerate(self.property_descs_by_id)]
        except KeyError as e:
            print_error('property {} undefined', e)

    # def propertyGet(self, controller, request, callback):
    #     raise NotImplementedError

    def watch_properties(self, service_id=None, service_name=None):
        self.properties = {}
        # if service_name is not None:
        #     service_opt_ext = dvlt_pool.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
        #     opt = self.DESCRIPTOR.GetOptions().Extensions[service_opt_ext]
        #     new_opt = ServiceOptions.FromString(opt.SerializeToString())
        #     new_opt.Extensions[service_opt_ext].serviceName = service_name

        #     new_desc = google.protobuf.descriptor.ServiceDescriptor(
        #         self.DESCRIPTOR.name,
        #         self.DESCRIPTOR.full_name,
        #         self.DESCRIPTOR.index,
        #         [],
        #         options=new_opt,
        #         file=self.DESCRIPTOR.file)

        #     for method in self.DESCRIPTOR.methods:
        #         new_desc.methods.append(google.protobuf.descriptor.MethodDescriptor(
        #             method.name,
        #             method.full_name,
        #             method.index,
        #             new_desc,
        #             method.input_type,
        #             method.output_type,
        #             options=method.GetOptions()))
            # print(new_desc.methods[0].containing_service)
            # self.serviceName = service_name
            # print_info('Changing descriptor from {} to {}', self.DESCRIPTOR, new_desc)
            # self.DESCRIPTOR = new_desc
        # self.service_id = self.rpc_channel.find_service_id(self.serviceName)
        # self.unique_name = [srv.name for srv in self.rpc_channel.service_list.services if srv.id == self.service_id][0]
        if service_id is not None:
            self.service_id = service_id
        if service_name is not None:
            self.service_name_unique = service_name
        print_info('Getting properties for {}', self.serviceName)
        props = self.propertyGet(DevialetController(self), Devialet.CallMeMaybe.Empty(), None)
        if props is not None:
            self.set_properties(props)
        self.propertyUpdate(DevialetController(self), None, self.set_property)

    def get_error(self, errorcode):
        if errorcode > Devialet.CallMeMaybe.BaseError.MAX_ERROR:
            errorcode -= Devialet.CallMeMaybe.BaseError.MAX_ERROR
            try:
                error_enum = dvlt_pool.FindEnumTypeByName(self.errorEnumName)
                return error_enum.values_by_number[errorcode].name
            except KeyError:
                return 'unknownError'
        else:
            return Devialet.CallMeMaybe.BaseError.Code.Name(errorcode)

    # def CallUnknownMethod(self, subTypeId, request, done):
    #     print_info('Calling unknown method #{} from service #{} on port {}', subTypeId, self.service_id, self.rpc_channel.port)
    #     reqUUID = uuid.uuid4().bytes
    #     cmm_request = Devialet.CallMeMaybe.Request(
    #         serverId=self.rpc_channel.serverId,
    #         serviceId=self.service_id,
    #         requestId=reqUUID, type=0,
    #         subTypeId=subTypeId)
    #     if done is None:
    #         # Blocking call
    #         self.rpc_channel.blocking_response = None
    #         self.rpc_channel.request_queue[reqUUID] = (None, None, DevialetController(), self.rpc_channel.unblock_call)
    #         self.write_rpc(cmm_request.SerializeToString(), request.SerializeToString())
    #         while self.rpc_channel.blocking_response is None and self.rpc_channel.receive():
    #             # print_info("Waiting for response on unknown method (serviceId {}, subTypeId {})",
    #             #            serviceId, subTypeId)
    #             # time.sleep(1)
    #             pass
    #         if self.rpc_channel.blocking_response is None:
    #             self.rpc_channel.close()
    #             print_error("Server hung up before response")
    #         return self.rpc_channel.blocking_response
    #     else:
    #         self.rpc_channel.request_queue[reqUUID] = (None, None, DevialetController(), done)
    #         self.write_rpc(cmm_request.SerializeToString(), request.SerializeToString())

dvlt_pool = DevialetDescriptorPool()

if __name__ == '__main__':
    dvlt_pool.print_graph()
