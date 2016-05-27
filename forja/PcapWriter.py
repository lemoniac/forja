from scapy.all import *
from BinaryWriter import BinaryWriter

class PcapWriter:
    def __init__(self, protocol):
        self.protocol = protocol
        self.writer = BinaryWriter(protocol)

    def write(self, packet):
        s = self.writer.write(packet)

        p = Ether()/IP()/TCP()/s

        return p

    def save(self, packets):
        wrpcap("test.pcap", packets)

