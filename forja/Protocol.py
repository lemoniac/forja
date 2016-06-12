class Enum:
    def __init__(self, name, enum_type, items):
        self.name = name
        self.type = enum_type
        self.items = items


    def get(self, key):
        for i in self.items:
            if i[0] == key:
                return i[1]

        raise Exception(key + " is not present in enum " + self.name)


    def get_default(self):
        return self.items[0][1]


class Field:
    def __init__(self, name, fieldtype, valid = None, ignore = False, value = None, enum = None):
        self.name = name
        self.fieldtype = fieldtype
        self.valid = valid
        self.ignore = ignore
        self.value = value
        self.enum = enum


    def __str__(self):
        s = str(self.fieldtype) + " " + self.name

        if self.value != None:
            s += " = " + self.value
        if self.ignore:
            s += " ignore"
        if self.valid != None:
            s += " " + str(self.valid)

        return s


    def set_valid(self, valid):
        self.valid = valid
        if self.value == None and len(self.valid) > 0:
            self.value = self.valid[0]


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
        self.enums = {}
        self.endianness = "little_endian"


    def __str__(self):
        s = self.endianness + "\n"

        for n, m in self.messages.iteritems():
            s += str(m) + "\n"

        return s


    def add_message(self, message):
        self.messages[message.name] = message


    def add_enum(self, enum):
        self.enums[enum.name] = enum

