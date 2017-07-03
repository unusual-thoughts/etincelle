import socket
from datetime import datetime
from select import select
from dvlt_pool import dvlt_pool, Devialet, DevialetController
from dvlt_output import print_info, print_data, print_warning
from dvlt_client import DevialetClient, WhatsUpClient
from dvlt_discovery import DevialetDiscovery
from queue import Queue
# from threading import Thread


discovered = Queue()
dscvr = DevialetDiscovery(discovered)
dscvr.start()

serial, dvlt_addr = discovered.get(block=True)


def callback_test(arg):
    print_data("Callback with", arg)

# Open a WhatsUp connection
wu_client = WhatsUpClient(name="WhatsUp", addr=dvlt_addr, port=24242, start_time=datetime.now())
wu_client.open()
wu_client.run()
wu_client.keep_receiving(timeout=2)
# reg.propertyGet(cmm_ctrl, Devialet.CallMeMaybe.Empty(), callback_test)

# tmf_client = DevialetClient(name='TooManyFlows Configuration', addr=dvlt_addr, port=37610, start_time=datetime.now())
# tmf_client.open()
# tmf_conf = Devialet.TooManyFlows.Configuration(tmf_client)
# tmf_ctrl = DevialetController(tmf_conf)
# tmf_conf.propertyGet(tmf_ctrl, Devialet.CallMeMaybe.Empty(), callback_test)
# tmf_client.keep_receiving()


# Whatsup Listening socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 24242))
serversocket.listen(5)

dscvr.start_advertising()


def pingback(arg):
    print_info("Pong <--")

while True:  # ~ 20 ms round-trip for pings
    # time.sleep(1)
    ready = select([wu_client.sock], [], [], 1)
    print_info("One spin of the loop")
    if ready[0]:
        wu_client.receive()
    else:
        print_info("Ping -->")
        wu_client.conn.ping(DevialetController(wu_client.conn), Devialet.CallMeMaybe.Empty(), pingback)
        # sock.sendto(b'DVL\x01HERE\x00\x00\x00\x08\xB0\xB0\xB0\xB0\xB0\xB0\xB0\xB0', ('255.255.255.255', discovery_port))
        (clientsocket, address) = serversocket.accept()
        print_info('Client {} connected to us!', address)
        data = clientsocket.recv(2048)
        if data:
            print_info('Received {} on server socket', data.hex())
