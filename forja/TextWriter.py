import sys
from Writer import Writer

class TextWriter(Writer):
    def __init__(self, protocol, definition, random = False):
        Writer.__init__(self, protocol, random)
        self.definition = definition


    def write(self, packet):
        s = "Packet:"
        if packet.timestamp != None:
            s += " ts=" + str(packet.timestamp)
        if packet.is_server:
            s += ' ' + str(self.definition.server_address[0]) + ":" + str(self.definition.server_address[1])
            s += ' -> ' + str(self.definition.client_address[0]) + ":" + str(self.definition.client_address[1])
        else:
            s += ' ' + str(self.definition.client_address[0]) + ":" + str(self.definition.client_address[1])
            s += ' -> ' + str(self.definition.server_address[0]) + ":" + str(self.definition.server_address[1])
        s += "\n"
        for m in packet.messages:
            fields = {}
            for f in m[1]:
                fields[f[0]] = f[1]

            message = self.protocol.messages[m[0]]

            s += "    Message " + m[0] + "\n"
            for field in message.fields:
                l = field.name + " = " + str(self.get_value(fields, field))
                s += "        " + l + "\n"

        return s


    def save(self, packets):
        for packet in packets:
            sys.stdout.write(packet)

