class Field:
	def __init__(self, name, fieldtype, valid = None, ignore = False, value = None):
		self.name = name
		self.fieldtype = fieldtype
		self.valid = valid
		self.ignore = ignore
		self.value = value

	def __str__(self):
		s = str(self.fieldtype) + " " + self.name

		if self.value != None:
			s += " = " + self.value
		if self.ignore:
			s += " ignore"
		if self.valid != None:
			s += " " + str(self.valid)

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

