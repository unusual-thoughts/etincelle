python2 -m pbd -d ./protoc -o .
rm google/protobuf/descriptor.proto
protoc *.proto !(protobufs_android)/*.proto --python_out=.
