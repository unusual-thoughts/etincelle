import time
import uuid
from dvlt_pool import Devialet, DevialetController
from dvlt_output import print_info, print_warning, print_data
from dvlt_client import WhatsUpClient
from dvlt_server import DevialetServer, WhatsUpServer
from dvlt_discovery import DevialetDiscovery
from queue import Queue

# Find a suitable Devialet device
hostUid = b'etincelle-' + bytes(uuid.uuid4().hex, 'ascii')
target_serial = b'J'

discovered = Queue()
dscvr = DevialetDiscovery(discovered, serial=hostUid)
dscvr.start()

serial, dvlt_addr = discovered.get(block=True)
while not serial.startswith(target_serial):
    print_warning('Not who we are looking for')
    serial, dvlt_addr = discovered.get(block=True)


# Open a WhatsUp connection
wu_client = WhatsUpClient(name="WhatsUp", addr=dvlt_addr, port=24242)
wu_client.go()


# Init WhatsUp server
wu_srv = WhatsUpServer(hostUid=hostUid)
wu_srv.open()

# Init AudioSource server
putp_server = DevialetServer(wu_srv, hostUid=hostUid)
putp_service = Devialet.AudioSource.OnlineSourceSession(putp_server)
putp_service.serviceName += '.pickupthepieces'
putp_service.properties = {
    'sourceId': Devialet.CallMeMaybe.StringProperty(value='putp'),
    'availableMethods': Devialet.AudioSource.OnlineSourceAvailableMethods(
        isSearchable=False,
        hasAutocomplete=False,
        hasBatchMode=False,
        supportPlaylistManagement=True)
}

putp_server.open()
putp_server.register_service(putp_service)

# Setup URI Callback
trackUID = uuid.uuid4().bytes + putp_service.uid  # uuid.uuid4().hex
trackURL = 'dvlt://{}@{}/{}'.format(putp_service.uid.hex(), putp_service.properties['sourceId'].value, trackUID.hex())
trackURI = "http://hcmaslov.d-real.sci-nnov.ru/public/mp3/Queen/Queen%20'Barcelona'.mp3"


def handle_uri(id_pb):
    uri = trackURI
    print_info('Got uri request for {}, replying with {}', id_pb.id.hex(), uri, color='magenta')
    return Devialet.AudioSource.Uri(uri=uri)

putp_service.uri(DevialetController(putp_service), None, handle_uri)

# Start the AudioSource server
putp_server.start()

# Start the entrypoint server
dscvr.start_advertising()
wu_srv.start()


def callback_test(arg):
    print_data("Callback with", arg)


# Clear Playlist then insert track, then start playback
tmf_client, tmf_playlist = wu_client.try_to_find_service('com.devialet.toomanyflows.playlist-0')
tmf_client.go()
tmf_playlist.watch_properties()

tmf_client2, tmf_playback = wu_client.try_to_find_service('com.devialet.toomanyflows.playback-0')
tmf_client2.go()
tmf_playback.watch_properties()

tmf_client3, tmf_meta = wu_client.try_to_find_service('com.devialet.toomanyflows.metadata-0')
tmf_client3.go()

tmf_playlist.cleared(DevialetController(tmf_playlist), None, lambda empty: tmf_playlist.insert(
    DevialetController(tmf_playlist), Devialet.TooManyFlows.TracksMsg(tracks=[Devialet.TooManyFlows.TrackMsg(index=0, url=trackURL)]), callback_test))

# tmf_playlist.tracksAdded(DevialetController(tmf_playlist), None, lambda empty: tmf_playback.play(
#     DevialetController(tmf_playback), Devialet.CallMeMaybe.Empty(), callback_test))

tmf_meta.propertyUpdate(DevialetController(tmf_meta), None, lambda empty: tmf_playback.play(
    DevialetController(tmf_playback), Devialet.CallMeMaybe.Empty(), callback_test))

# GO
tmf_playlist.clear(DevialetController(tmf_playlist), Devialet.CallMeMaybe.Empty(), callback_test)

print_info('Successfully cleared playlist', color='green')
# tmf_client.shutdown()


# time.sleep(3)

# time.sleep(10)
print_info('Successfully pressed play', color='green')


def pingback(arg):
    print_info("Pong <--")

try:
    while True:  # ~ 20 ms round-trip for pings
        time.sleep(1)
        print_info("Ping -->")
        wu_client.conn.ping(DevialetController(wu_client.conn), Devialet.CallMeMaybe.Empty(), pingback)
except KeyboardInterrupt:
    wu_client.shutdown()
    tmf_client.shutdown()
    tmf_client2.shutdown()
    tmf_client3.shutdown()
    putp_server.shutdown()
    wu_srv.shutdown()
    dscvr.shutdown()

    print_info('join()ing wu client...')
    wu_client.join()
    print_info('join()ing tmf client...')
    tmf_client.join()
    print_info('join()ing putp server...')
    putp_server.join()
    print_info('join()ing wu server...')
    wu_srv.join()
    print_info('join()ing discovery..')
    dscvr.join()
