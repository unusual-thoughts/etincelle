import re
from pprint import pprint

import AppleAirPlay.Playback_pb2
import CallMeMaybe.CallMeMaybe_pb2
import CallMeMaybe.CommonMessages_pb2
import Fresh.Fresh_pb2
import GetThePartyStarted.Aerobase_pb2
import GetThePartyStarted.GetThePartyStarted_pb2
import GetThePartyStarted.Logging_pb2
import GetThePartyStarted.Player_pb2
import IMASlave4U.Configuration_pb2
import IMASlave4U.SoundControl_pb2
import IMASlave4U.SoundDesign_pb2
import LeftAlone.Configuration_pb2
import MasterOfPuppets.Configuration_pb2
import RPCMessages_pb2
import SaveMe.SaveMe_pb2
import SpotifyConnect.SpotifyConnect_pb2
import TheSoundOfSilence.Album_pb2
import TheSoundOfSilence.Artist_pb2
import TheSoundOfSilence.Category_pb2
import TheSoundOfSilence.Collection_pb2
import TheSoundOfSilence.LiveSource_pb2
import TheSoundOfSilence.Node_pb2
import TheSoundOfSilence.OnlineSource_pb2
import TheSoundOfSilence.Picture_pb2
import TheSoundOfSilence.Playlist_pb2
import TheSoundOfSilence.Session_pb2
import TheSoundOfSilence.Source_pb2
import TheSoundOfSilence.Subcategory_pb2
import TheSoundOfSilence.TrackDetails_pb2
import TheSoundOfSilence.Track_pb2
import TooManyFlows.Configuration_pb2
import TooManyFlows.History_pb2
import TooManyFlows.Identifier_pb2
import TooManyFlows.Metadata_pb2
import TooManyFlows.Playback_pb2
import TooManyFlows.Playlist_pb2
import TooManyFlows.SoundControl_pb2
import TooManyFlows.SoundDesign_pb2
import TwerkIt.SoundDesign_pb2
import WhatsUp_pb2

from google.protobuf import descriptor_pb2, message

from dvlt_messages import interpret_as, heuristic_search
from dvlt_output import *

class DevialetRPCProcessor:
    def __init__(self):
        self.service_list = RPCMessages_pb2.ServicesList().services
        self.find_and_extend_services()
    def get_property(self, service_desc, property_id, output_raw):
        props = service_desc \
                .GetOptions() \
                .Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions] \
                .properties \
                .property
        try:
            # print("Trying to get property {} from {}".format(property_id, service_desc.full_name))
            # return props[property_id]
            prop = interpret_as(output_raw, props[property_id].type)
            print_data("property {}:".format(props[property_id].name), prop)
            return prop
        except IndexError:
            print_error('Too many multiparts for propertyget({}), {} >= {}', 
                service_desc.full_name, property_id, len(props))
            return CallMeMaybe.CommonMessages_pb2.Empty()

    def process_rpc(self, rep, input_raw, outputs_raw, is_event=False):
        try:
            if rep.serviceId == 0 and not self.service_list:
                service = RPCMessages_pb2.Connection()
                service_name_full = "Devialet.CallMeMaybe.Connection"
            else:
                service_name_full = [service.name for service in self.service_list if service.id == rep.serviceId][0]
                service_name = '.'.join(service_name_full.split('.')[:-1])
                while service_name not in self.service_by_name and len(service_name.split('.')) > 1:
                    service_name = '.'.join(service_name.split('.')[:-1])
                    print_info("truncating {} to {}".format(service_name_full, service_name))
                service = self.service_by_name[service_name]()

            service_desc = service.GetDescriptor()

            # if  or rep.isMultipart: rep.type == 1

            # Get Properties / No actual method
            if rep.subTypeId == 0xFFFFFFFF and rep.type == 1: # These should all be equivalent? Nope at least not for events
                print_info("PropertyGet details: {} / {} outputs, type={} subtype={}".format(
                    service_name_full, len(outputs_raw), rep.type, rep.subTypeId))
                if len(input_raw):
                    print_error('propertyget but input type not empty')
                outputs_pb = []
                for i, output_raw in enumerate(outputs_raw):
                    # prop = service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property[i]
                    prop = self.get_property(service_desc, i, output_raw)
                    outputs_pb.append(prop)
                    # print_data(prop.name, interpret_as(output_raw, prop.type))
                return (service_desc, descriptor_pb2.MethodDescriptorProto(), CallMeMaybe.CommonMessages_pb2.Empty(), outputs_pb)
            else:
                try:
                    method = service_desc.methods[rep.subTypeId]

                    print_info("RPC/Event details: {} -> {} [{} -> {}] {}".format(
                        service_name_full, method.full_name, method.input_type.full_name, method.output_type.full_name, method.output_type.full_name))

                    input_pb = service.GetRequestClass(method)()
                    input_pb.ParseFromString(input_raw)
                    if input_pb.FindInitializationErrors():
                        print_warning("There were uninitialized fields in input proto: {}", input_pb.FindInitializationErrors())

                    output_pb = service.GetResponseClass(method)()
                    output_pb.ParseFromString(outputs_raw[0])
                    if output_pb.FindInitializationErrors():
                        print_warning("There were uninitialized fields in output proto: {}", output_pb.FindInitializationErrors())
                    # input_pb = interpret_as(input_raw, method.input_type.full_name)
                    # output_pb = interpret_as(outputs_raw[0], method.output_type.full_name)
                    print_data("input  ({}):".format(method.input_type.full_name), input_pb)
                    print_data("output ({}):".format(method.output_type.full_name), output_pb)

                    if service.DESCRIPTOR.full_name == "Devialet.CallMeMaybe.Connection":
                        if method.name == "openConnection":
                            self.service_list = output_pb.services
                        if method.name == 'serviceAdded':
                            print_info("Extending list of services")
                            self.service_list.add(name=input_pb.name, id=input_pb.id)


                    return(service_desc, method, input_pb, [output_pb])
                except IndexError as e:
                    print_error("{} too big for {} that has only {} methods: {}", rep.subTypeId, service_desc.full_name, len(service_desc.methods), e)
                except message.DecodeError as e:
                    print_error('Failed to decode incoming or outgoing protobuf: {}', e)
        except IndexError:
            print_error('Service ID {} not in list {}', rep.serviceId, ' '.join(str(self.service_list).split('\n')))
        except KeyError:
            print_error("Can't find service {} in database", service_name)
        return (descriptor_pb2.ServiceDescriptorProto(), descriptor_pb2.MethodDescriptorProto(), CallMeMaybe.CommonMessages_pb2.Empty(), [])


    def find_method(self, rep):
        method = {'name': 'not found'}
        service = {'name': 'not found'}
        package = {'package_name': 'not found'}
        service_name_full = ""

        # if not(self.service_list):
        if rep.serviceId == 0 and not self.service_list:
            # Assume initial service is CallmeMaybe.Connection, which is placed first
            package = self.all_services_old[0]
            service = package['services'][rep.type]
            method = service['methods'][rep.subTypeId]

        elif rep.serviceId in [service.id for service in self.service_list]:
            service_name_full = [service.name for service in self.service_list if service.id == rep.serviceId][0]
            # package_name = '.'.join(service_name.split('.')[1:-2])
            # service_name = '.'.join(service_name.split('.')[-2:-1])
            package_name, service_name = re.match(
                '^[^\.]+\.(.*?)(?:-0)?\.([^\.]+?)(?:-0)?\.[^\.]+$', service_name_full).groups()
            # this isnt perfect, apparently sometimes more than one service: com.devialet.getthepartystarted.configuration-0.player-0.ece3ce2e

            # print(package_name, service_name)
            
            for p in self.all_services_old:
                if p['package_name'].lower() == package_name:
                    for s in p['services']:
                        if s['name'].lower() == service_name:
                            # for m in s['methods']:
                            #     if m['name'] == 
                            service = s
                            package = p
                            print_warning('service {} from {} appears to correspond to type {}, subtype {} ({})',
                                service_name, package_name, rep.type, rep.subTypeId, service_name_full
                            )
                            try:
                                method = service['methods'][rep.subTypeId]
                            except IndexError:
                                print_error('subTypeId {} too big for {} ({}->{})', 
                                    rep.subTypeId, service_name_full, package_name, service_name
                                )
            if package == {} or service == {}:
                print_error('service "{}" or package "{}" not found in database', service_name, package_name)
        else:
            print_error('Unknown service ID {}', rep.serviceId)

        return (service_name_full, package, service, method)

    def find_and_extend_services(self):
        self.all_services = [
            # First one should always be Connection
            RPCMessages_pb2.Connection,
            SaveMe.SaveMe_pb2.SavePlaylist,
            WhatsUp_pb2.Registrar,
            WhatsUp_pb2.Registry,
            MasterOfPuppets.Configuration_pb2.Configuration,
            AppleAirPlay.Playback_pb2.Playback,
            LeftAlone.Configuration_pb2.Configuration,
            TwerkIt.SoundDesign_pb2.SoundDesign,
            TheSoundOfSilence.OnlineSource_pb2.AuthenticatedOnlineSource,
            TheSoundOfSilence.OnlineSource_pb2.OnlineSourceSession,
            TheSoundOfSilence.LiveSource_pb2.LiveSourceSession,
            TheSoundOfSilence.LiveSource_pb2.LiveSource,
            TheSoundOfSilence.Source_pb2.SourceSession,
            TheSoundOfSilence.Source_pb2.ConfigureSource,
            TheSoundOfSilence.Source_pb2.Source,
            TooManyFlows.Playback_pb2.Playback,
            TooManyFlows.Playlist_pb2.Playlist,
            TooManyFlows.History_pb2.History,
            TooManyFlows.SoundControl_pb2.SoundControl,
            TooManyFlows.Configuration_pb2.Configuration,
            TooManyFlows.Metadata_pb2.Metadata,
            TooManyFlows.SoundDesign_pb2.SoundDesign,
            Fresh.Fresh_pb2.Update,
            Fresh.Fresh_pb2.SlaveUpdate,
            Fresh.Fresh_pb2.MasterUpdate,
            IMASlave4U.SoundControl_pb2.SoundControl,
            IMASlave4U.Configuration_pb2.Configuration,
            IMASlave4U.SoundDesign_pb2.SoundDesign,
            SpotifyConnect.SpotifyConnect_pb2.Agent,
            GetThePartyStarted.Player_pb2.Configuration,
            GetThePartyStarted.Player_pb2.Setup,
            GetThePartyStarted.GetThePartyStarted_pb2.Configuration,
            GetThePartyStarted.GetThePartyStarted_pb2.Setup,
            GetThePartyStarted.GetThePartyStarted_pb2.SlaveDeviceSetup,
            GetThePartyStarted.GetThePartyStarted_pb2.AttachedSlaveDeviceSetup,
            GetThePartyStarted.GetThePartyStarted_pb2.RemoteSlaveDeviceSetup,
            GetThePartyStarted.GetThePartyStarted_pb2.MasterDeviceSetup,
            GetThePartyStarted.Logging_pb2.LogUploader,
            GetThePartyStarted.Aerobase_pb2.Configuration,
            GetThePartyStarted.Aerobase_pb2.Setup,
        ]

        self.all_files = [
            AppleAirPlay.Playback_pb2,
            CallMeMaybe.CallMeMaybe_pb2,
            CallMeMaybe.CommonMessages_pb2,
            Fresh.Fresh_pb2,
            GetThePartyStarted.Aerobase_pb2,
            GetThePartyStarted.GetThePartyStarted_pb2,
            GetThePartyStarted.Logging_pb2,
            GetThePartyStarted.Player_pb2,
            IMASlave4U.Configuration_pb2,
            IMASlave4U.SoundControl_pb2,
            IMASlave4U.SoundDesign_pb2,
            LeftAlone.Configuration_pb2,
            MasterOfPuppets.Configuration_pb2,
            RPCMessages_pb2,
            SaveMe.SaveMe_pb2,
            SpotifyConnect.SpotifyConnect_pb2,
            TheSoundOfSilence.Album_pb2,
            TheSoundOfSilence.Artist_pb2,
            TheSoundOfSilence.Category_pb2,
            TheSoundOfSilence.Collection_pb2,
            TheSoundOfSilence.LiveSource_pb2,
            TheSoundOfSilence.Node_pb2,
            TheSoundOfSilence.OnlineSource_pb2,
            TheSoundOfSilence.Picture_pb2,
            TheSoundOfSilence.Playlist_pb2,
            TheSoundOfSilence.Session_pb2,
            TheSoundOfSilence.Source_pb2,
            TheSoundOfSilence.Subcategory_pb2,
            TheSoundOfSilence.TrackDetails_pb2,
            TheSoundOfSilence.Track_pb2,
            TooManyFlows.Configuration_pb2,
            TooManyFlows.History_pb2,
            TooManyFlows.Identifier_pb2,
            TooManyFlows.Metadata_pb2,
            TooManyFlows.Playback_pb2,
            TooManyFlows.Playlist_pb2,
            TooManyFlows.SoundControl_pb2,
            TooManyFlows.SoundDesign_pb2,
            TwerkIt.SoundDesign_pb2,
            WhatsUp_pb2,
        ]

        # lowercase name with -0 for inheritance
        self.service_by_name = {}
        # Class name
        self.service_by_full_name = {}
        for service in self.all_services:
            self.service_by_name[service.GetDescriptor().GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].serviceName] = service
            self.service_by_full_name[service.GetDescriptor().full_name] = service

        for service_name, service in self.service_by_full_name.items():
            # props = service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property

            opts = service.GetDescriptor().GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions]
            service_properties = opts.properties

            new_props = CallMeMaybe.CallMeMaybe_pb2.ServiceProperties()
            # new_props.MergeFrom(service_properties)
            # new_props.Clear()
            # extend left or right? maybe left, because of the bad output types
            baseservice_name = opts.baseService
            while baseservice_name in self.service_by_full_name:
                baseservice_opts = self.service_by_full_name[baseservice_name].GetDescriptor().GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions]
                base_props = baseservice_opts.properties

                
                # Extend Right
                # props.extend(base_props)

                # Extend Left
                # base_props.extend(props)
                # props = base_props

                new_props.Clear()
                new_props.MergeFrom(base_props)
                # new_props.property.extend(service_properties.property)
                for prop in service_properties.property:
                    if prop.name not in [p.name for p in new_props.property]:
                        new_props.property.add()
                        new_props.property[-1].MergeFrom(prop)
                    else:
                        # print("Duplicate property {} not added".format(prop.name))
                        pass

                service_properties.CopyFrom(new_props)

                # print("Extending props {} with {} : {}".format(service_name, baseservice_name, [p.name for p in service_properties.property]))

                baseservice_name = baseservice_opts.baseService

            # service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.Clear()
            # service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property.MergeFrom(props)

        # pprint(self.service_by_name)
        