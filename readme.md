# Devialet Spark Protocol reverse engineering
- Used `Protod` to extract protobuf descriptors from binaries (either windows app dlls or shared library inside of android APK), then used `pbd` to disassemble them (forked and added support for RPCs)

- Captured traffic and reverse-engineer the encapsulation of the protobufs inside raw TCP frames

## Initial discovery using UDP beacon on port 24242 (`Discovery.dll`)

Request:
```
00000000: 4456 4c01 5748 4f3f                      DVL.WHO?
```

Response:
```
                                     serial length
                                     vv 
00000000: 4456 4c01 4845 5245 0000 00## **** ****  DVL.HERE...#**** 
00000010: **** **** **** **** **        ^^^^^^^^^  *********
          ^^^^^^^^^^^^^^^^^^^^^^        serial
```
Then Spark establishes first TCP connection (including service `WhatsUp.Registry`), also on port 24242

On exit:
```
00000000: 4456 4c01 4259 4521 0000 00## **** ****  DVL.BYE!...#****
00000010: **** **** **** **** **                   *********
```

## Protobuf encapsulation format for RPC requests/responses:
```
C2 01 00 00 00 00
<always empty>
C2 01 00 00 00 <length>
<Devialet.CallMeMaybe.Request or Devialet.CallMeMaybe.Reponse>
...                     \ Usually these are absent,
C2 01 00 00 00 <length> | as there is only one protobuf
<nth protobuf>          | for requests or responses.
...                     / But a special RPC lists all properties
C2 00 00 00 00 <length> (note second byte == 0)
<last protobuf>
```
protobuf encapsulation format for RPC events:
```
C3 01 00 00 00 00
<always empty>
C3 01 00 00 00 10 (length of 16 byte UID)                    \
<16 byte UID> (same as Devialet.CallMeMaybe.Event.serverId)  | extra UID field
C3 01 00 00 00 00                                            |
<always empty>                                               /
C3 01 00 00 00 <length>
<Devialet.CallMeMaybe.Event>
C3 00 00 00 00 <length> (note second byte == 0)
<payload protobuf>
```

The first RPC is `Devialet.CallMeMaybe.Connection.openConnection()` that returns the services on this endpoint (== port)

`Devialet.WhatsUp.Registry` keeps an updated list of endpoints and their services, that can be used to discover new services, and is present on the initial endpoint on port 24242.

<!--```
- Devialet.CallMeMaybe.Request -> Devialet.CallMeMaybe.Reply
- Devialet.CallMeMaybe.ConnectionRequest -> Devialet.CallMeMaybe.ConnectionReply

- Devialet.CallMeMaybe.Request -> Devialet.CallMeMaybe.Reply
- (empty) -> ???

- Devialet.CallMeMaybe.Request -> Devialet.CallMeMaybe.Reply
- (empty) -> (empty)

- Devialet.CallMeMaybe.Request -> Devialet.CallMeMaybe.Reply
- (empty) -> Devialet.CallMeMaybe.ServicesList

- Devialet.CallMeMaybe.Request -> Devialet.CallMeMaybe.Reply
- (empty) -> (empty)
.. repeated
```
-->

<!-- First send a `Devialet.CallMeMaybe.Request` protobuf, the response `Devialet.CallMeMaybe.Reply` contains the RPC parameters. The first RPC is `Devialet.CallMeMaybe.ConnectionRequest`.
Then send the input of the RPC, get the output
 -->
MP3 uploading and playback done via HTTP using service `PickUpThePieces`

Apparently (see disassembly of `CmmClient.dll`), messages use RFC4122 UUIDS (https://en.wikipedia.org/wiki/Universally_unique_identifier)

requestIds are RCF4122 version 4 apparently. the 3 msb bits of byte 8 are 101 or 100 (http://doc.qt.io/qt-4.8/quuid.html#variant-field). the 4 msb bits of byte 6 are 0100 -> random

# List of services
- `AppleAirPlay`: self-explanatory
- `AudioSource` (`TheSoundOfSilence`)
- `CallMeMaybe`: service/message infrastructure (`RPCMessages.proto`, `CallMeMaybe.proto`)
- `Fresh`: Firmware/Software updates
- `GetThePartyStarted`: Setup Wizard/Network config
- `IMASlave4U`: secondary phantom control?
- `LeftAlone`: dummy?
- `MasterOfPuppets`: bouquet/orchestration
- `PickUpThePieces`: audio streaming (http-based)? tracks have URIs like: `dvlt://<8 byte server id>@putp/<18 byte song id>` not in protobufs. HTTP server uses libevent
- `PlayThatFunkyMusic`: not in any protobuf... looks like a derivative of `TooManyFlows`
- `SaveMe`: playlists
- `SpotifyConnect`: self-explanatory
- `TikTok`: not in protobufs, likely microsecond-level synchronization for dialog/phantoms
- `TooManyFlows`: playback control on bouquets
- `TwerkIt`: "Sound design"
- `WhatsUp`: service discovery, initial connection (port 24242)

