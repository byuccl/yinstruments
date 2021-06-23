from enum import Enum
import vxi11
class Channel_Element:
    def __init__(self, instr, channel_format, command, command_query):
        self.__instr = instr
        self.channel_format = channel_format
        self.command = command
        self.command_query = command_query
        self.channel = {
            1: None,
            2: None,
            3: None,
            4: None
        }

    def __getitem__(self, key):
        return self.channel[key]

    def __setitem__(self, key, value):
        self.channel[key] = value
        if self.channel[key]:
            command_format = self.channel_format + str(key) + self.command + " " + str(self.channel[key])
            self.__instr.write(command_format)

class Display(Channel_Element):
    def __init__(self, instr, channel_format, command, command_query):
        self.__instr = instr
        super().__init__(instr, channel_format, command, command_query)

    def __getitem__(self, key):
        return self.channel[key]

    def __setitem__(self, key, value):
        if type(value) == int:
            if value:
                self.channel[key] = "ON"
            else:
                self.channel[key] = "OFF"
        elif type(value) == bool:
            if value:
                self.channel[key] = "ON"
            else:
                self.channel[key] = "OFF"
        elif type(value) == str:
            input = str(value).upper()
            if not str(input).find("ON"):
                self.channel[key] = "ON"
            else:
                self.channel[key] = "OFF"
        else:
            self.channel[key] = "ON"        

        if self.channel[key]:
            command_format = self.channel_format + str(key) + self.command + " " + str(self.channel[key])
            self.__instr.write(command_format)               


class Voltage_Range(Channel_Element):
    pass

class Voltage_Division(Channel_Element):
    pass

class Voltage_Offset(Channel_Element):
    pass

class Attenuation(Channel_Element):
    pass

class Wave_Premable(Channel_Element):
    pass

class Wave_Data(Channel_Element):
    pass
    


class Measure_Type(Enum):
    PKPK = 0
    MAX = 1

class Measure_Element(Channel_Element):
    def __init__(self, instr, channel_format, command, command_query):
        self.__instr = instr
        super().__init__(instr, channel_format, command, command_query)

    def __getitem__(self, key):
        command_format = self.command + " " + self.channel_format + str(key)
        self.__instr.write(command_format)
        query_format = self.channel_format + self.command_query + " "
        self.channel[key] = self.__instr.ask(query_format)
        return self.channel[key]

    def __setitem__(self, key, value):
        print("Error: Cannot set measured value.")
