from scapy.all import *
from BinaryWriter import BinaryWriter
from Writer import Writer

class PcapWriter(Writer):
    def __init__(self, protocol, definition, outfile, random = False):
        Writer.__init__(self, protocol, random)
        self.definition = definition
        self.writer = BinaryWriter(protocol, random = random)
        self.outfile = outfile


    def write(self, packet):
        s = self.writer.write(packet)

        if packet.is_server:
            dst_address = self.definition.client_address[0]
            dst_port=self.definition.client_address[1]
            src_address = self.definition.server_address[0]
            src_port=self.definition.server_address[1]
        else:
            src_address = self.definition.client_address[0]
            src_port=self.definition.client_address[1]
            dst_address = self.definition.server_address[0]
            dst_port=self.definition.server_address[1]


        p = Ether()/IP(src=src_address,dst=dst_address)

        if self.definition.transport == "TCP":
            p = p/TCP(sport=src_port,dport=dst_port,seq=0,flags="PA",ack=0)
        elif self.definition.transport == "UDP":
            p = p/UDP(sport=src_port,dport=dst_port)
        else:
            raise Exception("Unknown transport: " + self.definition.transport)

        p = p/s

        if packet.timestamp != None:
            p.time = packet.timestamp

        return p


    def save(self, packets):
        wrpcap(self.outfile, packets)

