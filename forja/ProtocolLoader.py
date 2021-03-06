import copy
import shlex
from Protocol import Enum, Field, Message, Protocol
from Types import create_type

FIELD_TYPES = ["char", "int8", "uint8", "int16", "uint16", "int32", "uint32", "int64", "uint64", "string", "lenstring"]

class Loader(object):
    def __init__(self, src):
        self.lexer = shlex.shlex(src)
        self.lexer.wordchars += "."

        self.protocol = Protocol()
        self.structs = {}

        self.token = ""
        self.token_type = ""

        self.load()



    def get_token(self):
        self.token = self.lexer.get_token()
        if len(self.token) == 0:
            raise Exception("EOF")
        if len(self.token) > 1 and self.token[0] == '"' and self.token[-1] == '"':
            self.token_type = "str"
            return self.token[1:-1]
        if len(self.token) > 1 and self.token[0] == "'" and self.token[-1] == "'":
            self.token_type = "str"
            return self.token[1:-1]

        self.token_type = ""
        return self.token


    def expect(self, token):
        t = self.get_token()
        if t != token:
            raise Exception("Expected: " + token + " found " + t)


    def load(self):
        token = self.get_token()
        while len(token) > 0:
            if token == "set":
                self.parse_set()
            elif token == "struct":
                s = self.parse_struct()
                self.structs[s.name] = s
            elif token == "message":
                self.protocol.add_message( self.parse_struct() )
            elif token == "enum":
                self.protocol.add_enum( self.parse_enum() )
            elif token == "const":
                self.parse_const()
            else:
                raise Exception("Unexpected token: " + token)

            try:
                token = self.get_token()
            except Exception:
                return


    def parse_set(self):
        token = self.get_token()
        if token == "little_endian":
            self.protocol.endianness = "little_endian"
            self.expect(";")
        elif token == "big_endian":
            self.protocol.endianness = "big_endian"
            self.expect(";")
        else:
            raise Exception("Unknown set: " + token)


    def parse_struct(self):
        name = self.get_token()
        fields = []
        self.expect("{")
        token = self.get_token()
        while token != "}":
            if token in FIELD_TYPES:
                fields.append( self.parse_field(token) )
            elif token in self.structs:
                for f in self.parse_user_type(token):
                    fields.append(f)
            elif token in self.protocol.enums:
                fields.append( self.parse_enum_instance(token) )
            else:
                raise Exception("Type expected, found: " + token)

            token = self.get_token()

        return Message(name, fields)


    def parse_user_type(self, name):
        token = self.get_token()
        if token != "(":
            prefix = token + "."
            self.expect("(")
        else:
            prefix = None

        token = self.get_token()
        fields = {}
        while token != ")":
            field_name = token

            self.expect("=")
            field_value = self.get_token()

            token = self.get_token()
            if token == ',':
                token = self.get_token()

            fields[field_name] = field_value

        self.expect(";")

        l = []
        for f in self.structs[name].fields:
            c = copy.copy(f)
            if c.name in fields:
                c.value = fields[c.name]

            if prefix != None:
                c.name = prefix + c.name

            l.append(c)

        return l


    def parse_enum_instance(self, name):
        field_name = self.get_token()
        token = self.get_token()
        enum = self.protocol.enums[name]
        if token == ";":
            field_value = enum.get_default()
            return Field(field_name, self.protocol.enums[name].type, value=field_value, enum=enum)
        elif token != "=":
            raise Exception("Expected ';' or '=', found: " + token)

        field_value = self.get_token()
        self.expect(";")

        return Field(field_name, enum.type, value=enum.get(field_value), enum=enum)


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
        token = self.get_token()

        bits = None
        if token == ":":
            bits = int(self.get_token())
            token = self.get_token()

        size = 1

        if field_type == "char" and token == "[":
            size = int(self.get_token())
            self.expect("]")
            token = self.get_token()

        field_name = token

        field = Field(field_name, create_type(field_type, size, self.protocol.endianness == "little_endian"))
        if bits != None:
            field.bits = bits

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
                field.set_valid( self.parse_list() )
                self.expect(";")
            elif token == "list":
                field.islist = True
                self.expect(";")
            else:
                raise Exception("Unknown field modifier: " + token)

        return field


    def parse_enum(self):
        name = self.get_token()
        self.expect(":")
        enum_type = self.get_token()
        items = []
        self.expect("{")
        token = self.get_token()
        while token != "}":
            item_name = token
            self.expect("=")
            item_value = self.get_token()

            token = self.get_token()
            if token == ",":
                token = self.get_token()

            items.append( (item_name, item_value) )

        return Enum(name, create_type(enum_type, 1, self.protocol.endianness == "little_endian"), items)


    def parse_const(self):
        name = self.get_token()
        self.expect("=")
        value = self.get_token()
        self.expect(";")

        self.protocol.consts[name] = value
