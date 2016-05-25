import argparse
import sys

from DefinitionLoader import DefLoader

from Protocol import Field, Message, Protocol
from ProtocolLoader import Loader

from TextWriter import TextWriter
from BinaryWriter import BinaryWriter


def main():

    parser = argparse.ArgumentParser(prog="forja")
    parser.add_argument('files', type=str, nargs=2, help="protocol packets")
    parser.add_argument('-t', dest='format', default='t', help="Format (b=binary, p=pcap, t=text)")

    args = parser.parse_args(sys.argv[1:])

    loader = Loader(args.files[0])
    def_loader = DefLoader(args.files[1])

    if args.format == 't':
        writer = TextWriter(loader.protocol)
    elif args.format == 'b':
        writer = BinaryWriter(loader.protocol)

    for p in def_loader.packets:
        writer.write(p)

