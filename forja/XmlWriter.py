import sys
from Writer import Writer

class XmlWriter(Writer):
    def __init__(self, protocol, random = False):
        Writer.__init__(self, protocol, random)


    def write(self, packet):
        s = "  <packet>\n"
        for m in packet.messages:
            fields = {}
            for f in m[1]:
                fields[f[0]] = f[1]

            message = self.protocol.messages[m[0]]

            s += '    <message name="' + m[0] + '">\n'
            for field in message.fields:
                l = '<field name="' + field.name + '" value="' + str(self.get_value(fields, field)) + '"/>'
                s += "      " + l + "\n"
            s += '    </message>\n'

        s += "  </packet>\n"
        return s


    def save(self, packets):
        sys.stdout.write("<packets>\n")
        for packet in packets:
            sys.stdout.write(packet)
        sys.stdout.write("</packets>\n")

