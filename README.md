# DESCRIPTION

**Forja** creates pcaps based on a description of a protocol and a description of the messages that they will contain.

    forja [OPTIONS] protocol messages


# OPTIONS
    -h
    -t (b|p|t)     Format of the output (binary, pcap, text)


# Definition files

## Protocol

    set little_endian;
    
    message Message1 {
        uint8 field1 = 2;
        uint8 reserved : ignored;
        uint16 "Field 2";
        char[10] field3;
        int32 field4 : valid(1, 54, 876);
    }


## Messages

    packet {
      server;
      message Message1 { "Field 2" = 123, field3 = "123" }
    }

