class TextWriter:
    def __init__(self, protocol):
        self.protocol = protocol

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
                    l += fields[field.name]
                elif field.value != None:
                    l += str(field.value)
                else:
                    l += str(field.fieldtype.default())
                s += "        " + l + "\n"

        print s
