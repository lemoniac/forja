import copy
import shlex
from Protocol import Field, Message, Protocol
from Types import create_type

types = ["char", "uint8", "int16", "uint16", "int32", "uint32"]

class Loader:
    def __init__(self, filename):
        self.lexer = shlex.shlex(open(filename, "rt"))

        self.protocol = Protocol()
        self.structs = {}

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
            if token == "set":
                self.parse_set()
            elif token == "struct":
                s = self.parse_struct()
                self.structs[s.name] = s
            elif token == "message":
                self.protocol.add_message( self.parse_struct() )
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
            if token in types:
                fields.append( self.parse_field(token) )
            elif token in self.structs:
                for f in self.parse_user_type(token):
                    fields.append(f)
            else:
                raise Exception("Type expected, found: " + token)

            token = self.get_token()

        return Message(name, fields)


    def parse_user_type(self, name):
        self.expect("(")
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
            l.append( c )

        return l


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
            else:
                raise Exception("Unknown field modifier: " + token)
        return field

