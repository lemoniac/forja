import sys
from forja import ProtocolLoader

import xml.sax


class Message:
    def __init__(self, name):
        self.name = name
        self.fields = []


class XmlParser(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)


    def startElement(self, name, attrs):
        if name == "message":
            self.message = Message( attrs.getValue("name") )
        elif name == "field":
            self.message.fields.append( (attrs.getValue("name"), attrs.getValue("value")) )


    def endElement(self, name):
        if name == "message":
            print self.message.name
            print self.message.fields
            self.message = None


def main():
    loader = ProtocolLoader.Loader( open(sys.argv[1], "rt") )

    xml.sax.parse( open(sys.argv[2]), XmlParser() )


