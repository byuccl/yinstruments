import vxi11
import re
import json
from enum import Enum
from Pyoscilloscope.elements.channel_element import *


class TriggerSweep(Enum):
    NORM = 0
    AUTO = 1
    SINGLE = 2
    STOP = 3

class TriggerMode(Enum):
    EDGE = 0
    GLIT = 1
    SLEW = 2
    TV = 3
                           
class AcquisitionMode(Enum):
    SAMPLING = 0
    PDE = 1
    AVERAGE = 2
    HIGH_RES = 3


class Interface:
    def __init__(self, ip_address, commands_file=None):
        self._ip_address = ip_address
        
        self.__instr = vxi11.Instrument(self._ip_address)

        if commands_file == None:
            with open("oscilloscope_commands_default.json") as f:
                self.__command_list = json.load(f)
        else:
            with open(commands_file) as f:
                self.__command_list = json.load(f)
        
        self.__measurement_commands = self.__command_list["measurement"]

        self.display = Display(self.__instr, self.__command_list["channel_expression"], self.__command_list["display"], self.__command_list["request_expression"])

        self.attenuation = Attenuation(self.__instr, self.__command_list["channel_expression"], self.__command_list["attenuation"], self.__command_list["request_expression"])

        self.voltage_range = Voltage_Range(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_range"], self.__command_list["request_expression"])

        self.voltage_division = Voltage_Division(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_division"], self.__command_list["request_expression"])

        self.voltage_offset = Voltage_Offset(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_offset"], self.__command_list["request_expression"])

        self.measure = Measure_Element(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_offset"], self.__command_list["request_expression"])

        self._time_range = None
        self._time_delay = None
        self._time_division = None

        self._trigger_sweep = None

        self._acquisition_mode = None
                             

    @property
    def time_range(self):
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
            request = self.__command_list["time_range"] + " " + str(value)
            self.__instr.write(request)


    @property
    def time_delay(self):
        request = self.__command_list["time_delay"] + self.__command_list["request_expression"]
        scope_value = self.__instr.ask(request)
        scope_time_delay = re.search(r"[-]*\d+[.]\d+[mun][s]", scope_value).group(0)
        if scope_time_delay != self._time_delay:
            print("Warning: current scope time range setting is", scope_time_delay, "rather than", self._time_delay, " Setting to actual value", scope_time_delay)
            self._time_delay = scope_time_delay
        return self._time_delay

    @property
    def time_division(self):
        request = self.__command_list["time_division"] + self.__command_list["request_expression"]
        scope_value = self.__instr.ask(request)
        scope_time_division = float(re.search(r"\d[.]\d+E[+-]\d+", scope_value).group(0))
        if scope_time_division != self._time_division:
            print("Warning: current scope time range setting is", scope_time_division, "rather than", self._time_division, " Setting to actual value", scope_time_division)
            self._time_division = scope_time_division
        return self._time_division

    @time_division.setter
    def time_division(self, value):
        self._time_division = value
        if self._time_division:
            request = self.__command_list["time_division"] + " " + str(value)
            self.__instr.write(request)    
    
    @time_delay.setter
    def time_delay(self, value):
        self._time_delay = value
        if self._time_delay != None:
            request = self.__command_list["time_delay"] + " " + str(value)
            self.__instr.write(request)

    @property
    def trigger_sweep(self):
        request = self.__command_list["trigger_sweep"] + self.__command_list["request_expresssion"]
        scope_value = self.__instr.ask(request)
        return self._trigger_sweep

    @trigger_sweep.setter
    def trigger_sweep(self, value):
        if type(value) == TriggerSweep:
            self._trigger_sweep = value.name
        else:
            self._trigger_sweep = TriggerSweep(0)
        if self._trigger_sweep != None:
            request = self.__command_list["trigger_sweep"] + " " + str(self._trigger_sweep)
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

    def auto_setup(self):
        self.__instr(self.__command_list["auto_setup"])

    def force_trigger(self):
        self.__instr(self.__command_list["force_trigger"])

    def set_trigger(self, source, trigger_type):
        command_format = self.__command_list["trigger_select"] + " " + trigger_type.name + ", " + "SR, " + self.__command_list["channel_expression"] + str(source)
        print(command_format)
        self.__instr.write(command_format)

    def get_measurement(self, channel, measurement_type):
        return self.__instr.ask("C1:PAVA? DUTY")

    def display_measurement(self, channel, measurement_type):
        command_format = self.__command_list["measure_display"] + " " + self.__measurement_commands[measurement_type] + ", " + self.__command_list["channel_expression"] + str(channel)
        self.__instr.write(command_format)

    def write(self, expression):
        self.__instr.write(expression)

    def ask(self, expression):
        self.__instr.write(expression)
        return self.__instr.read()    

        