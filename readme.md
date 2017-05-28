# Devialet Spark Protocol reverse engineering
Use `Protod` to extract protobuf descriptors from binaries (either windows app dlls or shared library inside of android APK), then use `pbd` to disassemble them (added support for RPCs)

Capture traffic and reverse-engineer the encapsulation of the protobufs inside raw TCP frames

Initial discovery using UDP beacon on port 24242 (`Discovery.dll`)

Request:
```
00000000: 4456 4c01 5748 4f3f                      DVL.WHO?
```

Response (In Android capture): (maybe Spark version ID)
```
00000000: 4456 4c01 4845 5245 0000 0008 **** ****  DVL.HERE.....\s.
00000010: **** ****                                S...
```

In Windows capture
```
                                     serial length
                                     vv 
00000000: 4456 4c01 4845 5245 0000 00## **** ****  DVL.HERE...#**** 
00000010: **** **** **** **** **        ^^^^^^^^^  *********
          ^^^^^^^^^^^^^^^^^^^^^^        serial
```
Then Spark establishes first TCP connection, also on port 24242

protobuf encapsulation format:
```
C2/C3 01 00 00 00 00
<always empty?>
C2/C3 01 00 00 00 10 (length of 16 byte UID) )
<16 byte UID> (changes often)                ) OPTIONAL
C2/C3 01 00 00 00 00                         )
<always empty?>                              )
C2/C3 01 00 00 00 <length>
<first protobuf>
...
C2/C3 01 00 00 00 <length>
<nth protobuf>
...
C2/C3 00 00 00 00 <length> (note second byte == 0)
<last protobuf>
```
This structure is repeated any number of times in each packet

Apparently (see disassembly of `CmmClient.dll`) it uses RFC4122 UUIDS (https://en.wikipedia.org/wiki/Universally_unique_identifier)

<!-- - The First at least 3 protobuf packets from Spark appear to be `Devialet.CallMeMaybe.Request` (from `RPCMessages.proto`)
- The very first may actually be `Devialet.CallMeMaybe.ServiceProperty` (from `CallMeMaybe.proto`) -->

```
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

First send a `Devialet.CallMeMaybe.Request` protobuf, the response `Devialet.CallMeMaybe.Reply` contains the RPC parameters. The first RPC is `Devialet.CallMeMaybe.ConnectionRequest`.
Then send the input of the RPC, get the output

MP3 uploading and playback done via HTTP

# List of services
- `CallMeMaybe`: service/message infrastructure (also related to RPCMessages?)
- `GetThePartyStarted`: Setup Wizard
- `Fresh`: Firmware/Software updates