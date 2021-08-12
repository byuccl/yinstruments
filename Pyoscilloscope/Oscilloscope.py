from posixpath import dirname
import vxi11
import os
import re
import json
from enum import Enum
from Pyoscilloscope.elements.channel_element import *

# This class acts as a virtual interface to control the scope. The class holds variables that control the scope such as the volts per division, seconds per division, voltage offset, trigger settings, auto and cursor 
# measurements and the wave data of the scope. The interface class also includes functions for common button functions such as stop, run, single, auto and more. The parameters is the ip address of the device and a
# command file which contains all the commands for a specific oscilloscope. 
class Interface:
    def __init__(self, ip_address, commands_file=None, verbose=None):
        self._ip_address = ip_address
        self.verbose = verbose

        # Try to connect to the scope, if a timeout or other error occurs then print an error message.
        try:
            self.__instr = vxi11.Instrument(self._ip_address)
        except:
            print("Error: A timeout has occurred trying to connect to the scope. Please try reconnecting.")
        
        # Setup the directory where the oscilloscope commands are stored by obtaining the directory of the Oscilloscope.py file (this file) and joining the name of the oscilloscope commands directory.
        commands_directory_name = "oscilloscope_commands"
        commands_directory_path = os.path.join(os.path.dirname(__file__), commands_directory_name)

        # Check if the oscilloscope commands does not exist. If the directory does not exist then print and error and return.
        if not os.path.isdir(commands_directory_path):
            print("Error: The oscilloscope_commands directory:", commands_directory_path, "does not exist")
            print("Please check that the oscilloscope_commands directory is inside Pyoscilloscope directory")
            return

        # Check if the user inputted command file name is None, if so open the default command list otherwise open the custom command list.  
        if commands_file == None:

            # Setup the default file path by joining the oscilloscope directory with the default commands name. Check if the file does not exist, if the file does not exist then print an error message and return.
            default_commands_name = "default.json"
            commands_file_path = os.path.join(commands_directory_path, default_commands_name)
            if not os.path.isfile(commands_file_path):
                print("Error: The default commands file:", commands_file_path, "does not exist")
                print("Please check that default.json is inside the oscilloscope_commands directory")
                return
            
            # Open the command file and convert the .json command file to a dictionary object. If an error has occurred with opening the commands file or proessing the .json then print an error message and return.    
            try:    
                with open(commands_file_path) as f:
                    self.__command_list = json.load(f)
            except:
                print("Error: A failure has occurred opening the default command file at:", commands_file_path, "or loading json format")
                return        
        else:
            # Setup the custom commands file path by joining the oscilloscope directory with the commands name. Check if the file does not exist, if the file does not exist then print an error message and return.
            commands_file_path = os.path.join(commands_directory_path, commands_file)
            if not os.path.isfile(commands_file_path):
                print("Error: The custom commands file:", commands_file_path, "does not exist")
                print("Please check that,", commands_file, "is inside the oscilloscope_commands directory")
                return

            # Open the command file and convert the .json command file to a dictionary object. If an error has occurred with opening the commands file or proessing the .json then print an error message and return.        
            try:    
                with open(commands_file_path) as f:
                    self.__command_list = json.load(f)
            except:
                print("Error: A failure has occurred opening the default command file at:", commands_file_path, "or loading json format")
                return
        

        # The commands .json as multiple embedded dictionaries for example measurement = {...}. The following lines of code setup up the sub command list for different functions on the scope. 
        self.__measurement_commands = self.__command_list["measurement"]

        self.__trigger_sweep_commands = self.__command_list["trigger_sweep_type"]

        self.__trigger_mode_commands = self.__command_list["trigger_mode_type"]

        self.__acquisition_mode_commands = self.__command_list["acquire_mode_type"]

        self.__not_applicable_command = "NA"

        # The following lines of code define variables that control scope parameters which is dependent on the selected channel. Each class type contains a dictionary where the key represents the channel.
        # The input for most of these classes are the vxi11 instrument to send the command to the scope, the channel expression the scope uses for example C or CHAN, the command to interact with the parameter
        # and a request expression (usually ?) to obtain the parameter from the scope. 
        self.display = Display(self.__instr, self.__command_list["channel_expression"], self.__command_list["display"], self.__command_list["request_expression"])

        self.attenuation = Attenuation(self.__instr, self.__command_list["channel_expression"], self.__command_list["attenuation"], self.__command_list["request_expression"])

        self.voltage_range = Voltage_Range(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_range"], self.__command_list["request_expression"])

        self.voltage_division = Voltage_Division(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_division"], self.__command_list["request_expression"])

        self.voltage_offset = Voltage_Offset(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_offset"], self.__command_list["request_expression"])

        self.measure = Measure_Element(self.__instr, self.__command_list["channel_expression"], self.__command_list["voltage_offset"], self.__command_list["request_expression"])

        self.trigger_mode = Trigger_Type(self.__instr, self.__trigger_mode_commands, self.__command_list["channel_expression"], self.__command_list["trigger_mode"], self.__command_list["request_expression"])

        self.wave_preamble = Wave_Preamble(self.__instr, self.__command_list["channel_expression"], self.__command_list["wave_preamble"], self.__command_list["request_expression"])

        self.wave_form = Wave_Data(self.__instr, self.__command_list["channel_expression"], self.__command_list["wave_one_command"], self.__command_list["wave_data"], self.__command_list["request_expression"])


        # The following lines of code define variables that control scope parameters which affects all channels. Each variable contains getters and setters below to send commands to the scope and receive data.
        self._time_range = None
        self._time_delay = None
        self._time_division = None

        self._trigger_sweep = None
        self._acquisition_mode = None
        self._acquisition_complete = None

        
        
                             

    @property
    def time_range(self):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["time_range"] == self.__not_applicable_command:
            print("Error: This scope does not feature time range according to the .json commands file. No changes made to scope")
            return

        request = None
        scope_value = None
        # Ask the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message            
        try:
            request = self.__command_list["time_range"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
        except KeyError:
            print("Error: Invalid key: time_range or request_expression at time_range getter. Please check the .json file. No data received")
            return
        except:
            print("Error: A failure has occurred writing", request, "to the scope at time_range getter. Possible scope timeout. No data received")
            return

        return_value = None
        # Parse the string received from the scope and set the return value as a float. If the key is not in the command list then catch and print an error.
        # If the format of the returned string does not match the regular expression then catch the error and print a message. The regular expression has two
        # groups. The first is the numberic value and the second is the SI unit. 
        try:
            return_format = self.__command_list["time_range"] + " "
            m = re.search(rf"{return_format}([.+-E0123456789]*)([smun])", scope_value)
            # Check which SI unit is being used, multiple the numberic value and round properly
            if m.group(2) == "m":
                return_value = round(float(m.group(1)) * 1e-3, 3)
            elif m.group(2) == "u":
                return_value = round(float(m.group(1)) * 1e-6, 6)
            elif m.group(2) == "n":
                return_value = round(float(m.group(1)) * 1e-6, 9)
            else:
                return_value = float(m.group(1))
        except KeyError:
            print("Error: Invalid key: time_range at time_range getter. Please check the .json file. No data received")
            return
        except:
            print("Error: Unexpected return string from scope:", scope_value, "at time_range getter. Unable to parse and retrieve value or SI unit. No data received")
            return

        # If the return value from the scope is different from the currently stored value then print a warning message and set the returned scope value to the currently stored value. 
        if return_value != self._time_range:
            print("Warning: current scope time range setting is", return_value, "rather than", self._time_range, " Setting to actual value", return_value)
            self._time_range = return_value
        return self._time_range

    @time_range.setter
    def time_range(self, value):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["time_division"] == self.__not_applicable_command:
            print("Error: This scope does not feature time division according to the .json commands file. No changes made to scope")
            return

        self._time_range = value
        # Check to see if the time_division variable is a value other than none. If the value is not None, then write the command
        if self._time_range != None:
            # Write the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message             
            try:
                request = self.__command_list["time_range"] + " " + str(value)
                self.__instr.write(request)
            except KeyError:
                print("Error: Invalid key: time_range at time_range setter. Please check the .json file. No changes made to scope")
            except:
                print("Error: A failure has occurred writing", self.__command_list["time_range"], "to the scope at time_range setter. Possible scope timeout") 

    @property
    def time_division(self):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["time_division"] == self.__not_applicable_command:
            print("Error: This scope does not feature time division according to the .json commands file. No changes made to scope")
            return
        
        request = None
        scope_value = None
        # Ask the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message            
        try:
            request = self.__command_list["time_division"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
        except KeyError:
            print("Error: Invalid key: time_division or request_expression at time_division getter. Please check the .json file. No data received")
            return
        except:
            print("Error: A failure has occurred writing", request, "to the scope at time_division getter. Possible scope timeout. No data received")
            return        
        
        return_value = None
        # Parse the string received from the scope and set the return value as a float. If the key is not in the command list then catch and print an error.
        # If the format of the returned string does not match the regular expression then catch the error and print a message. The regular expression has two
        # groups. The first is the numberic value and the second is the SI unit. 
        try:
            return_format = self.__command_list["time_division"] + " "
            m = re.search(rf"{return_format}([.+-E0123456789]*)([smun])", scope_value)
            # Check which SI unit is being used, multiple the numberic value and round properly
            if m.group(2) == "m":
                return_value = round(float(m.group(1)) * 1e-3, 3)
            elif m.group(2) == "u":
                return_value = round(float(m.group(1)) * 1e-6, 6)
            elif m.group(2) == "n":
                return_value = round(float(m.group(1)) * 1e-6, 9)
            else:
                return_value = float(m.group(1))
        except KeyError:
            print("Error: Invalid key: time_division at time_division getter. Please check the .json file. No data received")
            return
        except:
            print("Error: Unexpected return string from scope:", scope_value, "at time_division getter. Unable to parse and retrieve value or SI unit. No data received")
            return

        # If the return value from the scope is different from the currently stored value then print a warning message and set the returned scope value to the currently stored value. 
        if return_value != self._time_division:
            print("Warning: current scope time division setting is", return_value, "rather than", self._time_division, " Setting to actual value", return_value)
            self._time_division = return_value
        return self._time_division

    # This function is a setter for the seconds per division variable. This will check if the feature is applicable to the scope and write the command to set the seconds per division.
    @time_division.setter
    def time_division(self, value):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["time_division"] == self.__not_applicable_command:
            print("Error: This scope does not feature time division according to the .json commands file. No changes made to scope")
            return

        self._time_division = value
        # Check to see if the time_division variable is a value other than none. If the value is not None, then write the command
        if self._time_division != None:
            # Write the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message             
            try:
                request = self.__command_list["time_division"] + " " + str(value)
                self.__instr.write(request)
            except KeyError:
                print("Error: Invalid key: time_division at time_division setter. Please check the .json file. No changes made to scope")
            except:
                print("Error: A failure has occurred writing", self.__command_list["time_division"], "to the scope at time_division setter. Possible scope timeout")                
    
    @property
    def time_delay(self):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["time_delay"] == self.__not_applicable_command:
            print("Error: This scope does not feature time delay according to the .json commands file. No changes made to scope")
            return

        request = None
        scope_value = None
        # Ask the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message            
        try:
            request = self.__command_list["time_delay"] + self.__command_list["request_expression"]
            scope_value = self.__instr.ask(request)
        except KeyError:
            print("Error: Invalid key: time_delay or request_expression at time_delay getter. Please check the .json file. No data received")
            return
        except:
            print("Error: A failure has occurred writing", request, "to the scope at time_delay getter. Possible scope timeout. No data received")
            return

        return_value = None
        # Parse the string received from the scope and set the return value as a float. If the key is not in the command list then catch and print an error.
        # If the format of the returned string does not match the regular expression then catch the error and print a message. The regular expression has two
        # groups. The first is the numberic value and the second is the SI unit. 
        try:
            return_format = self.__command_list["time_delay"] + " "
            m = re.search(rf"{return_format}([.+-E0123456789]*)([smun])", scope_value)
            # Check which SI unit is being used, multiple the numberic value and round properly
            if m.group(2) == "m":
                return_value = round(float(m.group(1)) * 1e-3, 3)
            elif m.group(2) == "u":
                return_value = round(float(m.group(1)) * 1e-6, 6)
            elif m.group(2) == "n":
                return_value = round(float(m.group(1)) * 1e-6, 9)
            else:
                return_value = float(m.group(1))        
        except KeyError:
            print("Error: Invalid key: time_delay at time_delay getter. Please check the .json file. No data received")
            return
        except:
            print("Error: Unexpected return string from scope:", scope_value, "at time_delay getter. Unable to parse and retrieve value or SI unit. No data received")
            return

        #If the return value from the scope is different from the currently stored value then print a warning message and set the returned scope value to the currently stored value. 
        if return_value != self._time_delay:
            print("Warning: current scope time delay setting is", return_value, "rather than", self._time_delay, " Setting to actual value", return_value)
            self._time_delay = return_value
        return self._time_delay


    # This function is a setter for the time delay variable. This will check if the feature is applicable to the scope and write the command to set the time delay.
    @time_delay.setter
    def time_delay(self, value):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["time_delay"] == self.__not_applicable_command:
            print("Error: This scope does not feature time delay according to the .json commands file. No changes made to scope")
            return

        self._time_delay = value
        # Check to see if the time_delay variable is a value other than none. If the value is not None, then write the command
        if self._time_delay != None:
            try:
                request = self.__command_list["time_delay"] + " " + str(value)
                self.__instr.write(request)
            except KeyError:
                print("Error: Invalid key: time_delay at time_delay setter. Please check the .json file. No changes made to scope")
            except:
                print("Error: A failure has occurred writing", self.__command_list["time_delay"], "to the scope at time_delay setter. Possible scope timeout")                            
    
    @property
    def trigger_sweep(self):
        request = self.__command_list["trigger_sweep"] + self.__command_list["request_expresssion"]
        scope_value = self.__instr.ask(request)
        return self._trigger_sweep


    @trigger_sweep.setter
    def trigger_sweep(self, value):
        self._trigger_sweep = value
        if self._trigger_sweep != None:
            request = self.__command_list["trigger_sweep"] + " " + self.__trigger_sweep_commands[value]
            self.__instr.write(request)


    @property
    def acquisition_mode(self):
        i = 0

    @acquisition_mode.setter
    def acquisition_mode(self, value):
        self._acquisition_mode = value
        if self.acquisition_mode != None:
            request = self.__command_list["acquire_mode"] + " " + self.__acquisition_mode_commands[value]
            self.__instr.write(request)

    @property
    def acquisition_complete(self):
        i = 0

    @acquisition_complete.setter
    def acquisition_complete(self, value):
        self._acquisition_complete = value
        if self.acquisition_complete != None:
            request = self.__command_list["acquire_complete"] + " " + str(value)
            self.__instr.write(request)                                    


    # This function will return the identification such as oscilloscope model received from the oscilloscope. It is good to use to identify the scope is connected properly
    def identify(self):
         # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["identify"] == self.__not_applicable_command:
            print("Error: This scope does not feature identify according to the .json commands file. No changes made to scope")
            return
        # Write the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message            
        try:    
            return self.__instr.ask(self.__command_list["identify"])
        except KeyError:
            print("Error: Invalid key: identify at identify(). Please check the .json file. No changes made to scope")
        except:
            print("Error: A failure has occurred writing", self.__command_list["identify"], "to the scope at identify(). Possible scope timeout")    



    # This function will clear different registers within the oscilloscope such as a status register and error register. It is good to run on a first use or after running into a problem
    def clear(self):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["clear"] == self.__not_applicable_command:
            print("Error: This scope does not feature clear according to the .json commands file. No changes made to scope")
            return
        # Write the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message        
        try:    
            self.__instr.write(self.__command_list["clear"])
        except KeyError:
            print("Error: Invalid key: clear at clear(). Please check the .json file. No changes made to scope")
        except:
            print("Error: A failure has occurred writing", self.__command_list["clear"], "to the scope at clear(). Possible scope timeout")    


    # This function will reset multiple variables to a default state such as volt per division and volt offset on all channels, second per division and trigger settings.  
    def reset(self):
         # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["reset"] == self.__not_applicable_command:
            print("Error: This scope does not feature reset according to the .json commands file. No changes made to scope")
            return
        # Write the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message    
        try:    
            self.__instr.write(self.__command_list["reset"])
        except KeyError:
            print("Error: Invalid key: reset at reset(). Please check the .json file. No changes made to scope")
        except:        
            print("Error: A failure has occurred writing", self.__command_list["reset"], "to the scope at reset(). Possible scope timeout")    


    # This function will run the auto setup for all signals (This is the same as pressing the AUTO button).
    def auto_setup(self):
        # Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["auto_setup"] == self.__not_applicable_command:
            print("Error: This scope does not feature auto_setup according to the .json commands file. No changes made to scope")
            return
        # Write the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message
        try:
            self.__instr.write(self.__command_list["auto_setup"])
        except KeyError:
            print("Error: Invalid key: auto_setup at auto_setup(). Please check the .json file. No changes made to scope")    
        except:
            print("Error: A failure has occurred writing", self.__command_list["auto_setup"], "to the scope at auto_setup(). Possible scope timeout")    
    
    # This function will force the trigger to be activated regardless of the trigger status or criteria.  
    def force_trigger(self):
        #Check if the scope supports the command, if the command is not supported then print an error message and return
        if self.__command_list["force_trigger"] == self.__not_applicable_command:
            print("Error: This scope does not feature force_trigger according to the .json commands file. No changes made to scope")
            return
        # Write the command to the scope, if the key is not in the command list catch and print the error. If a timeout occurs or some other error catch and print a message    
        try:    
            self.__instr.write(self.__command_list["force_trigger"])
        except KeyError:
            print("Error: Invalid key: force_trigger at force_trigger(). Please check the .json file. No changes made to scope")
        except:
            print("Error: A failure has occurred writing", self.__command_list["auto_setup"], "to the scope at force_trigger(). Possible scope timeout")    


    def display_measurement(self, channel, measurement_type):
        command_format = self.__command_list["measure_display"] + " " + self.__measurement_commands[measurement_type] + ", " + self.__command_list["channel_expression"] + str(channel)
        self.__instr.write(command_format)

    # This function allows the user to send commands directly to the oscilloscope in case a command is not implemented in this class
    def write(self, expression):
        # Write the expression to the scope, if a timeout or other issue occurs catch and print an error message
        try:
            self.__instr.write(expression)
        except:    
            print("Error: A failure has occurred writing", expression, "to the scope at write(). Possible scope timeout")    

    # This function allows the user to send a command and then read data coming from the scope, usually used with query commands. 
    def ask(self, expression):
        # Write the expression to the scope and return the read value, if a timeout or other issue occurs catch and print an error message    
        try:
            return self.__instr.ask(expression)
        except:
            print("Error: A failure has occurred asking", expression, "to the scope at ask(). Possible scope timeout")

    # This function allows the user to reconnect to the scope if necessary
    def connect(self):
        # Try to connect to the scope, if a timeout or other error occurs then print an error message and return.
        try:
            self.__instr = vxi11.Instrument(self._ip_address)
        except:
            print("Error: A timeout has occurred trying to connect to the scope. Please try reconnecting.")
            return


        