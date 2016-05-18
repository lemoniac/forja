import sys

from DefinitionLoader import DefLoader

from Protocol import Field, Message, Protocol
from ProtocolLoader import Loader


def main():
    loader = Loader(sys.argv[1])
    def_loader = DefLoader(sys.argv[2])

    print loader.protocol
    print "\n---\n"
    for p in def_loader.packets:
	    print p

