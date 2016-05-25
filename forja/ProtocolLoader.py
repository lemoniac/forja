import shlex
from Protocol import Field, Message, Protocol
from Types import create_type

types = ["char", "uint8", "int16", "uint16", "int32", "uint32"]

class Loader:
	def __init__(self, filename):
		self.lexer = shlex.shlex(open(filename, "rt"))

		self.protocol = Protocol()

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
			elif token == "struct" or token == "message":
				self.protocol.add_message( self.parse_struct() )

	def parse_set(self):
		token = self.get_token()
		if token == "little_endian":
			self.expect(";")

	def parse_struct(self):
		name = self.get_token()
		fields = []
		self.expect("{")
		token = self.get_token()
		while token != "}":
			fields.append( self.parse_field(token) )

			token = self.get_token()

		return Message(name, fields)

	def parse_list(self):
		l = []
		self.expect("(")
		token = self.get_token()
		while token != ")":
			l.append(token)
			token = self.get_token()
			if token == ",":
				token = self.get_token()

		return l

	def parse_field(self, field_type):
		if not field_type in types:
			raise Exception("Type expected, found: " + field_type)

		token = self.get_token()
		size = 1

		if field_type == "char" and token == "[":
			size = int(self.get_token())
			self.expect("]")
			token = self.get_token()

		field_name = token

		field = Field(field_name, create_type(field_type, size, True))

		token = self.get_token()
		if token == ";":
			return field
		elif token == "=":
			field.value = self.get_token()
			self.expect(";")
			return field
		elif token == ":":
			token = self.get_token()
			if token == "ignore":
				field.ignore = True
				self.expect(";")
			elif token == "valid":
				field.valid = self.parse_list()
				self.expect(";")
			return field
