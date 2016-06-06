import sys

class TextWriter:
    def __init__(self, protocol, random = False):
        self.protocol = protocol
        self.random = random


    def write(self, packet):
        s = "Packet:\n"
        for m in packet.messages:
            fields = {}
            for f in m[1]:
                fields[f[0]] = f[1]

            message = self.protocol.messages[m[0]]

            s += "    Message " + m[0] + "\n"
            for field in message.fields:
                l = field.name + " = "
                if field.name in fields:
                    if field.enum == None:
                        l += fields[field.name]
                    else:
                        l += field.enum.get( fields[field.name] )
                elif field.value != None:
                    l += str(field.value)
                elif not field.ignore and self.random:
                    l += str(field.fieldtype.random())
                else:
                    l += str(field.fieldtype.default())
                s += "        " + l + "\n"

        return s


    def save(self, packets):
        for packet in packets:
            sys.stdout.write(packet)

