class Packet(object):
    def __init__(self, messages=None, is_server=False, timestamp=None):
        if messages is None:
            self.messages = []
        else:
            self.messages = messages
        self.is_server = is_server
        self.timestamp = timestamp


    def __str__(self):
        s = "Packet:\n"
        for m in self.messages:
            s += "    Message " + m[0] + "\n"
            for f in m[1]:
                s += "        " + f[0] + " = " + f[1] + "\n"
        return s


class Definition(object):
    def __init__(self):
        self.transport = "TCP"
        self.server_address = ("127.0.0.1", 10000)
        self.client_address = ("127.0.0.1", 10001)

