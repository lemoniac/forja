import unittest
from forja.Types import *

class TestTypes(unittest.TestCase):

    def test_int32_le(self):
        i = Integer(32, True)
        
        assert i.encode(0)    == '\x00\x00\x00\x00'
        assert i.encode(1234) == '\xd2\x04\x00\x00'
        assert i.encode(-1) == '\xff\xff\xff\xff'


    def test_int32_be(self):
        i = Integer(32, False)
        
        assert i.encode(0)    == '\x00\x00\x00\x00'
        assert i.encode(1234) == '\x00\x00\x04\xd2'
        assert i.encode(-1) == '\xff\xff\xff\xff'


    def test_string(self):
        s = String()
        
        assert s.encode("hello") == "hello\0"
        assert s.encode("") == "\0"

