from scapy.all import *
from BinaryWriter import BinaryWriter

class PcapWriter:
    def __init__(self, protocol, definition):
        self.protocol = protocol
        self.definition = definition
        self.writer = BinaryWriter(protocol)


    def write(self, packet):
        s = self.writer.write(packet)

        p = Ether()/IP()

        if self.definition.transport == "TCP":
            p = p/TCP()
        elif self.definition.transport == "UDP":
            p = p/UDP()
        else:
            raise Exception("Unknown transport: " + self.definition.transport)

        p = p/s

        return p


    def save(self, packets):
        wrpcap("test.pcap", packets)

