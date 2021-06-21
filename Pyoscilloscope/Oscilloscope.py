import vxi11
import re
import json
from enum import Enum


class TriggerSweep(Enum):
    NORM = 0
    AUTO = 1
    SINGLE = 2
    STOP = 3

class TriggerMode(Enum):
    EDGE = 0
    GLIT = 1
    HV = 2
    HT = 3
    IL = 4
    INTV = 5
    IS = 6
    PL = 7
    PS = 8
    SR = 9
    TI = 10
    TV = 11
    CHAR = 12
    LPIC = 13
    LINE = 14
                           
class AcquisitionMode(Enum):
    SAMPLING = 0
    PDE = 1
    AVERAGE = 2
    HIGH_RES = 3


class Scope:
    def __init__(self, ip_address=None, commands_file=None):
        self._ip_address = ip_address
        
        if ip_address:
            self.__instr = vxi11.Instrument(self._ip_address)
            self.__connected = True
        else:
            self.__instr = None    
            self.__connected = False

        self._display_on_channel_1 = None
        self._display_on_channel_2 = None
        self._display_on_channel_3 = None
        self._display_on_channel_4 = None     

        self._voltage_range_channel_1 = None
        self._voltage_range_channel_2 = None
        self._voltage_range_channel_3 = None
        self._voltage_range_channel_4 = None

        self._voltage_division_channel_1 = None
        self._voltage_division_channel_2 = None
        self._voltage_division_channel_3 = None
        self._voltage_division_channel_4 = None

        self._voltage_offset = [None, None, None, None]
        self._time_range = None
        self._time_delay = None

        self._trigger_sweep = None
        self._trigger_mode = None
        self._trigger_source = None

        self._acquisition_mode = None

        if commands_file == None:
            with open("oscilloscope_commands_default.json") as f:
                self.__command_list = json.load(f)
        else:
            with open(commands_file) as f:
                self.__command_list = json.load(f)

    @property
    def display_on_channel_1(self):
        if self.__connected:
            request = self.__command_list["display_channel_1"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_display = re.search(r"[ONF]+", scope_value).group(0)
            if scope_display != self._display_on_channel_1:
                print("Warning: current scope display setting is", scope_display, "rather than", self._display_on_channel_1, " Setting to actual value", scope_display)
                self._display_on_channel_1 = scope_display        
        return self._display_on_channel_1

    @display_on_channel_1.setter
    def display_on_channel_1(self, value):
        if (type(value) == int or type(value) == bool):
            if value:
                self._display_on_channel_1 = "ON"
            else:
                self._display_on_channel_1 = "OFF"
        elif (type(value) == str):
            self._display_on_channel_1
        else:
            self._display_on_channel_1 = "ON"                
        
        if self._display_on_channel_1:
            if self.__connected:
                request = self.__command_list["display_channel_1"] + " " + str(self._display_on_channel_1)
                self.__instr.write(request)

    @property
    def display_on_channel_2(self):
        if self.__connected:
            request = self.__command_list["display_channel_2"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_display = re.search(r"[ONF]+", scope_value).group(0)
            if scope_display != self._display_on_channel_2:
                print("Warning: current scope display setting is", scope_display, "rather than", self._display_on_channel_2, " Setting to actual value", scope_display)
                self._display_on_channel_2 = scope_display        
        return self._display_on_channel_2

    @display_on_channel_2.setter
    def display_on_channel_2(self, value):
        if (type(value) == int or type(value) == bool):
            if value:
                self._display_on_channel_2 = "ON"
            else:
                self._display_on_channel_2 = "OFF"
        elif (type(value) == str):
            self._display_on_channel_2
        else:
            self._display_on_channel_2 = "ON"                
        
        if self._display_on_channel_2:
            if self.__connected:
                request = self.__command_list["display_channel_2"] + " " + str(self._display_on_channel_2)
                self.__instr.write(request)            
    
    
    @property
    def display_on_channel_3(self):
        if self.__connected:
            request = self.__command_list["display_channel_3"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_display = re.search(r"[ONF]+", scope_value).group(0)
            if scope_display != self._display_on_channel_3:
                print("Warning: current scope display setting is", scope_display, "rather than", self._display_on_channel_3, " Setting to actual value", scope_display)
                self._display_on_channel_3 = scope_display        
        return self._display_on_channel_3

    @display_on_channel_3.setter
    def display_on_channel_3(self, value):
        if (type(value) == int or type(value) == bool):
            if value:
                self._display_on_channel_3 = "ON"
            else:
                self._display_on_channel_3 = "OFF"
        elif (type(value) == str):
            self._display_on_channel_3
        else:
            self._display_on_channel_3 = "ON"                
        
        if self._display_on_channel_3:
            if self.__connected:
                request = self.__command_list["display_channel_3"] + " " + str(self._display_on_channel_3)
                self.__instr.write(request)

    @property
    def display_on_channel_4(self):
        if self.__connected:
            request = self.__command_list["display_channel_4"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_display = re.search(r"[ONF]+", scope_value).group(0)
            if scope_display != self._display_on_channel_4:
                print("Warning: current scope display setting is", scope_display, "rather than", self._display_on_channel_4, " Setting to actual value", scope_display)
                self._display_on_channel_4 = scope_display        
        return self._display_on_channel_4

    @display_on_channel_4.setter
    def display_on_channel_4(self, value):
        if (type(value) == int or type(value) == bool):
            if value:
                self._display_on_channel_4 = "ON"
            else:
                self._display_on_channel_4 = "OFF"
        elif (type(value) == str):
            self._display_on_channel_4
        else:
            self._display_on_channel_4 = "ON"                
        
        if self._display_on_channel_4:
            if self.__connected:
                request = self.__command_list["display_channel_4"] + " " + str(self._display_on_channel_4)
                self.__instr.write(request)

    @property
    def voltage_range_channel_1(self):
        if self.__connected:
            request = self.__command_list["voltage_range_channel_1"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_range = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_range != self._voltage_range_channel_1:
                print("Warning: current scope time range setting is", scope_voltage_range, "rather than", self._voltage_range_channel_1, " Setting to actual value", scope_voltage_range)
                self._voltage_range_channel_1 = scope_voltage_range
        return self._voltage_range_channel_1    

    @voltage_range_channel_1.setter
    def voltage_range_channel_1(self, value):
        self._voltage_range_channel_1 = value
        if self.voltage_range_channel_1:
            if self.__connected:
                request = self.__command_list["voltage_range_channel_1"] + " " + str(value)
                self.__instr.write(request)

    @property
    def voltage_range_channel_2(self):
        if self.__connected:
            request = self.__command_list["voltage_range_channel_2"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_range = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_range != self._voltage_range_channel_2:
                print("Warning: current scope time range setting is", scope_voltage_range, "rather than", self._voltage_range_channel_2, " Setting to actual value", scope_voltage_range)
                self._voltage_range_channel_2 = scope_voltage_range
        return self._voltage_range_channel_2

    @voltage_range_channel_2.setter
    def voltage_range_channel_2(self, value):
        self._voltage_range_channel_2 = value
        if (self.voltage_range_channel_2):
            if self.__connected:
                request = self.__command_list["voltage_range_channel_2"] + " " + str(value)
                self.instr.write(request)

    @property
    def voltage_range_channel_3(self):
        if self.__connected:
            request = self.__command_list["voltage_range_channel_3"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_range = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_range != self._voltage_range_channel_3:
                print("Warning: current scope time range setting is", scope_voltage_range, "rather than", self._voltage_range_channel_3, " Setting to actual value", scope_voltage_range)
                self._voltage_range_channel_3 = scope_voltage_range
        return self._voltage_range_channel_3

    @voltage_range_channel_3.setter
    def voltage_range_channel_3(self, value):
        self._voltage_range_channel_3 = value
        if (self.voltage_range_channel_3):
            if self.__connected:
                request = self.__command_list["voltage_range_channel_3"] + " " + str(value)
                self.instr.write(request)

    @property
    def voltage_range_channel_4(self):
        if self.__connected:
            request = self.__command_list["voltage_range_channel_4"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_range = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_range != self._voltage_range_channel_4:
                print("Warning: current scope time range setting is", scope_voltage_range, "rather than", self._voltage_range_channel_4, " Setting to actual value", scope_voltage_range)
                self._voltage_range_channel_4 = scope_voltage_range
        return self._voltage_range_channel_4

    @voltage_range_channel_4.setter
    def voltage_range_channel_4(self, value):
        self._voltage_range_channel_4 = value
        if (self.voltage_range_channel_4):
            if self.__connected:
                request = self.__command_list["voltage_range_channel_4"] + " " + str(value)
                self.instr.write(request)                        


    @property
    def voltage_division_channel_1(self):
        if self.__connected:
            request = self.__command_list["voltage_division_channel_1"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_division = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_division != self._voltage_division_channel_1:
                print("Warning: current scope time range setting is", scope_voltage_division, "rather than", self._voltage_division_channel_1, " Setting to actual value", scope_voltage_division)
                self._voltage_division_channel_1 = scope_voltage_division
        return self._voltage_division_channel_1    

    @voltage_division_channel_1.setter
    def voltage_division_channel_1(self, value):
        self._voltage_division_channel_1 = value
        if (self.voltage_division_channel_1):
            if self.__connected:
                request = self.__command_list["voltage_division_channel_1"] + " " + str(value)
                self.__instr.write(request)

    @property
    def voltage_division_channel_2(self):
        if self.__connected:
            request = self.__command_list["voltage_division_channel_2"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_division = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_division != self._voltage_division_channel_2:
                print("Warning: current scope time range setting is", scope_voltage_division, "rather than", self._voltage_division_channel_2, " Setting to actual value", scope_voltage_division)
                self._voltage_division_channel_2 = scope_voltage_division
        return self._voltage_division_channel_2

    @voltage_division_channel_2.setter
    def voltage_division_channel_2(self, value):
        self._voltage_division_channel_2 = value
        if (self.voltage_division_channel_2):
            if self.__connected:
                request = self.__command_list["voltage_division_channel_2"] + " " + str(value)
                self.instr.write(request)

    @property
    def voltage_division_channel_3(self):
        if self.__connected:
            request = self.__command_list["voltage_division_channel_3"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_division = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_division != self._voltage_division_channel_3:
                print("Warning: current scope time range setting is", scope_voltage_division, "rather than", self._voltage_division_channel_3, " Setting to actual value", scope_voltage_division)
                self._voltage_division_channel_3 = scope_voltage_division
        return self._voltage_division_channel_3

    @voltage_division_channel_3.setter
    def voltage_division_channel_3(self, value):
        self._voltage_division_channel_3 = value
        if (self.voltage_division_channel_3):
            if self.__connected:
                request = self.__command_list["voltage_division_channel_3"] + " " + str(value)
                self.instr.write(request)

    @property
    def voltage_division_channel_4(self):
        if self.__connected:
            request = self.__command_list["voltage_division_channel_4"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_division = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_division != self._voltage_division_channel_4:
                print("Warning: current scope time range setting is", scope_voltage_division, "rather than", self._voltage_division_channel_4, " Setting to actual value", scope_voltage_division)
                self._voltage_division_channel_4 = scope_voltage_division
        return self._voltage_division_channel_4

    @voltage_division_channel_4.setter
    def voltage_division_channel_4(self, value):
        self._voltage_division_channel_4 = value
        if (self.voltage_division_channel_4):
            if self.__connected:
                request = self.__command_list["voltage_division_channel_4"] + " " + str(value)
                self.instr.write(request)

    @property
    def voltage_offset_channel_1(self):
        if self.__connected:
            request = self.__command_list["voltage_offset_channel_1"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_offset = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_offset != self._voltage_offset_channel_1:
                print("Warning: current scope time range setting is", scope_voltage_offset, "rather than", self._voltage_offset_channel_1, " Setting to actual value", scope_voltage_offset)
                self._voltage_offset_channel_1 = scope_voltage_offset
        return self._voltage_offset_channel_1

    @voltage_offset_channel_1.setter
    def voltage_offset_channel_1(self, value):
        self._voltage_offset_channel_1 = value
        if self._voltage_offset_channel_1:
            if self.__connected:
                request = self.__command_list["voltage_offset_channel_1"] + " " + str(value)
                self.__instr.write(request)

    @property
    def voltage_offset_channel_2(self):
        if self.__connected:
            request = self.__command_list["voltage_offset_channel_2"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_offset = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_offset != self._voltage_offset_channel_2:
                print("Warning: current scope time range setting is", scope_voltage_offset, "rather than", self._voltage_offset_channel_2, " Setting to actual value", scope_voltage_offset)
                self._voltage_offset_channel_2 = scope_voltage_offset
        return self._voltage_offset_channel_2

    @voltage_offset_channel_2.setter
    def voltage_offset_channel_2(self, value):
        self._voltage_offset_channel_2 = value
        if self._voltage_offset_channel_2:
            if self.__connected:
                request = self.__command_list["voltage_offset_channel_2"] + " " + str(value)
                self.__instr.write(request)

    @property
    def voltage_offset_channel_3(self):
        if self.__connected:
            request = self.__command_list["voltage_offset_channel_3"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_offset = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_offset != self._voltage_offset_channel_3:
                print("Warning: current scope time range setting is", scope_voltage_offset, "rather than", self._voltage_offset_channel_3, " Setting to actual value", scope_voltage_offset)
                self._voltage_offset_channel_3 = scope_voltage_offset
        return self._voltage_offset_channel_3

    @voltage_offset_channel_3.setter
    def voltage_offset_channel_3(self, value):
        self._voltage_offset_channel_3 = value
        if self._voltage_offset_channel_3:
            if self.__connected:
                request = self.__command_list["voltage_offset_channel_3"] + " " + str(value)
                self.__instr.write(request)

    @property
    def voltage_offset_channel_4(self):
        if self.__connected:
            request = self.__command_list["voltage_offset_channel_4"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_voltage_offset = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_voltage_offset != self._voltage_offset_channel_4:
                print("Warning: current scope time range setting is", scope_voltage_offset, "rather than", self._voltage_offset_channel_4, " Setting to actual value", scope_voltage_offset)
                self._voltage_offset_channel_4 = scope_voltage_offset
        return self._voltage_offset_channel_4

    @voltage_offset_channel_4.setter
    def voltage_offset_channel_4(self, value):
        self._voltage_offset_channel_4 = value
        if self._voltage_offset_channel_4:
            if self.__connected:
                request = self.__command_list["voltage_offset_channel_4"] + " " + str(value)
                self.__instr.write(request)         

    @property
    def time_range(self):
        if self.__connected:
            request = self.__command_list["time_range"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_time_range = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
            if scope_time_range != self._time_range:
                print("Warning: current scope time range setting is", scope_time_range, "rather than", self._time_range, " Setting to actual value", scope_time_range)
                self._time_range = scope_time_range
        return self._time_range

    @time_range.setter
    def time_range(self, value):
        self._time_range = value
        if self._time_range:
            if self.__connected:
                request = self.__command_list["time_range"] + " " + str(value)
                self.__instr.write(request)


    @property
    def time_delay(self):
        if self.__connected:
            request = self.__command_list["time_delay"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
            scope_time_delay = re.search(r"[-]*\d+[.]\d+[mun][s]", scope_value).group(0)
            if scope_time_delay != self._time_delay:
                print("Warning: current scope time range setting is", scope_time_delay, "rather than", self._time_delay, " Setting to actual value", scope_time_delay)
                self._time_delay = scope_time_delay
        return self._time_delay
    
    @time_delay.setter
    def time_delay(self, value):
        self._time_delay = value
        if self._time_delay:
            if self.__connected:
                request = self.__command_list["time_delay"] + " " + str(value)
                self.__instr.write(request)

    @property
    def trigger_sweep(self):
        if self.__connected:
            request = self.__connected["trigger_sweep"] + self.__command_list["request_expresssion"]
            scope_value = self.__instr.ask(request)
            scope_trigger_sweep = re.search(r"", scope_value).group(0)
        return self._trigger_sweep

    @trigger_sweep.setter
    def trigger_sweep(self, value):
        if type(value) == TriggerSweep:
            self._trigger_sweep = value.name
        else:
            self._trigger_sweep = TriggerSweep(0)
        if self._trigger_sweep:
            if self.__connected:
                request = self.__command_list["trigger_sweep"] + " " + str(self._trigger_sweep)
                self.__instr.write(request)

    @property
    def trigger_mode(self):
        if self.__connected:
            request = self.__connected["trigger_mode"] + self.__command_list["request_expresssion"]
            scope_value = self.__instr.ask(request)
            scope_trigger_mode = re.search(r"", scope_value).group(0)
        return self._trigger_mode

    @trigger_mode.setter
    def trigger_mode(self, value):
        if type(value) == TriggerMode:
            self._trigger_mode = value.name
        else:
            self._trigger_mode = TriggerMode(0)
        if self._trigger_mode:
            if self.__connected:
                request = self.__command_list["trigger_mode"] + " " + str(self._trigger_mode)
                self.__instr.write(request)

    @property
    def acquisition_mode(self):
        i = 0

    @acquisition_mode.setter
    def acquisition_mode(self, value):
        i = 0                            



    def identify(self):
        print(self.__instr.ask(self.__command_list["identify"]))

    def clear(self):
        self.__instr.write(self.__command_list["clear"])

    def reset(self):
        self.__instr.write(self.__command_list["reset"])

    def write(self, expression):
        self.__instr.write(expression)

    def ask(self, expression):
        self.__instr.write(expression)
        return self.__instr.read()    

        

def main():
    print("hello there :)")
    ip = "192.168.137.5"
    command_file = "oscilloscope_commands_Siglent_SDS_1052DL+.json"
    scope = Scope(ip, command_file)
    scope.clear()
    scope.reset()
    scope.write("TRSE GLIT")
    scope.write("TRSE GLIT, SR, C2")
if __name__ == "__main__":
    main()