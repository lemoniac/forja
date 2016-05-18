from struct import pack

class Integer:
    def __init__(self, width, LE = True):
        self.width = width
        self.endianness = "<" if LE else ">"
        
    def encode(self, value):
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



class String:
    def encode(self, value):
        return value + '\0'

