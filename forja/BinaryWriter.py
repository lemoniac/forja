import sys

class BinaryWriter:
    def __init__(self, protocol):
        self.protocol = protocol

    def write(self, packet):
        s = ""
        for m in packet.messages:
            fields = {}
            for f in m[1]:
                fields[f[0]] = f[1]

            message = self.protocol.messages[m[0]]

            for field in message.fields:
                if field.name in fields:
                    value = fields[field.name]
                elif field.value != None:
                    value = field.value
                else:
                    value = field.fieldtype.default()

                s += field.fieldtype.encode( field.fieldtype.from_string(value) )

        return s

    def save(self, packets):
        for packet in packets:
            sys.stdout.write(packet)

