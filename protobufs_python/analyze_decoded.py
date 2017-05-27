import pickle
from collections import Counter
from pprint import pprint
from protobuf_to_dict import protobuf_to_dict

# import RPCMessages_pb2
# import CallMeMaybe.CallMeMaybe_pb2

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



all_msgs = [
    {
        "msg": SaveMe.SaveMe_pb2.SavePlaylistError(),
        "name": "Devialet.SaveMe.SavePlaylistError",
    },
    {
        "msg": SaveMe.SaveMe_pb2.Track(),
        "name": "Devialet.SaveMe.Track",
    },
    {
        "msg": SaveMe.SaveMe_pb2.PlaylistMsg(),
        "name": "Devialet.SaveMe.PlaylistMsg",
    },
    {
        "msg": SaveMe.SaveMe_pb2.TrackInPlaylist(),
        "name": "Devialet.SaveMe.TrackInPlaylist",
    },
    {
        "msg": SaveMe.SaveMe_pb2.CreatePlaylist(),
        "name": "Devialet.SaveMe.CreatePlaylist",
    },
    {
        "msg": SaveMe.SaveMe_pb2.PlaylistSaved(),
        "name": "Devialet.SaveMe.PlaylistSaved",
    },
    {
        "msg": SaveMe.SaveMe_pb2.PlaylistContent(),
        "name": "Devialet.SaveMe.PlaylistContent",
    },
    {
        "msg": SaveMe.SaveMe_pb2.ModifyTracks(),
        "name": "Devialet.SaveMe.ModifyTracks",
    },
    {
        "msg": SaveMe.SaveMe_pb2.ModifyOneTrack(),
        "name": "Devialet.SaveMe.ModifyOneTrack",
    },
    {
        "msg": SaveMe.SaveMe_pb2.ModifyPlaylistName(),
        "name": "Devialet.SaveMe.ModifyPlaylistName",
    },
    {
        "msg": WhatsUp_pb2.RegistrarRegisterQuery(),
        "name": "Devialet.WhatsUp.RegistrarRegisterQuery",
    },
    {
        "msg": WhatsUp_pb2.RegistrarUnregisterQuery(),
        "name": "Devialet.WhatsUp.RegistrarUnregisterQuery",
    },
    {
        "msg": WhatsUp_pb2.RegistrarServicesQuery(),
        "name": "Devialet.WhatsUp.RegistrarServicesQuery",
    },
    {
        "msg": WhatsUp_pb2.RegistrarPingQuery(),
        "name": "Devialet.WhatsUp.RegistrarPingQuery",
    },
    {
        "msg": WhatsUp_pb2.RegistrarErrors(),
        "name": "Devialet.WhatsUp.RegistrarErrors",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpNetwork(),
        "name": "Devialet.WhatsUp.WhatsUpNetwork",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpNetworkInterface(),
        "name": "Devialet.WhatsUp.WhatsUpNetworkInterface",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpHost(),
        "name": "Devialet.WhatsUp.WhatsUpHost",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpHostsList(),
        "name": "Devialet.WhatsUp.WhatsUpHostsList",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpService(),
        "name": "Devialet.WhatsUp.WhatsUpService",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpServicesList(),
        "name": "Devialet.WhatsUp.WhatsUpServicesList",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpServicesUpdate(),
        "name": "Devialet.WhatsUp.WhatsUpServicesUpdate",
    },
    {
        "msg": WhatsUp_pb2.WhatsUpServicesRemoval(),
        "name": "Devialet.WhatsUp.WhatsUpServicesRemoval",
    },
    {
        "msg": WhatsUp_pb2.RegistryLookupHostQuery(),
        "name": "Devialet.WhatsUp.RegistryLookupHostQuery",
    },
    {
        "msg": WhatsUp_pb2.RegistryLookupHostReply(),
        "name": "Devialet.WhatsUp.RegistryLookupHostReply",
    },
    {
        "msg": WhatsUp_pb2.RegistryFindServicesQuery(),
        "name": "Devialet.WhatsUp.RegistryFindServicesQuery",
    },
    {
        "msg": WhatsUp_pb2.RegistryNetworkConfigurationChangedNotification(),
        "name": "Devialet.WhatsUp.RegistryNetworkConfigurationChangedNotification",
    },
    {
        "msg": WhatsUp_pb2.RegistryHostUpdatedNotification(),
        "name": "Devialet.WhatsUp.RegistryHostUpdatedNotification",
    },
    {
        "msg": google.protobuf.descriptor_pb2.FileDescriptorSet(),
        "name": "google.protobuf.FileDescriptorSet",
    },
    {
        "msg": google.protobuf.descriptor_pb2.FileDescriptorProto(),
        "name": "google.protobuf.FileDescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.DescriptorProto(),
        "name": "google.protobuf.DescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.FieldDescriptorProto(),
        "name": "google.protobuf.FieldDescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.OneofDescriptorProto(),
        "name": "google.protobuf.OneofDescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.EnumDescriptorProto(),
        "name": "google.protobuf.EnumDescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.EnumValueDescriptorProto(),
        "name": "google.protobuf.EnumValueDescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.ServiceDescriptorProto(),
        "name": "google.protobuf.ServiceDescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.MethodDescriptorProto(),
        "name": "google.protobuf.MethodDescriptorProto",
    },
    {
        "msg": google.protobuf.descriptor_pb2.FileOptions(),
        "name": "google.protobuf.FileOptions",
    },
    {
        "msg": google.protobuf.descriptor_pb2.MessageOptions(),
        "name": "google.protobuf.MessageOptions",
    },
    {
        "msg": google.protobuf.descriptor_pb2.FieldOptions(),
        "name": "google.protobuf.FieldOptions",
    },
    {
        "msg": google.protobuf.descriptor_pb2.EnumOptions(),
        "name": "google.protobuf.EnumOptions",
    },
    {
        "msg": google.protobuf.descriptor_pb2.EnumValueOptions(),
        "name": "google.protobuf.EnumValueOptions",
    },
    {
        "msg": google.protobuf.descriptor_pb2.ServiceOptions(),
        "name": "google.protobuf.ServiceOptions",
    },
    {
        "msg": google.protobuf.descriptor_pb2.MethodOptions(),
        "name": "google.protobuf.MethodOptions",
    },
    {
        "msg": google.protobuf.descriptor_pb2.UninterpretedOption(),
        "name": "google.protobuf.UninterpretedOption",
    },
    {
        "msg": google.protobuf.descriptor_pb2.SourceCodeInfo(),
        "name": "google.protobuf.SourceCodeInfo",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.GroupId(),
        "name": "Devialet.MasterOfPuppets.GroupId",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.BouquetId(),
        "name": "Devialet.MasterOfPuppets.BouquetId",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.RendererId(),
        "name": "Devialet.MasterOfPuppets.RendererId",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.NodeRenderer(),
        "name": "Devialet.MasterOfPuppets.NodeRenderer",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.NodeGroup(),
        "name": "Devialet.MasterOfPuppets.NodeGroup",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.NodeBouquet(),
        "name": "Devialet.MasterOfPuppets.NodeBouquet",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.NodeRoot(),
        "name": "Devialet.MasterOfPuppets.NodeRoot",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.AddGroupQuery(),
        "name": "Devialet.MasterOfPuppets.AddGroupQuery",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.AddRendererQuery(),
        "name": "Devialet.MasterOfPuppets.AddRendererQuery",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.MoveGroupQuery(),
        "name": "Devialet.MasterOfPuppets.MoveGroupQuery",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.MoveRendererQuery(),
        "name": "Devialet.MasterOfPuppets.MoveRendererQuery",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.RenameQuery(),
        "name": "Devialet.MasterOfPuppets.RenameQuery",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.BouquetAddedNotification(),
        "name": "Devialet.MasterOfPuppets.BouquetAddedNotification",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.GroupAddedNotification(),
        "name": "Devialet.MasterOfPuppets.GroupAddedNotification",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.RendererAddedNotification(),
        "name": "Devialet.MasterOfPuppets.RendererAddedNotification",
    },
    {
        "msg": MasterOfPuppets.Configuration_pb2.StateNotification(),
        "name": "Devialet.MasterOfPuppets.StateNotification",
    },
    {
        "msg": AppleAirPlay.Playback_pb2.Dummy(),
        "name": "Devialet.AppleAirPlay.Dummy",
    },
    {
        "msg": LeftAlone.Configuration_pb2.FakeMsg(),
        "name": "Devialet.LeftAlone.FakeMsg",
    },
    {
        "msg": TheSoundOfSilence.Playlist_pb2.Playlist(),
        "name": "Devialet.AudioSource.Playlist",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.OnlineSourceError(),
        "name": "Devialet.AudioSource.OnlineSourceError",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.OnlineSourceAvailableMethods(),
        "name": "Devialet.AudioSource.OnlineSourceAvailableMethods",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.CredentialsLoginRequest(),
        "name": "Devialet.AudioSource.CredentialsLoginRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.OAuthLoginRequest(),
        "name": "Devialet.AudioSource.OAuthLoginRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.AuthenticationMethods(),
        "name": "Devialet.AudioSource.AuthenticationMethods",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.RegistrationUrl(),
        "name": "Devialet.AudioSource.RegistrationUrl",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.AvailableReply(),
        "name": "Devialet.AudioSource.AvailableReply",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.LoginReply(),
        "name": "Devialet.AudioSource.LoginReply",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.LogoutRequest(),
        "name": "Devialet.AudioSource.LogoutRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.SearchRequest(),
        "name": "Devialet.AudioSource.SearchRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.AutocompleteRequest(),
        "name": "Devialet.AudioSource.AutocompleteRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.PictureIdRequest(),
        "name": "Devialet.AudioSource.PictureIdRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.CollectionRequest(),
        "name": "Devialet.AudioSource.CollectionRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.SubcategoryRequest(),
        "name": "Devialet.AudioSource.SubcategoryRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.TrackDetailsRequest(),
        "name": "Devialet.AudioSource.TrackDetailsRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.TracksDetailsRequest(),
        "name": "Devialet.AudioSource.TracksDetailsRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.UserAccountInfo(),
        "name": "Devialet.AudioSource.UserAccountInfo",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.GetSupportedFavoritesReply(),
        "name": "Devialet.AudioSource.GetSupportedFavoritesReply",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.UpdatePlaylistRequest(),
        "name": "Devialet.AudioSource.UpdatePlaylistRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.CreatePlaylistRequest(),
        "name": "Devialet.AudioSource.CreatePlaylistRequest",
    },
    {
        "msg": TheSoundOfSilence.OnlineSource_pb2.IsTrackInPlaylistRequest(),
        "name": "Devialet.AudioSource.IsTrackInPlaylistRequest",
    },
    {
        "msg": TheSoundOfSilence.Artist_pb2.Artist(),
        "name": "Devialet.AudioSource.Artist",
    },
    {
        "msg": TheSoundOfSilence.LiveSource_pb2.InputTypeMsg(),
        "name": "Devialet.AudioSource.InputTypeMsg",
    },
    {
        "msg": TheSoundOfSilence.LiveSource_pb2.LiveSourceStateMsg(),
        "name": "Devialet.AudioSource.LiveSourceStateMsg",
    },
    {
        "msg": TheSoundOfSilence.LiveSource_pb2.LiveSourceAvailableMethods(),
        "name": "Devialet.AudioSource.LiveSourceAvailableMethods",
    },
    {
        "msg": TheSoundOfSilence.LiveSource_pb2.LoadSessionQuery(),
        "name": "Devialet.AudioSource.LoadSessionQuery",
    },
    {
        "msg": TheSoundOfSilence.LiveSource_pb2.UnloadSessionQuery(),
        "name": "Devialet.AudioSource.UnloadSessionQuery",
    },
    {
        "msg": TheSoundOfSilence.Session_pb2.SessionId(),
        "name": "Devialet.AudioSource.SessionId",
    },
    {
        "msg": TheSoundOfSilence.Session_pb2.Session(),
        "name": "Devialet.AudioSource.Session",
    },
    {
        "msg": TheSoundOfSilence.Session_pb2.Sessions(),
        "name": "Devialet.AudioSource.Sessions",
    },
    {
        "msg": TheSoundOfSilence.Subcategory_pb2.Subcategory(),
        "name": "Devialet.AudioSource.Subcategory",
    },
    {
        "msg": TheSoundOfSilence.Source_pb2.SourceError(),
        "name": "Devialet.AudioSource.SourceError",
    },
    {
        "msg": TheSoundOfSilence.Source_pb2.Enabled(),
        "name": "Devialet.AudioSource.Enabled",
    },
    {
        "msg": TheSoundOfSilence.Source_pb2.Id(),
        "name": "Devialet.AudioSource.Id",
    },
    {
        "msg": TheSoundOfSilence.Source_pb2.Uri(),
        "name": "Devialet.AudioSource.Uri",
    },
    {
        "msg": TheSoundOfSilence.Node_pb2.NodeId(),
        "name": "Devialet.AudioSource.NodeId",
    },
    {
        "msg": TheSoundOfSilence.Node_pb2.NodeIds(),
        "name": "Devialet.AudioSource.NodeIds",
    },
    {
        "msg": TheSoundOfSilence.Node_pb2.Node(),
        "name": "Devialet.AudioSource.Node",
    },
    {
        "msg": TheSoundOfSilence.Node_pb2.Nodes(),
        "name": "Devialet.AudioSource.Nodes",
    },
    {
        "msg": TheSoundOfSilence.TrackDetails_pb2.TrackDetails(),
        "name": "Devialet.AudioSource.TrackDetails",
    },
    {
        "msg": TheSoundOfSilence.TrackDetails_pb2.TracksDetails(),
        "name": "Devialet.AudioSource.TracksDetails",
    },
    {
        "msg": TheSoundOfSilence.Collection_pb2.Collection(),
        "name": "Devialet.AudioSource.Collection",
    },
    {
        "msg": TheSoundOfSilence.Picture_pb2.Picture(),
        "name": "Devialet.AudioSource.Picture",
    },
    {
        "msg": TheSoundOfSilence.Picture_pb2.PictureId(),
        "name": "Devialet.AudioSource.PictureId",
    },
    {
        "msg": TheSoundOfSilence.Album_pb2.Album(),
        "name": "Devialet.AudioSource.Album",
    },
    {
        "msg": TheSoundOfSilence.Category_pb2.Category(),
        "name": "Devialet.AudioSource.Category",
    },
    {
        "msg": TheSoundOfSilence.Track_pb2.Track(),
        "name": "Devialet.AudioSource.Track",
    },
    {
        "msg": TooManyFlows.Playback_pb2.IndexMsg(),
        "name": "Devialet.TooManyFlows.IndexMsg",
    },
    {
        "msg": TooManyFlows.Playback_pb2.ProgressionMsg(),
        "name": "Devialet.TooManyFlows.ProgressionMsg",
    },
    {
        "msg": TooManyFlows.Playback_pb2.StateMsg(),
        "name": "Devialet.TooManyFlows.StateMsg",
    },
    {
        "msg": TooManyFlows.Playback_pb2.SeekMsg(),
        "name": "Devialet.TooManyFlows.SeekMsg",
    },
    {
        "msg": TooManyFlows.Playback_pb2.PlaybackError(),
        "name": "Devialet.TooManyFlows.PlaybackError",
    },
    {
        "msg": TooManyFlows.Playlist_pb2.TrackMsg(),
        "name": "Devialet.TooManyFlows.TrackMsg",
    },
    {
        "msg": TooManyFlows.Playlist_pb2.TracksMsg(),
        "name": "Devialet.TooManyFlows.TracksMsg",
    },
    {
        "msg": TooManyFlows.Playlist_pb2.MoveMsg(),
        "name": "Devialet.TooManyFlows.MoveMsg",
    },
    {
        "msg": TooManyFlows.History_pb2.UrlMsg(),
        "name": "Devialet.TooManyFlows.UrlMsg",
    },
    {
        "msg": TooManyFlows.History_pb2.UrlsMsg(),
        "name": "Devialet.TooManyFlows.UrlsMsg",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.Mute(),
        "name": "Devialet.TooManyFlows.Mute",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.GroupMute(),
        "name": "Devialet.TooManyFlows.GroupMute",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.RendererMute(),
        "name": "Devialet.TooManyFlows.RendererMute",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.NightMode(),
        "name": "Devialet.TooManyFlows.NightMode",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.GroupNightMode(),
        "name": "Devialet.TooManyFlows.GroupNightMode",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.RendererNightMode(),
        "name": "Devialet.TooManyFlows.RendererNightMode",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.Volume(),
        "name": "Devialet.TooManyFlows.Volume",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.GroupVolume(),
        "name": "Devialet.TooManyFlows.GroupVolume",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.RendererVolume(),
        "name": "Devialet.TooManyFlows.RendererVolume",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.Properties(),
        "name": "Devialet.TooManyFlows.Properties",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.GroupProperties(),
        "name": "Devialet.TooManyFlows.GroupProperties",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.RendererProperties(),
        "name": "Devialet.TooManyFlows.RendererProperties",
    },
    {
        "msg": TooManyFlows.SoundControl_pb2.AllProperties(),
        "name": "Devialet.TooManyFlows.AllProperties",
    },
    {
        "msg": TooManyFlows.Configuration_pb2.AddRendererQuery(),
        "name": "Devialet.TooManyFlows.AddRendererQuery",
    },
    {
        "msg": TooManyFlows.Configuration_pb2.ConfigurationError(),
        "name": "Devialet.TooManyFlows.ConfigurationError",
    },
    {
        "msg": TooManyFlows.Identifier_pb2.BouquetId(),
        "name": "Devialet.TooManyFlows.BouquetId",
    },
    {
        "msg": TooManyFlows.Identifier_pb2.GroupId(),
        "name": "Devialet.TooManyFlows.GroupId",
    },
    {
        "msg": TooManyFlows.Identifier_pb2.PlayerId(),
        "name": "Devialet.TooManyFlows.PlayerId",
    },
    {
        "msg": TooManyFlows.Identifier_pb2.RendererId(),
        "name": "Devialet.TooManyFlows.RendererId",
    },
    {
        "msg": Fresh.Fresh_pb2.UpdateInfo(),
        "name": "Devialet.Fresh.UpdateInfo",
    },
    {
        "msg": Fresh.Fresh_pb2.DeviceUpdateInfo(),
        "name": "Devialet.Fresh.DeviceUpdateInfo",
    },
    {
        "msg": Fresh.Fresh_pb2.DeviceUpdateInfoList(),
        "name": "Devialet.Fresh.DeviceUpdateInfoList",
    },
    {
        "msg": Fresh.Fresh_pb2.InstallUpdateRequest(),
        "name": "Devialet.Fresh.InstallUpdateRequest",
    },
    {
        "msg": Fresh.Fresh_pb2.UpdateDownloadProgress(),
        "name": "Devialet.Fresh.UpdateDownloadProgress",
    },
    {
        "msg": Fresh.Fresh_pb2.UpdateErrors(),
        "name": "Devialet.Fresh.UpdateErrors",
    },
    {
        "msg": IMASlave4U.Configuration_pb2.AudioMode(),
        "name": "Devialet.IMASlave4U.AudioMode",
    },
    {
        "msg": IMASlave4U.Configuration_pb2.Property(),
        "name": "Devialet.IMASlave4U.Property",
    },
    {
        "msg": IMASlave4U.Configuration_pb2.Input(),
        "name": "Devialet.IMASlave4U.Input",
    },
    {
        "msg": RPCMessages_pb2.Request(),
        "name": "Devialet.CallMeMaybe.Request",
    },
    {
        "msg": RPCMessages_pb2.Reply(),
        "name": "Devialet.CallMeMaybe.Reply",
    },
    {
        "msg": RPCMessages_pb2.Event(),
        "name": "Devialet.CallMeMaybe.Event",
    },
    {
        "msg": RPCMessages_pb2.ConnectionRequest(),
        "name": "Devialet.CallMeMaybe.ConnectionRequest",
    },
    {
        "msg": RPCMessages_pb2.Service(),
        "name": "Devialet.CallMeMaybe.Service",
    },
    {
        "msg": RPCMessages_pb2.ServicesList(),
        "name": "Devialet.CallMeMaybe.ServicesList",
    },
    {
        "msg": RPCMessages_pb2.ConnectionReply(),
        "name": "Devialet.CallMeMaybe.ConnectionReply",
    },
    {
        "msg": RPCMessages_pb2.ConnectionErrors(),
        "name": "Devialet.CallMeMaybe.ConnectionErrors",
    },
    {
        "msg": SpotifyConnect.SpotifyConnect_pb2.ZeroConfApiRequest(),
        "name": "Devialet.SpotifyConnect.ZeroConfApiRequest",
    },
    {
        "msg": SpotifyConnect.SpotifyConnect_pb2.ZeroConfApiReply(),
        "name": "Devialet.SpotifyConnect.ZeroConfApiReply",
    },
    {
        "msg": CallMeMaybe.CallMeMaybe_pb2.FieldOptions(),
        "name": "Devialet.CallMeMaybe.FieldOptions",
    },
    {
        "msg": CallMeMaybe.CallMeMaybe_pb2.ServiceProperty(),
        "name": "Devialet.CallMeMaybe.ServiceProperty",
    },
    {
        "msg": CallMeMaybe.CallMeMaybe_pb2.ServiceProperties(),
        "name": "Devialet.CallMeMaybe.ServiceProperties",
    },
    {
        "msg": CallMeMaybe.CallMeMaybe_pb2.ServiceOptions(),
        "name": "Devialet.CallMeMaybe.ServiceOptions",
    },
    {
        "msg": CallMeMaybe.CallMeMaybe_pb2.MethodOptions(),
        "name": "Devialet.CallMeMaybe.MethodOptions",
    },
    {
        "msg": CallMeMaybe.CallMeMaybe_pb2.EnumValueOptions(),
        "name": "Devialet.CallMeMaybe.EnumValueOptions",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.Empty(),
        "name": "Devialet.CallMeMaybe.Empty",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.BaseError(),
        "name": "Devialet.CallMeMaybe.BaseError",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.DoubleProperty(),
        "name": "Devialet.CallMeMaybe.DoubleProperty",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.FloatProperty(),
        "name": "Devialet.CallMeMaybe.FloatProperty",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.Int32Property(),
        "name": "Devialet.CallMeMaybe.Int32Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.Int64Property(),
        "name": "Devialet.CallMeMaybe.Int64Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.UInt32Property(),
        "name": "Devialet.CallMeMaybe.UInt32Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.UInt64Property(),
        "name": "Devialet.CallMeMaybe.UInt64Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.SInt32Property(),
        "name": "Devialet.CallMeMaybe.SInt32Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.SInt64Property(),
        "name": "Devialet.CallMeMaybe.SInt64Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.Fixed32Property(),
        "name": "Devialet.CallMeMaybe.Fixed32Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.Fixed64Property(),
        "name": "Devialet.CallMeMaybe.Fixed64Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.SFixed32Property(),
        "name": "Devialet.CallMeMaybe.SFixed32Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.SFixed64Property(),
        "name": "Devialet.CallMeMaybe.SFixed64Property",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.BoolProperty(),
        "name": "Devialet.CallMeMaybe.BoolProperty",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.StringProperty(),
        "name": "Devialet.CallMeMaybe.StringProperty",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.StringListProperty(),
        "name": "Devialet.CallMeMaybe.StringListProperty",
    },
    {
        "msg": CallMeMaybe.CommonMessages_pb2.BytesProperty(),
        "name": "Devialet.CallMeMaybe.BytesProperty",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.WiFiNetwork(),
        "name": "Devialet.GetThePartyStarted.Player.WiFiNetwork",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.ListWiFiNetworksReply(),
        "name": "Devialet.GetThePartyStarted.Player.ListWiFiNetworksReply",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.EnableStandaloneAccessPointRequest(),
        "name": "Devialet.GetThePartyStarted.Player.EnableStandaloneAccessPointRequest",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.SetupStep(),
        "name": "Devialet.GetThePartyStarted.Player.SetupStep",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.OpticalModeParameters(),
        "name": "Devialet.GetThePartyStarted.Player.OpticalModeParameters",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.StandaloneConfiguration(),
        "name": "Devialet.GetThePartyStarted.Player.StandaloneConfiguration",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.AppleWacAccessPointConfiguration(),
        "name": "Devialet.GetThePartyStarted.Player.AppleWacAccessPointConfiguration",
    },
    {
        "msg": GetThePartyStarted.Player_pb2.AppleWacWiFiNetworkConfiguration(),
        "name": "Devialet.GetThePartyStarted.Player.AppleWacWiFiNetworkConfiguration",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.ConfigurationErrors(),
        "name": "Devialet.GetThePartyStarted.ConfigurationErrors",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.DeviceInfo(),
        "name": "Devialet.GetThePartyStarted.DeviceInfo",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.SetupErrors(),
        "name": "Devialet.GetThePartyStarted.SetupErrors",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.SetupToken(),
        "name": "Devialet.GetThePartyStarted.SetupToken",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.SlaveInfo(),
        "name": "Devialet.GetThePartyStarted.SlaveInfo",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.SlaveInfoList(),
        "name": "Devialet.GetThePartyStarted.SlaveInfoList",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.StartSetupRequest(),
        "name": "Devialet.GetThePartyStarted.StartSetupRequest",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.WiFiNetwork(),
        "name": "Devialet.GetThePartyStarted.WiFiNetwork",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.WiFiConfigurationData(),
        "name": "Devialet.GetThePartyStarted.WiFiConfigurationData",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.PlcConfigurationData(),
        "name": "Devialet.GetThePartyStarted.PlcConfigurationData",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.ConfigurationData(),
        "name": "Devialet.GetThePartyStarted.ConfigurationData",
    },
    {
        "msg": GetThePartyStarted.GetThePartyStarted_pb2.SetConfigurationRequest(),
        "name": "Devialet.GetThePartyStarted.SetConfigurationRequest",
    },
    {
        "msg": GetThePartyStarted.Logging_pb2.UploadLogsRequest(),
        "name": "Devialet.GetThePartyStarted.UploadLogsRequest",
    },
    {
        "msg": GetThePartyStarted.Aerobase_pb2.SetupStep(),
        "name": "Devialet.GetThePartyStarted.Aerobase.SetupStep",
    },
    {
        "msg": GetThePartyStarted.Aerobase_pb2.SetTopologyConfigurationRequest(),
        "name": "Devialet.GetThePartyStarted.Aerobase.SetTopologyConfigurationRequest",
    }
]




dump_file = open('../all_decoded.pickle', 'rb')
sessions = pickle.load(dump_file)

# pprint([{
#           "session": session['name'],
#           "port_stats": sorted(Counter([
#               capture['port'] for capture in session['captures']
#           ]).items())
#       } for session in sessions])

# pprint([session['captures'][0]['packets'][:3] for session in sessions])

req = RPCMessages_pb2.Request()
reply = RPCMessages_pb2.Reply()

conn_req = RPCMessages_pb2.ConnectionRequest()
conn_reply = RPCMessages_pb2.ConnectionReply()

# Direction == 0 is from Spark to Phantom
# for packet in [
#         packet for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 0 
#     ][:10]:
#     for dec in packet['decoded']:
#         # pprint(dec)
#         for proto in dec['protobufs']:
#             # pprint(proto)
#             if proto['raw']:
#                 req.ParseFromString(proto['raw'])
#                 pprint(protobuf_to_dict(req))

        # pprint( [ [ [
        #           proto['protoc'] for proto in dec['protobufs']
        #       ] for dec in packet['decoded']
        #   ] for packet in [
        #       packet for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 1 
        #   ][:3]
        # ])

outgoing_packets = [packet['decoded'] for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 0]
incoming_packets = [packet['decoded'] for packet in sessions[0]['captures'][0]['packets'] if packet['direction'] == 1]

# pprint(outgoing_packets)

# First packet(s), first and only section, two protobufs each
        # req.ParseFromString(outgoing_packets[0][0]['protobufs'][0]['raw'])
        # pprint(protobuf_to_dict(req))

        # reply.ParseFromString(incoming_packets[0][0]['protobufs'][0]['raw'])
        # pprint(protobuf_to_dict(reply))


        # conn_req.ParseFromString(outgoing_packets[0][0]['protobufs'][1]['raw'])
        # pprint(protobuf_to_dict(conn_req))

        # conn_reply.ParseFromString(incoming_packets[0][0]['protobufs'][1]['raw'])
        # pprint(protobuf_to_dict(conn_reply))

# Second packet(s), first and only section, 


def full_len(d):
    if type(d) == dict:
        # print("yay", len(d))
        return sum(full_len(v) for v in d.values())
    elif type(d) == list:
        return sum(full_len(v) for v in d)
    else:
        return 1
    

# i=0
# lengths = [0] * len(all_msgs)
    # for i in range(len(all_msgs)):
    #     try:
    #         all_msgs[i]['msg'].ParseFromString(incoming_packets[0][0]['protobufs'][1]['raw'])
    #         # print(test['name'])
    #         # pprint(protobuf_to_dict(test['msg']))
    #         # lengths[i] = len(protobuf_to_dict(test['msg']))
    #         all_msgs[i]['length'] = full_len(protobuf_to_dict(all_msgs[i]['msg']))
    #         # i+=1
    #     except:
    #         all_msgs[i]['length'] = -1
    #         pass

# print(i, len(all_msgs))
# pprint(all_msgs)
# pprint([protobuf_to_dict(test['msg']) for test in all_msgs if test['length'] > 2])

# pprint([{'name': test['name'], 'length': test['length']} for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 1])

# pprint([{'name': test['name'], 'length': test['length'], 'msg': protobuf_to_dict(test['msg'])} for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 1])
# pprint([{test['name'], test['length']} for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 2])


# pprint([{
#     'name': test['name'],
#     'length': test['length'],
#     'msg': protobuf_to_dict(test['msg'])
#     } for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 2 or test['length'] == max(result['length'] for result in all_msgs)])


def heuristic_search(raw_protobuf, filter=""):
    for i in range(len(all_msgs)):
        if all_msgs[i]['name'].startswith(filter):
            try:
                all_msgs[i]['msg'].ParseFromString(raw_protobuf)
                all_msgs[i]['length'] = full_len(protobuf_to_dict(all_msgs[i]['msg']))
            except:
                all_msgs[i]['length'] = -1
                pass
        else:
            all_msgs[i]['length'] = -1
    return [{
            'name': test['name'],
            'length': test['length'],
            # 'msg': protobuf_to_dict(test['msg'])
        } for test in sorted(all_msgs, key=lambda x:x['length']) if test['length'] > 2 or test['length'] == max(
        result['length'] for result in all_msgs
    )]


# pprint(heuristic_search(incoming_packets[0][0]['protobufs'][1]['raw']))

def read_protobuf_raw_in_order(packets):
    for packet in packets:
        for section in packet:
            for protobuf in section['protobufs']:
                yield protobuf['raw']

# for packet_num in range(5):
#     for section in incoming_packets[packet_num]:
#         for protobuf in section['protobufs']:
#             if protobuf['raw']:
#                 pprint(heuristic_search(protobuf['raw'], filter="Devialet.CallMeMaybe"))
#             else:
#                 print("empty protobuf")

for (incoming, outgoing) in zip(read_protobuf_raw_in_order(incoming_packets), read_protobuf_raw_in_order(outgoing_packets)):
    pprint({
        "0outgoing": heuristic_search(outgoing, filter="Devialet.CallMeMaybe") if outgoing else "empty protobuf",
        "1incoming": heuristic_search(incoming, filter="Devialet.CallMeMaybe") if incoming else "empty protobuf" 
    })