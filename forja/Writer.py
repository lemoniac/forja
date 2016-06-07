class Writer:
    def __init__(self, protocol, random = False):
        self.protocol = protocol
        self.random = random


    def get_value(self, fields, field):
        if field.name in fields:
            if field.enum == None:
                value = fields[field.name]
            else:
                value = field.enum.get( fields[field.name] )
        elif field.value != None:
            value = field.value
        elif not field.ignore and self.random:
            value = field.fieldtype.random()
        else:
            value = field.fieldtype.default()

        return value

