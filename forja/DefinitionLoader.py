import shlex

from Definition import Definition, Packet

class DefLoader:
    def __init__(self, src):
        self.lexer = shlex.shlex(src)
        self.lexer.wordchars += "."

        self.definition = Definition()
        self.packets = []
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
            elif token == "packet":
                self.packets.append(self.parse_packet())
            else:
                raise Exception("Unexpected token: " + token)

            try:
                token = self.get_token()
            except Exception:
                return

    def parse_address(self):
        ip = self.get_token()
        self.expect(":")
        port = self.get_token()
        return (ip, int(port))


    def parse_timestamp(self):
        self.expect("=");
        timestamp = float( self.get_token() )
        self.expect(";");
        return timestamp


    def parse_set(self):
        token = self.get_token()

        if token == "transport":
            self.expect("=")
            self.definition.transport = self.get_token()
            self.expect(";")
        elif token == "server_address":
            self.expect("=")
            self.definition.server_address = self.parse_address()
            self.expect(";")
        elif token == "client_address":
            self.expect("=")
            self.definition.client_address = self.parse_address()
            self.expect(";")


    def parse_packet(self):
        messages = []
        is_server = False
        timestamp = None
        self.expect("{")
        token = self.get_token()

        while token != "}":
            if token == "client":
                self.expect(";")
            elif token == "server":
                is_server = True
                self.expect(";")
            elif token == "timestamp":
                timestamp = self.parse_timestamp();
            elif token == "message":
                messages.append(self.parse_message())
            else:
                raise Exception("Unexpected token: " + token)

            token = self.get_token()

        return Packet(messages, is_server, timestamp = timestamp)


    def parse_message(self):
        name = self.get_token()
        fields = []
        self.expect("{")
        token = self.get_token()
        while token != "}":
            field_name = token
            self.expect("=")
            token = self.get_token()
            if token == "[":
                field_value = []
                token = self.get_token()
                while token != "]":
                    field_value.append(token)
                    token = self.get_token()
                    if token == ",":
                        token = self.get_token()

            else:
                field_value = token

            token = self.get_token()
            if token == ",":
                token = self.get_token()

            fields.append( (field_name, field_value) )

        return (name, fields)

