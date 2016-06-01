import unittest
from forja.ProtocolLoader import *

def check_syntax(src):
    try:
        loader = Loader(src)
        return ""
    except Exception as e:
        return str(e)


class TestProtocolLoader(unittest.TestCase):

    def test_message(self):
        loader = Loader("""message Msg { }""")
        msgs = loader.protocol.messages
        assert len(msgs) == 1
        assert "Msg" in msgs

        loader = Loader('message "A message" { }')
        msgs = loader.protocol.messages
        assert len(msgs) == 1
        assert "A message" in msgs


    def test_struct(self):
        loader = Loader("""
            struct S {
                int32 i;
            }

            message M {
                S s();
                S();
            }""")
        m = loader.protocol.messages["M"]
        print m


    def test_syntax_error(self):
        assert check_syntax("""message Msg { }""") == ""
        assert check_syntax("""message Msg { """) == "EOF"
        #assert check_syntax("""message { """) == ""
        assert check_syntax("""message Msg {
                type asd;
            }""") == "Type expected, found: type"

