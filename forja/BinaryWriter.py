import sys

class BinaryWriter:
    def __init__(self, protocol, random = False):
        self.protocol = protocol
        self.random = random


    def write(self, packet):
        s = ""
        for m in packet.messages:
            fields = {}
            for f in m[1]:
                fields[f[0]] = f[1]

            message = self.protocol.messages[m[0]]

            for field in message.fields:
                if field.name in fields:
                    if field.enum == None:
                        value = fields[field.name]
                    else:
                        value = field.enum.get( fields[field.name] )
                elif field.value != None:
                    value = field.value
                elif not field.ignore and self.random:
                    value = field.fieldtype.random()
                else:
                    value = field.fieldtype.default()

                s += field.fieldtype.encode( field.fieldtype.from_string(value) )

        return s


    def save(self, packets):
        for packet in packets:
            sys.stdout.write(packet)

