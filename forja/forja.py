import sys

from DefinitionLoader import DefLoader

from Protocol import Field, Message, Protocol
from ProtocolLoader import Loader

from TextWriter import TextWriter


def main():
    loader = Loader(sys.argv[1])
    def_loader = DefLoader(sys.argv[2])

    writer = TextWriter(loader.protocol)

    for p in def_loader.packets:
        print writer.write(p)

