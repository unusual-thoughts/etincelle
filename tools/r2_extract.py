import r2pipe
import os
import json
from google.protobuf.descriptor_pb2 import FileDescriptorProto
import google.protobuf.message
from dvlt_output import print_info, print_error, print_warning

dll_dir = '/path/to/spark_dlls'
out_dir = './protoc_new/'

for filename in os.listdir(dll_dir):
    if filename.endswith('.dll'):
        filename = os.path.join(dll_dir, filename)
        print_info('Exploring file {}...', filename)
        f = open(filename, 'rb').read()
        r2 = r2pipe.open(filename)
        r2.cmd('aaa')
        # print_info('Finished analysis')
        sections = json.loads(r2.cmd('Sj'))
        xrefs = r2.cmd('axF InternalAddGeneratedFile|cut -d" " -f2|sort -u').split()

        def get_paddr(vaddr):
            for section in sections:
                if vaddr >= section['vaddr'] and vaddr < section['vaddr'] + section['size']:
                    return vaddr - section['vaddr'] + section['paddr']
            print_error("Can't find virtual address {}", vaddr)
            return 0

        for xref in xrefs:
            disasm = json.loads(r2.cmd('pdj -2 @ ' + xref))
            if disasm[0]['type'] == 'push' and disasm[1]['type'] == 'push':
                length = disasm[0]['val']
                addr = disasm[1]['val']
                # print_info('Found protobuf of length {:6d} at addr 0x{:8x}', length, addr)
                paddr = get_paddr(addr)
                data = f[paddr:paddr+length]
                try:
                    fdp = FileDescriptorProto.FromString(data)
                    print_info('Found FiledescriptorProto of length {:6d} at addr 0x{:08x}: {}', length, paddr, fdp.name, color='green')
                    outfile = open(os.path.join(out_dir, fdp.name.replace('/', '_')), 'wb')
                    outfile.write(data)
                    # print(fdp)
                except google.protobuf.message.DecodeError:
                    print_error('Error while decoding data at offset 0x{:08x}, length {:6d} as FiledescriptorProto', paddr, length)
            else:
                print_warning('No push in immediate vicinity')
