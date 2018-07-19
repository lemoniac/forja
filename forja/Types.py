from struct import pack
import random

class Integer:
    def __init__(self, width, signed = False, LE = True):
        self.width = width
        self.endianness = "<" if LE else ">"
        self.signed = signed


    def __str__(self):
        if self.signed:
            return "int" + str(self.width)
        else:
            return "uint" + str(self.width)


    def __len__(self):
        return self.width / 8


    def default(self):
       return 0


    def random(self):
        if self.signed:
            return random.randrange(-(1<<(self.width - 1)), ((1<<(self.width-1)) - 1))
        else:
            return random.randrange(0, (1<<self.width) - 1)


    def from_string(self, value):
        if type(value) == str and value.startswith("0x"):
            return int(value, 16)
        return int(value)


    def encode(self, value):
        if self.signed:
            if self.width == 8:
                return pack(self.endianness + "b", value)
            elif self.width == 16:
                return pack(self.endianness + "h", value)
            elif self.width == 32:
                return pack(self.endianness + "i", value)
            elif self.width == 64:
                return pack(self.endianness + "q", value)
            else:
                raise Exception("wrong width")
        else:
            if self.width == 8:
                return pack(self.endianness + "B", value)
            elif self.width == 16:
                return pack(self.endianness + "H", value)
            elif self.width == 32:
                return pack(self.endianness + "I", value)
            elif self.width == 64:
                return pack(self.endianness + "Q", value)
            else:
                raise Exception("wrong width")


class Fixed:
    def __init__(self, length):
        self.length = length


    def __str__(self):
        if self.length == 1:
            return "char"
        else:
            return "char[" + str(self.length) + "]"


    def __len__(self):
        return self.length


    def default(self):
        return ""


    def random(self):
        l = random.randint(0, self.length)
        s = ""
        for i in xrange(l):
            s += chr(random.randint(65, 90))

        return s


    def from_string(self, value):
        return value


    def encode(self, value):
        return pack(str(self.length) + "s", value)


class String:
    """Null terminated string"""

    def __len__(self):
        return self.length + 1

    def encode(self, value):
        return value + '\0'

    def from_string(self, value):
        return value

    def default(self):
        return ""


class LenString:
    """Length+string"""

    def __len__(self):
        return self.length + 1

    def encode(self, value):
        return pack("<b", len(value)) + value

    def from_string(self, value):
        return value

    def default(self):
        return '\0'


def create_type(name, length, LE):
    if name == "int8":
        return Integer(8, True, LE)
    if name == "int16":
        return Integer(16, True, LE)
    if name == "int32":
        return Integer(32, True, LE)
    if name == "int64":
        return Integer(64, True, LE)

    if name == "uint8":
        return Integer(8, False, LE)
    if name == "uint16":
        return Integer(16, False, LE)
    if name == "uint32":
        return Integer(32, False, LE)
    if name == "uint64":
        return Integer(64, False, LE)

    if name == "char":
        return Fixed(length)

    if name == "string":
        return String()
    if name == "lenstring":
        return LenString()

