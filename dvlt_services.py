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

from google.protobuf import descriptor_pb2

from dvlt_messages import interpret_as, heuristic_search

def get_property(service_desc, property_id, output_raw):
    props = service_desc \
            .GetOptions() \
            .Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions] \
            .properties \
            .property
    try:
        # print("Trying to get property {} from {}".format(property_id, service_desc.full_name))
        # return props[property_id]
        prop = interpret_as(output_raw, props[property_id].type)
        print("* {}: {{ {} }}".format(props[property_id].name, prop))
        return prop
    except IndexError:
        print("Error: Too many multiparts for propertyget({}), {} >= {}".format(
            service_desc.full_name, property_id, len(props)))
        return CallMeMaybe.CommonMessages_pb2.Empty()

def process_rpc(rep, service_list, input_raw, outputs_raw, is_event=False):
    print("PROCESS RPC---->")
    try:
        if rep.serviceId == 0 and not service_list:
            service = RPCMessages_pb2.Connection()
            service_name_full = "Devialet.CallMeMaybe.Connection"
        else:
            service_name_full = [service.name for service in service_list if service.id == rep.serviceId][0]
            service_name = '.'.join(service_name_full.split('.')[:-1])
            while service_name not in service_by_name and len(service_name.split('.')) > 1:
                service_name = '.'.join(service_name.split('.')[:-1])
                print("truncating {} to {}".format(service_name_full, service_name))
            service = service_by_name[service_name]()

        service_desc = service.GetDescriptor()
        # try:
        #     # TODO: Handle baseService

        #     # Could also use the -0 and get parent that way?
        #     # baseservice_desc = service_by_full_name[service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].baseService].GetDescriptor()

        #     # desc = descriptor_pb2.ServiceDescriptorProto()
        #     # service_desc.CopyToProto(desc)
        #     # baseservice_desc.CopyToProto(desc)
            
        #     props = service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property

        #         # # extend left or right? maybe left, because of the bad output types
        #         # baseservice_name = service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].baseService
        #         # while baseservice_name in service_by_full_name:
        #         #     baseservice_desc = service_by_full_name[baseservice_name].GetDescriptor()
        #         #     base_props = baseservice_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property

        #         #     print("Extending props {} with {} : {}".format(service_desc.full_name, baseservice_name, props))
        #         #     # Extend Right
        #         #     # props.extend(base_props)

        #         #     # Extend Left
        #         #     base_props.extend(props)
        #         #     props = base_props

        #         #     baseservice_name = baseservice_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].baseService

        #         # service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.Clear()
        #         # service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property.MergeFrom(props)

        #     # print("Extended props {}".format(service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property))
        #     # base_props.extend(props)
        #     # props = base_props
        #     # service_desc = desc

        #     # print("Successfully extended {} with {}".format(service_desc.full_name, baseservice_name))
        #     # desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property.extend(service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property)
        # except Exception as e:
        #     print("Error: trying to extend service with baseservice: {} {}".format(type(e), e))

        # if  or rep.isMultipart: rep.type == 1

        # Get Properties / No actual method
        if rep.subTypeId == 0xFFFFFFFF and rep.type == 1: # These should all be equivalent? Nope at least not for events
            print("PropertyGet details: {} / {} outputs, type={} subtype={}".format(
                service_name_full, len(outputs_raw), rep.type, rep.subTypeId))
            if len(input_raw):
                print("Error: propertyget but input type not empty")
            outputs_pb = []
            for i, output_raw in enumerate(outputs_raw):
                # prop = service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property[i]
                prop = get_property(service_desc, i, output_raw)
                outputs_pb.append(prop)
                # print(prop.name, interpret_as(output_raw, prop.type))
            return (service_desc, descriptor_pb2.MethodDescriptorProto(), CallMeMaybe.CommonMessages_pb2.Empty(), outputs_pb)
        else:
            try:
                method = service_desc.methods[rep.subTypeId]

                print("RPC/Event details: {} -> {} [{} -> {}] {}".format(
                    service_name_full, method.full_name, method.input_type.full_name, method.output_type.full_name, method.output_type.full_name))

                input_pb = service.GetRequestClass(method)()
                input_pb.ParseFromString(input_raw)

                output_pb = service.GetResponseClass(method)()
                output_pb.ParseFromString(outputs_raw[0])
                # input_pb = interpret_as(input_raw, method.input_type.full_name)
                # output_pb = interpret_as(outputs_raw[0], method.output_type.full_name)
                print(input_pb)
                print(output_pb)

                return(service_desc, method, input_pb, [output_pb])
            except IndexError as e:
                print("Error: {} too big for {} that has only {} methods: {}".format(rep.subTypeId, service_desc.full_name, len(service_desc.methods), e))
    except IndexError:
        print("Error: Service ID {} not in list {}".format(rep.serviceId, ' '.join(str(service_list).split('\n'))))
    except KeyError:
        print("Error: Can't find service {} in database".format(service_name))
    print('<---------')
    return (descriptor_pb2.ServiceDescriptorProto(), descriptor_pb2.MethodDescriptorProto(), CallMeMaybe.CommonMessages_pb2.Empty(), [])


def find_method(rep, service_list):
    method = {'name': 'not found'}
    service = {'name': 'not found'}
    package = {'package_name': 'not found'}
    service_name_full = ""

    # if not(service_list):
    if rep.serviceId == 0 and not service_list:
        # Assume initial service is CallmeMaybe.Connection, which is placed first
        package = all_services_old[0]
        service = package['services'][rep.type]
        method = service['methods'][rep.subTypeId]

    elif rep.serviceId in [service.id for service in service_list]:
        service_name_full = [service.name for service in service_list if service.id == rep.serviceId][0]
        # package_name = '.'.join(service_name.split('.')[1:-2])
        # service_name = '.'.join(service_name.split('.')[-2:-1])
        package_name, service_name = re.match(
            '^[^\.]+\.(.*?)(?:-0)?\.([^\.]+?)(?:-0)?\.[^\.]+$', service_name_full).groups()
        # this isnt perfect, apparently sometimes more than one service: com.devialet.getthepartystarted.configuration-0.player-0.ece3ce2e

        # print(package_name, service_name)
        
        for p in all_services_old:
            if p['package_name'].lower() == package_name:
                for s in p['services']:
                    if s['name'].lower() == service_name:
                        # for m in s['methods']:
                        #     if m['name'] == 
                        service = s
                        package = p
                        print('service {} from {} appears to correspond to type {}, subtype {} ({})'.format(
                            service_name, package_name, rep.type, rep.subTypeId, service_name_full
                        ))
                        try:
                            method = service['methods'][rep.subTypeId]
                        except IndexError:
                            print("Error: subTypeId {} too big for {} ({}->{})".format(
                                rep.subTypeId, service_name_full, package_name, service_name
                            ))
        if package == {} or service == {}:
            print('Error: service "{}" or package "{}" not found in database'.format(service_name, package_name))
    else:
        print("Error: Unknown service ID {}".format(rep.serviceId))

    return (service_name_full, package, service, method)

all_services = [
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

all_files = [
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
service_by_name = {}
# Class name
service_by_full_name = {}
for service in all_services:
    service_by_name[service.GetDescriptor().GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].serviceName] = service
    service_by_full_name[service.GetDescriptor().full_name] = service

for service_name, service in service_by_full_name.items():
    # props = service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property

    opts = service.GetDescriptor().GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions]
    service_properties = opts.properties

    new_props = CallMeMaybe.CallMeMaybe_pb2.ServiceProperties()
    # new_props.MergeFrom(service_properties)
    # new_props.Clear()
    # extend left or right? maybe left, because of the bad output types
    baseservice_name = opts.baseService
    while baseservice_name in service_by_full_name:
        baseservice_opts = service_by_full_name[baseservice_name].GetDescriptor().GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions]
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
                print("Duplicate property {} not added".format(prop.name))

        service_properties.CopyFrom(new_props)

        print("Extending props {} with {} : {}".format(service_name, baseservice_name, [p.name for p in service_properties.property]))

        baseservice_name = baseservice_opts.baseService

    # service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.Clear()
    # service_desc.GetOptions().Extensions[CallMeMaybe.CallMeMaybe_pb2.dvltServiceOptions].properties.property.MergeFrom(props)

pprint(service_by_name)
    

all_services_old = [
    # First one should always be CallMeMaybe
    {
        "package_name": "Devialet.CallMeMaybe",
        "services": [
            {
                "name": "Connection",
                "methods": [
                    {
                        "name": "openConnection",
                        "input_type": "Devialet.CallMeMaybe.ConnectionRequest",
                        "output_type": "Devialet.CallMeMaybe.ConnectionReply",
                    },
                    {
                        "name": "ping",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "serviceAdded",
                        "input_type": "Devialet.CallMeMaybe.Service",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "serviceRemoved",
                        "input_type": "Devialet.CallMeMaybe.Service",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "serverQuit",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.WhatsUp",
        "services": [
            {
                "name": "Registrar",
                "methods": [
                    {
                        "name": "registerServer",
                        "input_type": "Devialet.WhatsUp.RegistrarRegisterQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "unregisterServer",
                        "input_type": "Devialet.WhatsUp.RegistrarUnregisterQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "addServices",
                        "input_type": "Devialet.WhatsUp.RegistrarServicesQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "removeServices",
                        "input_type": "Devialet.WhatsUp.RegistrarServicesQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "ping",
                        "input_type": "Devialet.WhatsUp.RegistrarPingQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pingRequested",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "Registry",
                "methods": [
                    {
                        "name": "getNetworkConfiguration",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.WhatsUp.WhatsUpHost",
                    },
                    {
                        "name": "listHosts",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.WhatsUp.WhatsUpHostsList",
                    },
                    {
                        "name": "lookupHost",
                        "input_type": "Devialet.WhatsUp.RegistryLookupHostQuery",
                        "output_type": "Devialet.WhatsUp.RegistryLookupHostReply",
                    },
                    {
                        "name": "listServices",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.WhatsUp.WhatsUpServicesList",
                    },
                    {
                        "name": "findServices",
                        "input_type": "Devialet.WhatsUp.RegistryFindServicesQuery",
                        "output_type": "Devialet.WhatsUp.WhatsUpServicesList",
                    },
                    {
                        "name": "networkConfigurationChanged",
                        "input_type": "Devialet.WhatsUp.RegistryNetworkConfigurationChangedNotification",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "hostUpdated",
                        "input_type": "Devialet.WhatsUp.RegistryHostUpdatedNotification",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "servicesAdded",
                        "input_type": "Devialet.WhatsUp.WhatsUpServicesList",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "servicesUpdated",
                        "input_type": "Devialet.WhatsUp.WhatsUpServicesUpdate",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "servicesRemoved",
                        "input_type": "Devialet.WhatsUp.WhatsUpServicesRemoval",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.AppleAirPlay",
        "services": [
            {
                "name": "Playback",
                "methods": [
                    {
                        "name": "play",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pause",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "next",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "previous",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "toggleRepeat",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "toggleShuffle",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "stop",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "togglePause",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.TooManyFlows",
        "services": [
            { "name": "Metadata", "methods": [] },
            {
                "name": "Configuration",
                "methods": [
                    {
                        "name": "addPlayer",
                        "input_type": "Devialet.TooManyFlows.PlayerId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "addRenderer",
                        "input_type": "Devialet.TooManyFlows.AddRendererQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "removePlayer",
                        "input_type": "Devialet.TooManyFlows.PlayerId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "removeRenderer",
                        "input_type": "Devialet.TooManyFlows.RendererId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "reset",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "autoSwitch",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.BoolProperty",
                    },
                    {
                        "name": "setAutoSwitch",
                        "input_type": "Devialet.CallMeMaybe.BoolProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            { "name": "SoundDesign", "methods": [] },
            {
                "name": "SoundControl",
                "methods": [
                    {
                        "name": "setBouquetMute",
                        "input_type": "Devialet.TooManyFlows.Mute",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setGroupMute",
                        "input_type": "Devialet.TooManyFlows.GroupMute",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setRendererMute",
                        "input_type": "Devialet.TooManyFlows.RendererMute",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setBouquetNightMode",
                        "input_type": "Devialet.TooManyFlows.NightMode",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setGroupNightMode",
                        "input_type": "Devialet.TooManyFlows.GroupNightMode",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setRendererNightMode",
                        "input_type": "Devialet.TooManyFlows.RendererNightMode",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setBouquetVolume",
                        "input_type": "Devialet.TooManyFlows.Volume",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setGroupVolume",
                        "input_type": "Devialet.TooManyFlows.GroupVolume",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setRendererVolume",
                        "input_type": "Devialet.TooManyFlows.RendererVolume",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "bouquetMuteChanged",
                        "input_type": "Devialet.TooManyFlows.Mute",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "groupMuteChanged",
                        "input_type": "Devialet.TooManyFlows.GroupMute",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererMuteChanged",
                        "input_type": "Devialet.TooManyFlows.RendererMute",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "bouquetNightModeChanged",
                        "input_type": "Devialet.TooManyFlows.NightMode",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "groupNightModeChanged",
                        "input_type": "Devialet.TooManyFlows.GroupNightMode",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererNightModeChanged",
                        "input_type": "Devialet.TooManyFlows.RendererNightMode",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "bouquetVolumeChanged",
                        "input_type": "Devialet.TooManyFlows.Volume",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "groupVolumeChanged",
                        "input_type": "Devialet.TooManyFlows.GroupVolume",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererVolumeChanged",
                        "input_type": "Devialet.TooManyFlows.RendererVolume",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setBouquetVolumeByDelta",
                        "input_type": "Devialet.CallMeMaybe.DoubleProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "History",
                "methods": [
                    {
                        "name": "clear",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "cleared",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "trackPopped",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "trackPushed",
                        "input_type": "Devialet.TooManyFlows.UrlMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "Playlist",
                "methods": [
                    {
                        "name": "clear",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "insert",
                        "input_type": "Devialet.TooManyFlows.TracksMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "move",
                        "input_type": "Devialet.TooManyFlows.MoveMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "remove",
                        "input_type": "Devialet.TooManyFlows.TracksMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "cleared",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "tracksAdded",
                        "input_type": "Devialet.TooManyFlows.TracksMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "trackMoved",
                        "input_type": "Devialet.TooManyFlows.MoveMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "tracksRemoved",
                        "input_type": "Devialet.TooManyFlows.TracksMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "Playback",
                "methods": [
                    {
                        "name": "at",
                        "input_type": "Devialet.TooManyFlows.IndexMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "next",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pause",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "play",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "prev",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "seek",
                        "input_type": "Devialet.TooManyFlows.SeekMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "stop",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "playUrl",
                        "input_type": "Devialet.CallMeMaybe.StringProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.GetThePartyStarted.Player",
        "services": [
            { "name": "Configuration", "methods": [] },
            {
                "name": "Setup",
                "methods": [
                    {
                        "name": "startStandaloneSetup",
                        "input_type": "Devialet.GetThePartyStarted.StartSetupRequest",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "listWiFiNetworks",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.GetThePartyStarted.Player.ListWiFiNetworksReply",
                    },
                    {
                        "name": "enableStandaloneAccessPoint",
                        "input_type": "Devialet.GetThePartyStarted.Player.EnableStandaloneAccessPointRequest",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "configureBouquet",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "configureServices",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "enableOpticalDirectMode",
                        "input_type": "Devialet.GetThePartyStarted.Player.OpticalModeParameters",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "enableMotionDesignMode",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "enableAppleWacAccessPoint",
                        "input_type": "Devialet.GetThePartyStarted.Player.AppleWacAccessPointConfiguration",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "disableAppleWacAccessPoint",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "joinDestinationWiFiNetwork",
                        "input_type": "Devialet.GetThePartyStarted.Player.AppleWacWiFiNetworkConfiguration",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "destinationWiFiNetworkJoined",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "wasDestinationWiFiNetworkJoined",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.BoolProperty",
                    },
                    {
                        "name": "applyDeviceName",
                        "input_type": "Devialet.CallMeMaybe.StringProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "completeConfiguration",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.IMASlave4",
        "services": [
            { "name": "SoundControl", "methods": [] },
            { "name": "Configuration", "methods": [] },
            { "name": "SoundDesign", "methods": [] },
        ],
    },
    {
        "package_name": "Devialet.GetThePartyStarted",
        "services": [
            {
                "name": "Configuration",
                "methods": [
                    {
                        "name": "powerStandby",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "powerSuspend",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "powerOff",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "powerReboot",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "enableSetup",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "resetToFactory",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "checkForUpdate",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "Setup",
                "methods": [
                    {
                        "name": "startSetup",
                        "input_type": "Devialet.GetThePartyStarted.StartSetupRequest",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "cancelSetup",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "completeSetup",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            { "name": "SlaveDeviceSetup", "methods": [] },
            {
                "name": "LogUploader",
                "methods": [
                    {
                        "name": "uploadLogs",
                        "input_type": "Devialet.GetThePartyStarted.UploadLogsRequest",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.GetThePartyStarted.Aerobase",
        "services": [
            { "name": "Configuration", "methods": [] },
            {
                "name": "Setup",
                "methods": [
                    {
                        "name": "configureTopology",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "setTopologyConfiguration",
                        "input_type": "Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "configureServices",
                        "input_type": "Devialet.GetThePartyStarted.SetupToken",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.AudioSource",
        "services": [
            {
                "name": "LiveSourceSession",
                "methods": [
                    {
                        "name": "picture",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.AudioSource.Picture",
                    },
                    {
                        "name": "defaultVolume",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.DoubleProperty",
                    },
                ],
            },
            {
                "name": "LiveSource",
                "methods": [
                    {
                        "name": "loadSession",
                        "input_type": "Devialet.AudioSource.LoadSessionQuery",
                        "output_type": "Devialet.AudioSource.Session",
                    },
                    {
                        "name": "unloadSession",
                        "input_type": "Devialet.AudioSource.UnloadSessionQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "AuthenticatedOnlineSource",
                "methods": [
                    {
                        "name": "credentialsLogin",
                        "input_type": "Devialet.AudioSource.CredentialsLoginRequest",
                        "output_type": "Devialet.AudioSource.LoginReply",
                    },
                    {
                        "name": "oAuthLogin",
                        "input_type": "Devialet.AudioSource.OAuthLoginRequest",
                        "output_type": "Devialet.AudioSource.LoginReply",
                    },
                    {
                        "name": "logout",
                        "input_type": "Devialet.AudioSource.LogoutRequest",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "SourceSession",
                "methods": [
                    {
                        "name": "uri",
                        "input_type": "Devialet.AudioSource.Id",
                        "output_type": "Devialet.AudioSource.Uri",
                    },
                ],
            },
            {
                "name": "ConfigureSource",
                "methods": [
                    {
                        "name": "setEnabled",
                        "input_type": "Devialet.AudioSource.Enabled",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            {
                "name": "Source",
                "methods": [
                    {
                        "name": "logo",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.AudioSource.Picture",
                    },
                    {
                        "name": "sessionAdded",
                        "input_type": "Devialet.AudioSource.Session",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "sessionRemoved",
                        "input_type": "Devialet.AudioSource.SessionId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "bigLogo",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.AudioSource.Picture",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.Fresh",
        "services": [
            {
                "name": "Update",
                "methods": [
                    {
                        "name": "checkForUpdate",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "downloadUpdate",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "installUpdate",
                        "input_type": "Devialet.Fresh.InstallUpdateRequest",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "cancelUpdateInstallation",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "updateDownloadProgress",
                        "input_type": "Devialet.Fresh.UpdateDownloadProgress",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "updateDownloadFailed",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
            { "name": "SlaveUpdate", "methods": [] },
            { "name": "MasterUpdate", "methods": [] },
        ],
    },
    {
        "package_name": "Devialet.LeftAlone",
        "services": [ { "name": "Configuration", "methods": [] } ],
    },
    {
        "package_name": "Devialet.TwerkIt",
        "services": [
            {
                "name": "SoundDesign",
                "methods": [
                    {
                        "name": "allDeviceDone",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "allDevicesConnected",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "allDevicesGrouped",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "allInputsSetup",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pacoSelectedChannel",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pacoSelectedGroup",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pacoSelectedOptical",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "receivedNetworkSettings",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "remotePaired",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pacoHappy",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pacoUnhappy",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "demoPulse",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "demoSlowMotion",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "demoWave",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "disconnected",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.SpotifyConnect",
        "services": [
            {
                "name": "Agent",
                "methods": [
                    {
                        "name": "handleZeroConfApiRequest",
                        "input_type": "Devialet.SpotifyConnect.ZeroConfApiRequest",
                        "output_type": "Devialet.SpotifyConnect.ZeroConfApiReply",
                    },
                    {
                        "name": "setBouquetId",
                        "input_type": "Devialet.CallMeMaybe.BytesProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "play",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "pause",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "next",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "previous",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "repeat",
                        "input_type": "Devialet.CallMeMaybe.BoolProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "shuffle",
                        "input_type": "Devialet.CallMeMaybe.BoolProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "seek",
                        "input_type": "Devialet.CallMeMaybe.UInt32Property",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.SaveMe",
        "services": [
            {
                "name": "SavePlaylist",
                "methods": [
                    {
                        "name": "create",
                        "input_type": "Devialet.SaveMe.CreatePlaylist",
                        "output_type": "Devialet.CallMeMaybe.BytesProperty",
                    },
                    {
                        "name": "remove",
                        "input_type": "Devialet.CallMeMaybe.BytesProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "clear",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "tracks",
                        "input_type": "Devialet.CallMeMaybe.BytesProperty",
                        "output_type": "Devialet.SaveMe.PlaylistContent",
                    },
                    {
                        "name": "addTracks",
                        "input_type": "Devialet.SaveMe.ModifyTracks",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "removeTrack",
                        "input_type": "Devialet.SaveMe.ModifyOneTrack",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "edit",
                        "input_type": "Devialet.SaveMe.ModifyPlaylistName",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "playlistAdded",
                        "input_type": "Devialet.SaveMe.PlaylistMsg",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "playlistRemoved",
                        "input_type": "Devialet.CallMeMaybe.BytesProperty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "cleared",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "tracksAdded",
                        "input_type": "Devialet.SaveMe.ModifyTracks",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "trackRemoved",
                        "input_type": "Devialet.SaveMe.ModifyOneTrack",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "playlistEdited",
                        "input_type": "Devialet.SaveMe.ModifyPlaylistName",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
    {
        "package_name": "Devialet.MasterOfPuppets",
        "services": [
            {
                "name": "Configuration",
                "methods": [
                    {
                        "name": "addBouquet",
                        "input_type": "Devialet.CallMeMaybe.Empty",
                        "output_type": "Devialet.MasterOfPuppets.BouquetId",
                    },
                    {
                        "name": "removeBouquet",
                        "input_type": "Devialet.MasterOfPuppets.BouquetId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "addGroup",
                        "input_type": "Devialet.MasterOfPuppets.AddGroupQuery",
                        "output_type": "Devialet.MasterOfPuppets.GroupId",
                    },
                    {
                        "name": "isolateGroup",
                        "input_type": "Devialet.MasterOfPuppets.GroupId",
                        "output_type": "Devialet.MasterOfPuppets.BouquetId",
                    },
                    {
                        "name": "moveGroup",
                        "input_type": "Devialet.MasterOfPuppets.MoveGroupQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "removeGroup",
                        "input_type": "Devialet.MasterOfPuppets.GroupId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "renameGroup",
                        "input_type": "Devialet.MasterOfPuppets.RenameQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "addRenderer",
                        "input_type": "Devialet.MasterOfPuppets.AddRendererQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "moveRenderer",
                        "input_type": "Devialet.MasterOfPuppets.MoveRendererQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "removeRenderer",
                        "input_type": "Devialet.MasterOfPuppets.RendererId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "renameRenderer",
                        "input_type": "Devialet.MasterOfPuppets.RenameQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "bouquetAdded",
                        "input_type": "Devialet.MasterOfPuppets.BouquetAddedNotification",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "bouquetRemoved",
                        "input_type": "Devialet.MasterOfPuppets.BouquetId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "bouquetRenamed",
                        "input_type": "Devialet.MasterOfPuppets.RenameQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "groupAdded",
                        "input_type": "Devialet.MasterOfPuppets.GroupAddedNotification",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "groupMoved",
                        "input_type": "Devialet.MasterOfPuppets.MoveGroupQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "groupRemoved",
                        "input_type": "Devialet.MasterOfPuppets.GroupId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "groupRenamed",
                        "input_type": "Devialet.MasterOfPuppets.RenameQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererAdded",
                        "input_type": "Devialet.MasterOfPuppets.RendererAddedNotification",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererMoved",
                        "input_type": "Devialet.MasterOfPuppets.MoveRendererQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererRemoved",
                        "input_type": "Devialet.MasterOfPuppets.RendererId",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererRenamed",
                        "input_type": "Devialet.MasterOfPuppets.RenameQuery",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                    {
                        "name": "rendererStateChanged",
                        "input_type": "Devialet.MasterOfPuppets.StateNotification",
                        "output_type": "Devialet.CallMeMaybe.Empty",
                    },
                ],
            },
        ],
    },
];
