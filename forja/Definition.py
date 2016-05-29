class Packet:
	def __init__(self, messages = [], is_server = False):
		self.messages = messages
		self.is_server = is_server

	def __str__(self):
		s = "Packet:\n"
		for m in self.messages:
			s += "    Message " + m[0] + "\n"
			for f in m[1]:
				s += "        " + f[0] + " = " + f[1] + "\n"
		return s


class Definition:
    def __init__(self):
        self.transport = "TCP"
        self.server_address = ("127.0.0.1", 10000)
        self.client_address = ("127.0.0.1", 10001)

