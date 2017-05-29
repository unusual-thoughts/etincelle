import re

def find_method(rep, service_list):
    method = {}
    service = {}
    package = {}
    service_name = ""

    # if not(service_list):
    if rep.serviceId == 0 and not service_list:
        # Assume initial service is CallmeMaybe.Connection, which is placed first
        package = all_services[0]
        service = package['services'][rep.type]
        method = service['methods'][rep.subTypeId]

    elif rep.serviceId in [service.id for service in service_list]:
        service_name = [service.name for service in service_list if service.id == rep.serviceId][0]
        # package_name = '.'.join(service_name.split('.')[1:-2])
        # service_name = '.'.join(service_name.split('.')[-2:-1])
        package_name, service_name = re.match(
            '^[^\.]+\.(.*?)(?:-0)?\.([^\.]+?)(?:-0)?\.[^\.]+$', service_name).groups()
        # this isnt perfect, apparently sometimes more than one service: com.devialet.getthepartystarted.configuration-0.player-0.ece3ce2e

        # print(package_name, service_name)
        
        for p in all_services:
            if p['package_name'].lower() == package_name:
                for s in p['services']:
                    if s['name'].lower() == service_name:
                        # for m in s['methods']:
                        #     if m['name'] == 
                        service = s
                        package = p
                        print('service {} from {} appears to correspond to type {}'.format(
                            service_name, package_name, rep.type
                        ))
                        try:
                            method = service['methods'][rep.subTypeId]
                        except IndexError:
                            print("Error: subTypeId {} too big for package {}, service {}".format(
                                rep.subTypeId, package_name, service_name
                            ))
        if package == {} or service == {}:
            print('Error: service "{}" or package "{}" not found in database'.format(service_name, package_name))
    else:
        print("Error: Unknown service ID {}".format(rep.serviceId))

    return (service_name, package, service, method)

all_services = [
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
