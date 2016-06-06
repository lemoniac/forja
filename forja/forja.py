import argparse
import sys

from DefinitionLoader import DefLoader

from Protocol import Field, Message, Protocol
from ProtocolLoader import Loader


def main():

    parser = argparse.ArgumentParser(prog="forja")
    parser.add_argument('files', type=str, nargs=2, help="protocol packets")
    parser.add_argument('-t', dest='format', default='t', help="Format (b=binary, p=pcap, t=text)")
    parser.add_argument('-o', dest='outfile', help='output file')
    parser.add_argument('-r', action='store_true', dest='random', help='fill fields with random values')

    args = parser.parse_args(sys.argv[1:])

    loader = Loader( open(args.files[0], "rt") )
    def_loader = DefLoader( open(args.files[1], "rt") )

    if args.format == 't':
        from TextWriter import TextWriter
        writer = TextWriter(loader.protocol, random=args.random)
    elif args.format == 'b':
        from BinaryWriter import BinaryWriter
        writer = BinaryWriter(loader.protocol, random=args.random)
    elif args.format == 'p':
        if args.outfile == None:
            print "Error: output format 'pcap' needs an output file [-o filename]"
            return 1
        from PcapWriter import PcapWriter
        writer = PcapWriter(loader.protocol, def_loader.definition, args.outfile, random=args.random)
    else:
        raise Exception("Unknown format")

    packets = []
    for p in def_loader.packets:
         packets.append( writer.write(p) )

    writer.save(packets)

