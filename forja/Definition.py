class Packet:
	def __init__(self, messages = []):
		self.messages = messages

	def __str__(self):
		s = "Packet:\n"
		for m in self.messages:
			s += "    Message " + m[0] + "\n"
			for f in m[1]:
				s += "        " + f[0] + " = " + f[1] + "\n"
		return s

