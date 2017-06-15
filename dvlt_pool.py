import os
import sys
import types
import subprocess

from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message_factory import MessageFactory
from google.protobuf.descriptor_pb2 import FileDescriptorProto, ServiceOptions
from google.protobuf.service_reflection import GeneratedServiceStubType
import google.protobuf.service
import google.protobuf.descriptor
import google.protobuf.message

from protobuf_to_dict import protobuf_to_dict

from dvlt_output import print_warning, print_error, print_info, print_data, print_errordata

sys.modules['Devialet'] = types.ModuleType('Devialet')
import Devialet


def full_len(d):
    if type(d) == dict:
        return 1 + sum(full_len(v) for v in d.values())
    elif type(d) == list:
        return 1 + sum(full_len(v) for v in d)
    else:
        return 1


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
        packages = []

        factory = MessageFactory(pool=self)
        self.messages = {}

        def import_protoc(filename):
            pb_raw = open(os.path.join('protoc', filename), 'rb').read()
            filedesc = FileDescriptorProto()
            filedesc.ParseFromString(pb_raw)
            # print_data(filedesc.name, filedesc)
            self.Add(filedesc)
            proto_filenames.append(filedesc.name)
            packages.append(filedesc.package)
            # self.messages.update(factory.GetMessages([filedesc.name]))

        # Need to import dvltServiceOptions first
        import_protoc('CallMeMaybe_CallMeMaybe.protoc')
        self.messages.update(factory.GetMessages(proto_filenames))

        for filename in protoc_filenames:
            import_protoc(filename)
        self.messages.update(factory.GetMessages(proto_filenames))

        for pkgname in packages:
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

        def get_mod(objname):
            mod = Devialet
            for submodname in objname.split('.')[1:-1]:
                mod = getattr(mod, submodname)
            return mod

        # Import message classes into modules
        for msgname, msg in self.messages.items():
            setattr(get_mod(msgname), msgname.split('.')[-1], msg)

        # Offsets of original methods (for 1000 codes)
        self.method_offset_by_full_name = {}

        # lowercase names with -0 for inheritance
        self.service_by_name = {}

        # Both will be populated by method below
        self.extend_services()

        # Define service classes and add them to modules
        for srvname, srvdesc in self._service_descriptors.items():
            srvtype = GeneratedServiceStubType(srvname, (google.protobuf.service.Service,), {
                'DESCRIPTOR': srvdesc,
                '__module__': srvname.split('.')[:-1]
            })
            setattr(get_mod(srvname), srvname.split('.')[-1], srvtype)

    def extend_services(self):
        service_options_ext = self.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
        service_properties_msg = Devialet.CallMeMaybe.ServiceProperties.DESCRIPTOR
        empty_msg = Devialet.CallMeMaybe.Empty.DESCRIPTOR
        # Extend services with base service props and methods
        for service_name, service in self._service_descriptors.items():
            opts = service.GetOptions().\
                Extensions[service_options_ext]
            service_properties = opts.properties

            self.service_by_name[opts.serviceName] = service

            original_amount_of_methods = len(service.methods)

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
                for method in baseservice_methods:
                    new_method = google.protobuf.descriptor.MethodDescriptor(
                        method.name, method.full_name,
                        len(service.methods),
                        service, method.input_type,
                        method.output_type, options=method.GetOptions())
                    service.methods_by_name[method.name] = new_method
                    new_methods.append(new_method)
                service.methods = new_methods + service.methods

                # Moving up in base service tree
                baseservice_name = baseservice_opts.baseService

            self.method_offset_by_full_name[service_name] = len(service.methods) - original_amount_of_methods
            # if self.method_offset_by_full_name[service_name] != 0:
            #     print_info('Added {} inherited methods left of original {} to {}',
            #                self.method_offset_by_full_name[service_name],
            #                original_amount_of_methods, service_name)

        # Add 3 special methods
        for service_name, service in self._service_descriptors.items():
            propertyget = google.protobuf.descriptor.MethodDescriptor(
                'propertyGet', service_name + '.propertyGet',
                len(service.methods), service, empty_msg, service_properties_msg)
            service.methods.append(propertyget)
            service.methods_by_name['propertyGet'] = propertyget

            propertyupdate = google.protobuf.descriptor.MethodDescriptor(
                'propertyUpdate', service_name + '.propertyUpdate',
                len(service.methods), service, service_properties_msg, empty_msg)
            service.methods.append(propertyupdate)
            service.methods_by_name['propertyUpdate'] = propertyupdate

            propertyset = google.protobuf.descriptor.MethodDescriptor(
                'propertySet', service_name + '.propertySet',
                len(service.methods), service, service_properties_msg, empty_msg)
            service.methods.append(propertyset)
            service.methods_by_name['propertySet'] = propertyset

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
        results = {}
        if len(raw_protobuf) == 0:
            return {'empty protobuf'}
        for proto in self.messages:
            if proto.startswith(filter):
                try:
                    tmp = self.messages[proto]()
                    tmp.ParseFromString(raw_protobuf)
                    results[proto] = full_len(protobuf_to_dict(tmp))
                    if strict and len(tmp.FindInitializationErrors()) > 0:
                        results[proto] = -1
                except Exception as e:
                    # print('Error in heuristic:',    type(e), e)
                    results[proto] = -1
            else:
                results[proto] = -1
        return [raw_decode(raw_protobuf)] + sorted([
            (proto, length) for (proto, length) in results.items() if length > 2 and (length > 0 or length > max(results[x] for x in results)/2)
        ], key=lambda x: x[1])

    def get_property(self, service_desc, property_id, output_raw):
        service_options_ext = self.FindExtensionByName('Devialet.CallMeMaybe.dvltServiceOptions')
        props = service_desc.GetOptions().Extensions[service_options_ext].properties.property
        try:
            # Fix for PlaylistSaved
            if props[property_id].type not in self.messages:
                props[property_id].type = service_desc.file.package + '.' + props[property_id].type
            prop = self.interpret_as(output_raw, props[property_id].type)
            print_data('property {}:'.format(props[property_id].name), prop)
            return prop
        except IndexError:
            print_error('Too many multiparts for propertyget({}), {} >= {}, raw {}',
                        service_desc.full_name, property_id, len(props),
                        ' '.join(raw_decode(output_raw)['protoc'].split('\n')))
            return Devialet.CallMeMaybe.Empty()

    def process_rpc(self, service_name, rep, input_raw, outputs_raw, is_event=False):
        empty = Devialet.CallMeMaybe.Empty()
        try:
            service_desc = self.service_by_name[service_name]

            if rep.subTypeId == 0xFFFFFFFF and rep.type == 1:
                # Get Properties / No actual method
                # Usually Multipart is set
                print_info('PropertyGet details: {} / {} outputs, type={} subtype={}'.format(
                    service_name, len(outputs_raw), rep.type, rep.subTypeId))
                if len(input_raw):
                    print_error('PropertyGet but input type not empty')
                outputs_pb = []
                for i, output_raw in enumerate(outputs_raw):
                    prop = self.get_property(service_desc, i, output_raw)
                    outputs_pb.append(prop)
                    # print_data(prop.name, interpret_as(output_raw, prop.type))
                return (service_desc.methods_by_name['propertyGet'], empty, outputs_pb)
            elif rep.type == 1 and is_event:
                # Property Update Event
                print_info('PropertyUpdate details: {}, type={} subtype={}'.format(
                    service_name, rep.type, rep.subTypeId))
                prop = self.get_property(service_desc, rep.subTypeId, input_raw)
                return (service_desc.methods_by_name['propertyUpdate'], prop, empty)
            elif rep.type == 1 and not is_event:
                # Property Set Request
                print_info('PropertySet details: {}, type={} subtype={}'.format(
                    service_name, rep.type, rep.subTypeId))
                prop = self.get_property(service_desc, rep.subTypeId, input_raw)
                return (service_desc.methods_by_name['propertySet'], prop, empty)
            else:
                # Regular RPC Method, Response + Request (including regular events where output type = CmmEmpty)
                try:
                    # subtypes > 1000 mean original methods (non-extended)
                    if rep.subTypeId >= 1000:
                        rep.subTypeId -= 1000
                        rep.subTypeId += self.method_offset_by_full_name[service_desc.full_name]

                    method = service_desc.methods[rep.subTypeId]

                    print_info('RPC/Event details: {} -> {} [{} -> {}]'.format(
                        service_name, method.full_name, method.input_type.full_name, method.output_type.full_name))

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

dvlt_pool = DevialetDescriptorPool()
