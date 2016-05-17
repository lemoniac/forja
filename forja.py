#!/usr/bin/env python

import shlex
import sys

types = ["char", "uint8", "int16", "uint16", "int32", "uint32"]

class Field:
	def __init__(self, name, fieldtype, valid = None, ignore = False, value = None):
		self.name = name
		self.fieldtype = fieldtype
		self.valid = valid
		self.ignore = ignore
		self.value = value

	def __str__(self):
		s = self.name

		if self.value != None:
			s += " = " + self.value

		return s

class Message:
	def __init__(self, name, fields):
		self.name = name
		self.fields = fields

	def __str__(self):
		s = "Message: " + self.name + "\n"

		for f in self.fields:
			s += "    " + str(f) + "\n"

		return s

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

class Protocol:
	def __init__(self):
		self.messages = {}
		self.endianness = "littleendian"

	def __str__(self):
		s = self.endianness + "\n"

		for n, m in self.messages.iteritems():
			s += str(m) + "\n"

		return s


	def add_message(self, message):
		self.messages[message.name] = message

class Loader:
	def __init__(self, filename):
		self.lexer = shlex.shlex(open(filename, "rt"))

		self.protocol = Protocol()

		self.load()

	def get_token(self):
		token = self.lexer.get_token()
		if len(token) == 0:
			raise Exception("EOF")
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

		token = self.get_token()
		if token == ";":
			return (field_type, size, field_name)
		elif token == "=":
			value = self.get_token()
			self.expect(";")
			return (field_type, size, field_name, value)
		elif token == ":":
			token = self.get_token()
			if token == "ignore":
				self.expect(";")
			elif token == "valid":
				valid = self.parse_list()
				self.expect(";")
			return (field_type, size, field_name)

class DefLoader:
	def __init__(self, filename):
		self.lexer = shlex.shlex(open(filename, "rt"))

		self.packets = []
		self.load()

	def get_token(self):
		token = self.lexer.get_token()
		if len(token) == 0:
			raise Exception("EOF")
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

loader = Loader(sys.argv[1])
def_loader = DefLoader(sys.argv[2])

print loader.protocol
print "\n---\n"
for p in def_loader.packets:
	print p