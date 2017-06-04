import SaveMe.SaveMe_pb2
import WhatsUp_pb2
import google.protobuf.descriptor_pb2
import MasterOfPuppets.Configuration_pb2
import AppleAirPlay.Playback_pb2
import LeftAlone.Configuration_pb2
import TwerkIt.SoundDesign_pb2
import TheSoundOfSilence.Playlist_pb2
import TheSoundOfSilence.OnlineSource_pb2
import TheSoundOfSilence.Artist_pb2
import TheSoundOfSilence.LiveSource_pb2
import TheSoundOfSilence.Session_pb2
import TheSoundOfSilence.Subcategory_pb2
import TheSoundOfSilence.Source_pb2
import TheSoundOfSilence.Node_pb2
import TheSoundOfSilence.TrackDetails_pb2
import TheSoundOfSilence.Collection_pb2
import TheSoundOfSilence.Picture_pb2
import TheSoundOfSilence.Album_pb2
import TheSoundOfSilence.Category_pb2
import TheSoundOfSilence.Track_pb2
import TooManyFlows.Playback_pb2
import TooManyFlows.Playlist_pb2
import TooManyFlows.History_pb2
import TooManyFlows.SoundControl_pb2
import TooManyFlows.Configuration_pb2
import TooManyFlows.Metadata_pb2
import TooManyFlows.SoundDesign_pb2
import TooManyFlows.Identifier_pb2
import Fresh.Fresh_pb2
import IMASlave4U.SoundControl_pb2
import IMASlave4U.Configuration_pb2
import IMASlave4U.SoundDesign_pb2
import RPCMessages_pb2
import SpotifyConnect.SpotifyConnect_pb2
import CallMeMaybe.CallMeMaybe_pb2
import CallMeMaybe.CommonMessages_pb2
import GetThePartyStarted.Player_pb2
import GetThePartyStarted.GetThePartyStarted_pb2
import GetThePartyStarted.Logging_pb2
import GetThePartyStarted.Aerobase_pb2

import subprocess
from protobuf_to_dict import protobuf_to_dict
from dvlt_output import *

def interpret_as(raw_protobuf, proto_name):
    try:
        ret = all_msgs[proto_name]()
        ret.ParseFromString(raw_protobuf)
        if ret.FindInitializationErrors():
            print_warning("There were uninitialized fields in pb of type {}: {}",
                          proto_name, ret.FindInitializationErrors())
        return ret
    except Exception as e:
        print("Error: Can't interpret protobuf {{{}}} as {}: {}".format(
            ' '.join(raw_decode(raw_protobuf)['protoc'].split('\n')), proto_name, e))
        print(heuristic_search(raw_protobuf))
        pass
    return None

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
            "raw": data,
            "protoc": process.stdout.read().decode()
        }
    else:
        return {
            "raw": data,
            "protoc": "",
            "error": 'Failed to parse: ' + ' '.join('{:02x}'.format(x) for x in data)
        }

def heuristic_search(raw_protobuf, filter="", strict=True):
    results = {}
    if len(raw_protobuf) == 0:
        return { "empty protobuf" }
    for proto in all_msgs:
        if proto.startswith(filter):
            try:
                tmp = all_msgs[proto]()
                tmp.ParseFromString(raw_protobuf)
                results[proto] = full_len(protobuf_to_dict(tmp))
                if strict and len(tmp.FindInitializationErrors()) > 0:
                    results[proto] = -1
            except Exception as e:
                # print("Error in heuristic:",    type(e), e)
                results[proto] = -1
                # pass
        else:
            results[proto] = -1
    # return [[proto, length] for (proto, length) in results.items()]
    return sorted([(proto, length) for (proto, length) in  results.items() if length > 2 and (length > 0 or length > max(results[x] for x in results)/2)
        ], key=lambda x:x[1]) 

all_msgs = {
    "Devialet.SaveMe.SavePlaylistError": SaveMe.SaveMe_pb2.SavePlaylistError,
    "Devialet.SaveMe.Track": SaveMe.SaveMe_pb2.Track,
    "Devialet.SaveMe.PlaylistMsg": SaveMe.SaveMe_pb2.PlaylistMsg,
    "Devialet.SaveMe.TrackInPlaylist": SaveMe.SaveMe_pb2.TrackInPlaylist,
    "Devialet.SaveMe.CreatePlaylist": SaveMe.SaveMe_pb2.CreatePlaylist,
    "Devialet.SaveMe.PlaylistSaved": SaveMe.SaveMe_pb2.PlaylistSaved,
    "Devialet.SaveMe.PlaylistContent": SaveMe.SaveMe_pb2.PlaylistContent,
    "Devialet.SaveMe.ModifyTracks": SaveMe.SaveMe_pb2.ModifyTracks,
    "Devialet.SaveMe.ModifyOneTrack": SaveMe.SaveMe_pb2.ModifyOneTrack,
    "Devialet.SaveMe.ModifyPlaylistName": SaveMe.SaveMe_pb2.ModifyPlaylistName,
    "Devialet.WhatsUp.RegistrarRegisterQuery": WhatsUp_pb2.RegistrarRegisterQuery,
    "Devialet.WhatsUp.RegistrarUnregisterQuery": WhatsUp_pb2.RegistrarUnregisterQuery,
    "Devialet.WhatsUp.RegistrarServicesQuery": WhatsUp_pb2.RegistrarServicesQuery,
    "Devialet.WhatsUp.RegistrarPingQuery": WhatsUp_pb2.RegistrarPingQuery,
    "Devialet.WhatsUp.RegistrarErrors": WhatsUp_pb2.RegistrarErrors,
    "Devialet.WhatsUp.WhatsUpNetwork": WhatsUp_pb2.WhatsUpNetwork,
    "Devialet.WhatsUp.WhatsUpNetworkInterface": WhatsUp_pb2.WhatsUpNetworkInterface,
    "Devialet.WhatsUp.WhatsUpHost": WhatsUp_pb2.WhatsUpHost,
    "Devialet.WhatsUp.WhatsUpHostsList": WhatsUp_pb2.WhatsUpHostsList,
    "Devialet.WhatsUp.WhatsUpService": WhatsUp_pb2.WhatsUpService,
    "Devialet.WhatsUp.WhatsUpServicesList": WhatsUp_pb2.WhatsUpServicesList,
    "Devialet.WhatsUp.WhatsUpServicesUpdate": WhatsUp_pb2.WhatsUpServicesUpdate,
    "Devialet.WhatsUp.WhatsUpServicesRemoval": WhatsUp_pb2.WhatsUpServicesRemoval,
    "Devialet.WhatsUp.RegistryLookupHostQuery": WhatsUp_pb2.RegistryLookupHostQuery,
    "Devialet.WhatsUp.RegistryLookupHostReply": WhatsUp_pb2.RegistryLookupHostReply,
    "Devialet.WhatsUp.RegistryFindServicesQuery": WhatsUp_pb2.RegistryFindServicesQuery,
    "Devialet.WhatsUp.RegistryNetworkConfigurationChangedNotification": WhatsUp_pb2.RegistryNetworkConfigurationChangedNotification,
    "Devialet.WhatsUp.RegistryHostUpdatedNotification": WhatsUp_pb2.RegistryHostUpdatedNotification,
    "google.protobuf.FileDescriptorSet": google.protobuf.descriptor_pb2.FileDescriptorSet,
    "google.protobuf.FileDescriptorProto": google.protobuf.descriptor_pb2.FileDescriptorProto,
    "google.protobuf.DescriptorProto": google.protobuf.descriptor_pb2.DescriptorProto,
    "google.protobuf.FieldDescriptorProto": google.protobuf.descriptor_pb2.FieldDescriptorProto,
    "google.protobuf.OneofDescriptorProto": google.protobuf.descriptor_pb2.OneofDescriptorProto,
    "google.protobuf.EnumDescriptorProto": google.protobuf.descriptor_pb2.EnumDescriptorProto,
    "google.protobuf.EnumValueDescriptorProto": google.protobuf.descriptor_pb2.EnumValueDescriptorProto,
    "google.protobuf.ServiceDescriptorProto": google.protobuf.descriptor_pb2.ServiceDescriptorProto,
    "google.protobuf.MethodDescriptorProto": google.protobuf.descriptor_pb2.MethodDescriptorProto,
    "google.protobuf.FileOptions": google.protobuf.descriptor_pb2.FileOptions,
    "google.protobuf.MessageOptions": google.protobuf.descriptor_pb2.MessageOptions,
    "google.protobuf.FieldOptions": google.protobuf.descriptor_pb2.FieldOptions,
    "google.protobuf.EnumOptions": google.protobuf.descriptor_pb2.EnumOptions,
    "google.protobuf.EnumValueOptions": google.protobuf.descriptor_pb2.EnumValueOptions,
    "google.protobuf.ServiceOptions": google.protobuf.descriptor_pb2.ServiceOptions,
    "google.protobuf.MethodOptions": google.protobuf.descriptor_pb2.MethodOptions,
    "google.protobuf.UninterpretedOption": google.protobuf.descriptor_pb2.UninterpretedOption,
    "google.protobuf.SourceCodeInfo": google.protobuf.descriptor_pb2.SourceCodeInfo,
    "Devialet.MasterOfPuppets.GroupId": MasterOfPuppets.Configuration_pb2.GroupId,
    "Devialet.MasterOfPuppets.BouquetId": MasterOfPuppets.Configuration_pb2.BouquetId,
    "Devialet.MasterOfPuppets.RendererId": MasterOfPuppets.Configuration_pb2.RendererId,
    "Devialet.MasterOfPuppets.NodeRenderer": MasterOfPuppets.Configuration_pb2.NodeRenderer,
    "Devialet.MasterOfPuppets.NodeGroup": MasterOfPuppets.Configuration_pb2.NodeGroup,
    "Devialet.MasterOfPuppets.NodeBouquet": MasterOfPuppets.Configuration_pb2.NodeBouquet,
    "Devialet.MasterOfPuppets.NodeRoot": MasterOfPuppets.Configuration_pb2.NodeRoot,
    "Devialet.MasterOfPuppets.AddGroupQuery": MasterOfPuppets.Configuration_pb2.AddGroupQuery,
    "Devialet.MasterOfPuppets.AddRendererQuery": MasterOfPuppets.Configuration_pb2.AddRendererQuery,
    "Devialet.MasterOfPuppets.MoveGroupQuery": MasterOfPuppets.Configuration_pb2.MoveGroupQuery,
    "Devialet.MasterOfPuppets.MoveRendererQuery": MasterOfPuppets.Configuration_pb2.MoveRendererQuery,
    "Devialet.MasterOfPuppets.RenameQuery": MasterOfPuppets.Configuration_pb2.RenameQuery,
    "Devialet.MasterOfPuppets.BouquetAddedNotification": MasterOfPuppets.Configuration_pb2.BouquetAddedNotification,
    "Devialet.MasterOfPuppets.GroupAddedNotification": MasterOfPuppets.Configuration_pb2.GroupAddedNotification,
    "Devialet.MasterOfPuppets.RendererAddedNotification": MasterOfPuppets.Configuration_pb2.RendererAddedNotification,
    "Devialet.MasterOfPuppets.StateNotification": MasterOfPuppets.Configuration_pb2.StateNotification,
    "Devialet.AppleAirPlay.Dummy": AppleAirPlay.Playback_pb2.Dummy,
    "Devialet.LeftAlone.FakeMsg": LeftAlone.Configuration_pb2.FakeMsg,
    "Devialet.AudioSource.Playlist": TheSoundOfSilence.Playlist_pb2.Playlist,
    "Devialet.AudioSource.OnlineSourceError": TheSoundOfSilence.OnlineSource_pb2.OnlineSourceError,
    "Devialet.AudioSource.OnlineSourceAvailableMethods": TheSoundOfSilence.OnlineSource_pb2.OnlineSourceAvailableMethods,
    "Devialet.AudioSource.CredentialsLoginRequest": TheSoundOfSilence.OnlineSource_pb2.CredentialsLoginRequest,
    "Devialet.AudioSource.OAuthLoginRequest": TheSoundOfSilence.OnlineSource_pb2.OAuthLoginRequest,
    "Devialet.AudioSource.AuthenticationMethods": TheSoundOfSilence.OnlineSource_pb2.AuthenticationMethods,
    "Devialet.AudioSource.RegistrationUrl": TheSoundOfSilence.OnlineSource_pb2.RegistrationUrl,
    "Devialet.AudioSource.AvailableReply": TheSoundOfSilence.OnlineSource_pb2.AvailableReply,
    "Devialet.AudioSource.LoginReply": TheSoundOfSilence.OnlineSource_pb2.LoginReply,
    "Devialet.AudioSource.LogoutRequest": TheSoundOfSilence.OnlineSource_pb2.LogoutRequest,
    "Devialet.AudioSource.SearchRequest": TheSoundOfSilence.OnlineSource_pb2.SearchRequest,
    "Devialet.AudioSource.AutocompleteRequest": TheSoundOfSilence.OnlineSource_pb2.AutocompleteRequest,
    "Devialet.AudioSource.PictureIdRequest": TheSoundOfSilence.OnlineSource_pb2.PictureIdRequest,
    "Devialet.AudioSource.CollectionRequest": TheSoundOfSilence.OnlineSource_pb2.CollectionRequest,
    "Devialet.AudioSource.SubcategoryRequest": TheSoundOfSilence.OnlineSource_pb2.SubcategoryRequest,
    "Devialet.AudioSource.TrackDetailsRequest": TheSoundOfSilence.OnlineSource_pb2.TrackDetailsRequest,
    "Devialet.AudioSource.TracksDetailsRequest": TheSoundOfSilence.OnlineSource_pb2.TracksDetailsRequest,
    "Devialet.AudioSource.UserAccountInfo": TheSoundOfSilence.OnlineSource_pb2.UserAccountInfo,
    "Devialet.AudioSource.GetSupportedFavoritesReply": TheSoundOfSilence.OnlineSource_pb2.GetSupportedFavoritesReply,
    "Devialet.AudioSource.UpdatePlaylistRequest": TheSoundOfSilence.OnlineSource_pb2.UpdatePlaylistRequest,
    "Devialet.AudioSource.CreatePlaylistRequest": TheSoundOfSilence.OnlineSource_pb2.CreatePlaylistRequest,
    "Devialet.AudioSource.IsTrackInPlaylistRequest": TheSoundOfSilence.OnlineSource_pb2.IsTrackInPlaylistRequest,
    "Devialet.AudioSource.Artist": TheSoundOfSilence.Artist_pb2.Artist,
    "Devialet.AudioSource.InputTypeMsg": TheSoundOfSilence.LiveSource_pb2.InputTypeMsg,
    "Devialet.AudioSource.LiveSourceStateMsg": TheSoundOfSilence.LiveSource_pb2.LiveSourceStateMsg,
    "Devialet.AudioSource.LiveSourceAvailableMethods": TheSoundOfSilence.LiveSource_pb2.LiveSourceAvailableMethods,
    "Devialet.AudioSource.LoadSessionQuery": TheSoundOfSilence.LiveSource_pb2.LoadSessionQuery,
    "Devialet.AudioSource.UnloadSessionQuery": TheSoundOfSilence.LiveSource_pb2.UnloadSessionQuery,
    "Devialet.AudioSource.SessionId": TheSoundOfSilence.Session_pb2.SessionId,
    "Devialet.AudioSource.Session": TheSoundOfSilence.Session_pb2.Session,
    "Devialet.AudioSource.Sessions": TheSoundOfSilence.Session_pb2.Sessions,
    "Devialet.AudioSource.Subcategory": TheSoundOfSilence.Subcategory_pb2.Subcategory,
    "Devialet.AudioSource.SourceError": TheSoundOfSilence.Source_pb2.SourceError,
    "Devialet.AudioSource.Enabled": TheSoundOfSilence.Source_pb2.Enabled,
    "Devialet.AudioSource.Id": TheSoundOfSilence.Source_pb2.Id,
    "Devialet.AudioSource.Uri": TheSoundOfSilence.Source_pb2.Uri,
    "Devialet.AudioSource.NodeId": TheSoundOfSilence.Node_pb2.NodeId,
    "Devialet.AudioSource.NodeIds": TheSoundOfSilence.Node_pb2.NodeIds,
    "Devialet.AudioSource.Node": TheSoundOfSilence.Node_pb2.Node,
    "Devialet.AudioSource.Nodes": TheSoundOfSilence.Node_pb2.Nodes,
    "Devialet.AudioSource.TrackDetails": TheSoundOfSilence.TrackDetails_pb2.TrackDetails,
    "Devialet.AudioSource.TracksDetails": TheSoundOfSilence.TrackDetails_pb2.TracksDetails,
    "Devialet.AudioSource.Collection": TheSoundOfSilence.Collection_pb2.Collection,
    "Devialet.AudioSource.Picture": TheSoundOfSilence.Picture_pb2.Picture,
    "Devialet.AudioSource.PictureId": TheSoundOfSilence.Picture_pb2.PictureId,
    "Devialet.AudioSource.Album": TheSoundOfSilence.Album_pb2.Album,
    "Devialet.AudioSource.Category": TheSoundOfSilence.Category_pb2.Category,
    "Devialet.AudioSource.Track": TheSoundOfSilence.Track_pb2.Track,
    "Devialet.TooManyFlows.IndexMsg": TooManyFlows.Playback_pb2.IndexMsg,
    "Devialet.TooManyFlows.ProgressionMsg": TooManyFlows.Playback_pb2.ProgressionMsg,
    "Devialet.TooManyFlows.StateMsg": TooManyFlows.Playback_pb2.StateMsg,
    "Devialet.TooManyFlows.SeekMsg": TooManyFlows.Playback_pb2.SeekMsg,
    "Devialet.TooManyFlows.PlaybackError": TooManyFlows.Playback_pb2.PlaybackError,
    "Devialet.TooManyFlows.TrackMsg": TooManyFlows.Playlist_pb2.TrackMsg,
    "Devialet.TooManyFlows.TracksMsg": TooManyFlows.Playlist_pb2.TracksMsg,
    "Devialet.TooManyFlows.MoveMsg": TooManyFlows.Playlist_pb2.MoveMsg,
    "Devialet.TooManyFlows.UrlMsg": TooManyFlows.History_pb2.UrlMsg,
    "Devialet.TooManyFlows.UrlsMsg": TooManyFlows.History_pb2.UrlsMsg,
    "Devialet.TooManyFlows.Mute": TooManyFlows.SoundControl_pb2.Mute,
    "Devialet.TooManyFlows.GroupMute": TooManyFlows.SoundControl_pb2.GroupMute,
    "Devialet.TooManyFlows.RendererMute": TooManyFlows.SoundControl_pb2.RendererMute,
    "Devialet.TooManyFlows.NightMode": TooManyFlows.SoundControl_pb2.NightMode,
    "Devialet.TooManyFlows.GroupNightMode": TooManyFlows.SoundControl_pb2.GroupNightMode,
    "Devialet.TooManyFlows.RendererNightMode": TooManyFlows.SoundControl_pb2.RendererNightMode,
    "Devialet.TooManyFlows.Volume": TooManyFlows.SoundControl_pb2.Volume,
    "Devialet.TooManyFlows.GroupVolume": TooManyFlows.SoundControl_pb2.GroupVolume,
    "Devialet.TooManyFlows.RendererVolume": TooManyFlows.SoundControl_pb2.RendererVolume,
    "Devialet.TooManyFlows.Properties": TooManyFlows.SoundControl_pb2.Properties,
    "Devialet.TooManyFlows.GroupProperties": TooManyFlows.SoundControl_pb2.GroupProperties,
    "Devialet.TooManyFlows.RendererProperties": TooManyFlows.SoundControl_pb2.RendererProperties,
    "Devialet.TooManyFlows.AllProperties": TooManyFlows.SoundControl_pb2.AllProperties,
    "Devialet.TooManyFlows.AddRendererQuery": TooManyFlows.Configuration_pb2.AddRendererQuery,
    "Devialet.TooManyFlows.ConfigurationError": TooManyFlows.Configuration_pb2.ConfigurationError,
    "Devialet.TooManyFlows.BouquetId": TooManyFlows.Identifier_pb2.BouquetId,
    "Devialet.TooManyFlows.GroupId": TooManyFlows.Identifier_pb2.GroupId,
    "Devialet.TooManyFlows.PlayerId": TooManyFlows.Identifier_pb2.PlayerId,
    "Devialet.TooManyFlows.RendererId": TooManyFlows.Identifier_pb2.RendererId,
    "Devialet.Fresh.UpdateInfo": Fresh.Fresh_pb2.UpdateInfo,
    "Devialet.Fresh.DeviceUpdateInfo": Fresh.Fresh_pb2.DeviceUpdateInfo,
    "Devialet.Fresh.DeviceUpdateInfoList": Fresh.Fresh_pb2.DeviceUpdateInfoList,
    "Devialet.Fresh.InstallUpdateRequest": Fresh.Fresh_pb2.InstallUpdateRequest,
    "Devialet.Fresh.UpdateDownloadProgress": Fresh.Fresh_pb2.UpdateDownloadProgress,
    "Devialet.Fresh.UpdateErrors": Fresh.Fresh_pb2.UpdateErrors,
    "Devialet.IMASlave4U.AudioMode": IMASlave4U.Configuration_pb2.AudioMode,
    "Devialet.IMASlave4U.Property": IMASlave4U.Configuration_pb2.Property,
    "Devialet.IMASlave4U.Input": IMASlave4U.Configuration_pb2.Input,
    "Devialet.CallMeMaybe.Request": RPCMessages_pb2.Request,
    "Devialet.CallMeMaybe.Reply": RPCMessages_pb2.Reply,
    "Devialet.CallMeMaybe.Event": RPCMessages_pb2.Event,
    "Devialet.CallMeMaybe.ConnectionRequest": RPCMessages_pb2.ConnectionRequest,
    "Devialet.CallMeMaybe.Service": RPCMessages_pb2.Service,
    "Devialet.CallMeMaybe.ServicesList": RPCMessages_pb2.ServicesList,
    "Devialet.CallMeMaybe.ConnectionReply": RPCMessages_pb2.ConnectionReply,
    "Devialet.CallMeMaybe.ConnectionErrors": RPCMessages_pb2.ConnectionErrors,
    "Devialet.SpotifyConnect.ZeroConfApiRequest": SpotifyConnect.SpotifyConnect_pb2.ZeroConfApiRequest,
    "Devialet.SpotifyConnect.ZeroConfApiReply": SpotifyConnect.SpotifyConnect_pb2.ZeroConfApiReply,
    "Devialet.CallMeMaybe.FieldOptions": CallMeMaybe.CallMeMaybe_pb2.FieldOptions,
    "Devialet.CallMeMaybe.ServiceProperty": CallMeMaybe.CallMeMaybe_pb2.ServiceProperty,
    "Devialet.CallMeMaybe.ServiceProperties": CallMeMaybe.CallMeMaybe_pb2.ServiceProperties,
    "Devialet.CallMeMaybe.ServiceOptions": CallMeMaybe.CallMeMaybe_pb2.ServiceOptions,
    "Devialet.CallMeMaybe.MethodOptions": CallMeMaybe.CallMeMaybe_pb2.MethodOptions,
    "Devialet.CallMeMaybe.EnumValueOptions": CallMeMaybe.CallMeMaybe_pb2.EnumValueOptions,
    "Devialet.CallMeMaybe.Empty": CallMeMaybe.CommonMessages_pb2.Empty,
    "Devialet.CallMeMaybe.BaseError": CallMeMaybe.CommonMessages_pb2.BaseError,
    "Devialet.CallMeMaybe.DoubleProperty": CallMeMaybe.CommonMessages_pb2.DoubleProperty,
    "Devialet.CallMeMaybe.FloatProperty": CallMeMaybe.CommonMessages_pb2.FloatProperty,
    "Devialet.CallMeMaybe.Int32Property": CallMeMaybe.CommonMessages_pb2.Int32Property,
    "Devialet.CallMeMaybe.Int64Property": CallMeMaybe.CommonMessages_pb2.Int64Property,
    "Devialet.CallMeMaybe.UInt32Property": CallMeMaybe.CommonMessages_pb2.UInt32Property,
    "Devialet.CallMeMaybe.UInt64Property": CallMeMaybe.CommonMessages_pb2.UInt64Property,
    "Devialet.CallMeMaybe.SInt32Property": CallMeMaybe.CommonMessages_pb2.SInt32Property,
    "Devialet.CallMeMaybe.SInt64Property": CallMeMaybe.CommonMessages_pb2.SInt64Property,
    "Devialet.CallMeMaybe.Fixed32Property": CallMeMaybe.CommonMessages_pb2.Fixed32Property,
    "Devialet.CallMeMaybe.Fixed64Property": CallMeMaybe.CommonMessages_pb2.Fixed64Property,
    "Devialet.CallMeMaybe.SFixed32Property": CallMeMaybe.CommonMessages_pb2.SFixed32Property,
    "Devialet.CallMeMaybe.SFixed64Property": CallMeMaybe.CommonMessages_pb2.SFixed64Property,
    "Devialet.CallMeMaybe.BoolProperty": CallMeMaybe.CommonMessages_pb2.BoolProperty,
    "Devialet.CallMeMaybe.StringProperty": CallMeMaybe.CommonMessages_pb2.StringProperty,
    "Devialet.CallMeMaybe.StringListProperty": CallMeMaybe.CommonMessages_pb2.StringListProperty,
    "Devialet.CallMeMaybe.BytesProperty": CallMeMaybe.CommonMessages_pb2.BytesProperty,
    "Devialet.GetThePartyStarted.Player.WiFiNetwork": GetThePartyStarted.Player_pb2.WiFiNetwork,
    "Devialet.GetThePartyStarted.Player.ListWiFiNetworksReply": GetThePartyStarted.Player_pb2.ListWiFiNetworksReply,
    "Devialet.GetThePartyStarted.Player.EnableStandaloneAccessPointRequest": GetThePartyStarted.Player_pb2.EnableStandaloneAccessPointRequest,
    "Devialet.GetThePartyStarted.Player.SetupStep": GetThePartyStarted.Player_pb2.SetupStep,
    "Devialet.GetThePartyStarted.Player.OpticalModeParameters": GetThePartyStarted.Player_pb2.OpticalModeParameters,
    "Devialet.GetThePartyStarted.Player.StandaloneConfiguration": GetThePartyStarted.Player_pb2.StandaloneConfiguration,
    "Devialet.GetThePartyStarted.Player.AppleWacAccessPointConfiguration": GetThePartyStarted.Player_pb2.AppleWacAccessPointConfiguration,
    "Devialet.GetThePartyStarted.Player.AppleWacWiFiNetworkConfiguration": GetThePartyStarted.Player_pb2.AppleWacWiFiNetworkConfiguration,
    "Devialet.GetThePartyStarted.ConfigurationErrors": GetThePartyStarted.GetThePartyStarted_pb2.ConfigurationErrors,
    "Devialet.GetThePartyStarted.DeviceInfo": GetThePartyStarted.GetThePartyStarted_pb2.DeviceInfo,
    "Devialet.GetThePartyStarted.SetupErrors": GetThePartyStarted.GetThePartyStarted_pb2.SetupErrors,
    "Devialet.GetThePartyStarted.SetupToken": GetThePartyStarted.GetThePartyStarted_pb2.SetupToken,
    "Devialet.GetThePartyStarted.SlaveInfo": GetThePartyStarted.GetThePartyStarted_pb2.SlaveInfo,
    "Devialet.GetThePartyStarted.SlaveInfoList": GetThePartyStarted.GetThePartyStarted_pb2.SlaveInfoList,
    "Devialet.GetThePartyStarted.StartSetupRequest": GetThePartyStarted.GetThePartyStarted_pb2.StartSetupRequest,
    "Devialet.GetThePartyStarted.WiFiNetwork": GetThePartyStarted.GetThePartyStarted_pb2.WiFiNetwork,
    "Devialet.GetThePartyStarted.WiFiConfigurationData": GetThePartyStarted.GetThePartyStarted_pb2.WiFiConfigurationData,
    "Devialet.GetThePartyStarted.PlcConfigurationData": GetThePartyStarted.GetThePartyStarted_pb2.PlcConfigurationData,
    "Devialet.GetThePartyStarted.ConfigurationData": GetThePartyStarted.GetThePartyStarted_pb2.ConfigurationData,
    "Devialet.GetThePartyStarted.SetConfigurationRequest": GetThePartyStarted.GetThePartyStarted_pb2.SetConfigurationRequest,
    "Devialet.GetThePartyStarted.UploadLogsRequest": GetThePartyStarted.Logging_pb2.UploadLogsRequest,
    "Devialet.GetThePartyStarted.Aerobase.SetupStep": GetThePartyStarted.Aerobase_pb2.SetupStep,
    "Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest": GetThePartyStarted.Aerobase_pb2.SetTopologyConfigurationRequest
}