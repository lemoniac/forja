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

class Message:
	def __init__(self, name, fields):
		self.name = name
		self.fields = fields

class Packet:
	def __init__(self, messages = []):
		self.messages = messages

class Protocol:
	def __init__(self):
		self.messages = []
		self.endianness = "littleendian"

class Loader:
	def __init__(self, filename):
		self.lexer = shlex.shlex(open(filename, "rt"))

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
			print token
			try:
				token = self.get_token()
			except Exception:
				return
			if token == "set":
				self.parse_set()
			elif token == "struct" or token == "message":
				self.parse_struct()

	def parse_set(self):
		token = self.get_token()
		print token
		if token == "little_endian":
			self.expect(";")

	def parse_struct(self):
		name = self.get_token()
		self.expect("{")
		token = self.get_token()
		while token != "}":
			field = self.parse_field(token)
			print field
			token = self.get_token()

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
				print valid
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
			print token
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
			token = self.get_token()

		return Message(name, fields)

loader = Loader(sys.argv[1])
def_loader = DefLoader(sys.argv[2])
