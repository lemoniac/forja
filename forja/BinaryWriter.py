import sys
from Writer import Writer

class BinaryWriter(Writer):
    def __init__(self, protocol, random = False):
        Writer.__init__(self, protocol, random)


    def write(self, packet):
        s = ""
        for m in packet.messages:
            fields = {}
            for f in m[1]:
                fields[f[0]] = f[1]

            message = self.protocol.messages[m[0]]

            for field in message.fields:
                value = self.get_value(fields, field)

                if field.islist:
                    for v in value:
                        s += field.fieldtype.encode( field.fieldtype.from_string(v) )
                else:
                    s += field.fieldtype.encode( field.fieldtype.from_string(value) )

        return s


    def save(self, packets):
        for packet in packets:
            sys.stdout.write(packet)

