import shlex

from Definition import Packet

class DefLoader:
	def __init__(self, filename):
		self.lexer = shlex.shlex(open(filename, "rt"))

		self.packets = []
		self.load()

	def get_token(self):
		token = self.lexer.get_token()
		if len(token) == 0:
			raise Exception("EOF")
		if len(token) > 1 and token[0] == '"' and token[-1] == '"':
		    return token[1:-1]
		if len(token) > 1 and token[0] == "'" and token[-1] == "'":
		    return token[1:-1]
		return token

	def expect(self, token):
		if self.get_token() != token:
			raise Exception("Expected: " + token)

	def load(self):
		token = self.get_token()
		while len(token) > 0:
			try:
				token = self.get_token()
			except Exception:
				return
			if token == "set":
				self.parse_set()
			elif token == "packet":
				self.packets.append(self.parse_packet())

	def parse_set(self):
		token = self.get_token()
		if token == "transport":
			self.expect("=")
			self.get_token()
			self.expect(";")

	def parse_packet(self):
		messages = []
		self.expect("{")
		token = self.get_token()
		while token != "}":
			if token == "client":
				self.expect(";")
			elif token == "server":
				self.expect(";")
			elif token == "message":
				messages.append(self.parse_message())
			token = self.get_token()

		return Packet(messages)

	def parse_message(self):
		name = self.get_token()
		fields = []
		self.expect("{")
		token = self.get_token()
		while token != "}":
			field_name = token
			self.expect("=")
			field_value = self.get_token()
			token = self.get_token()
			if token == ",":
				token = self.get_token()

			fields.append( (field_name, field_value) )

		return (name, fields)

