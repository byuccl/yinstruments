from enum import Enum
import re
import vxi11


# This class serves as a method to set and get a dictionary object where the key of the dictionary is the channel of the scope. The input parameters are the instr to commicate with the scope, the channel format
# for example C or CHAN. The command that is associated with the oscilloscope parameter and the command_query (usually ?)
class Channel_Element:
    def __init__(self, instr, channel_format, command, command_query):
        self.__instr = instr
        self.channel_format = channel_format
        self.command = command
        self.command_query = command_query
        self.channel = {1: None, 2: None, 3: None, 4: None}

    # This function is a getter for the dictionary for a given key. It sends a command to the oscilloscope to see the current value of the wanted parameter and compares what
    # is currently stored. If the actual scope value and stored value differ then prints an warning message and sets the stored value as the actual scope value
    def __getitem__(self, key):
        # Check if the key is not included in the dictionary. If not included then print an error message and return
        if not (key in self.channel):
            print("Error: Invalid key:", key, "at channel_element getter. No data received")
            return
        scope_value = None
        command_format = self.channel_format + str(key) + self.command + self.command_query

        # Ask the command to the scope. If a timeout occurs or some other error catch and print a message
        try:
            scope_value = self.__instr.ask(command_format)
        except:
            print(
                "Error: A failure has occurred writing",
                command_format,
                "to the scope at channel_element getter. Possible scope timeout. No data received",
            )
            return

        return_value = None
        # Parse the string received from the scope and set the return value as a float. If the format of the returned string does not match the regular expression then catch the error and print a message.
        # The regular expression has a group for hte numberic value.
        try:
            return_format = self.channel_format + str(key) + self.command + " "
            m = re.search(rf"{return_format}([.+-E0123456789]*)", scope_value)
            return_value = float(m.group(1))
        except:
            print(
                "Error: Unexpected return string from scope:",
                scope_value,
                "at channel_element getter. Unable to parse and retrieve value. No data received",
            )
            return

        # If the return value from the scope is different from the currently stored value then print a warning message and set the returned scope value to the currently stored value.
        if return_value != self.channel[key]:
            print(
                "Warning:",
                self.command,
                "on channel",
                str(key),
                "is set to",
                self.channel[key],
                "but the scope is set to",
                scope_value,
                ". Changing to scope value",
            )
            self.channel[key] = scope_value

        return self.channel[key]

    # This function is a setter for the dictionary for a given key and value. A command is send to the scope when the value is set, making the stored value and scope value the same (if the value is a valid parameter to the scope)
    def __setitem__(self, key, value):
        # Check if the key is not in the dictionary if it's not then print an error message and return
        if not (key in self.channel):
            print("Error: Invalid key:", key, "at channel_element setter. No changes made to scope")
            return

        # Check if the value being set is something other than None. If so, write to the scope and set the store the value in a variable. Catch a timeout error occurs
        if value != None:
            command_format = (
                self.channel_format + str(key) + self.command + " " + str(self.channel[key])
            )
            try:
                self.__instr.write(command_format)
                self.channel[key] = value
            except:
                print(
                    "Error: A failure has occurred writing",
                    self.command,
                    "to the scope at channel_element setter. Possible scope timeout",
                )


# These classes follow the same format as the channel_element class
class Voltage_Range(Channel_Element):
    pass


class Voltage_Division(Channel_Element):
    pass


class Voltage_Offset(Channel_Element):
    pass


class Attenuation(Channel_Element):
    pass


class Wave_Preamble(Channel_Element):
    def __init__(self, instr, channel_format, command, command_query):
        self.__instr = instr
        super().__init__(instr, channel_format, command, command_query)

    def __getitem__(self, key):
        # Check if the key is not included in the dictionary. If not included then print an error message and return
        if not (key in self.channel):
            print("Error: Invalid key:", key, "at channel_element getter. No data received")
            return
        scope_value = None
        command_format = self.channel_format + str(key) + self.command + self.command_query

        # Ask the command to the scope. If a timeout occurs or some other error catch and print a message
        try:
            self.channel[key] = self.__instr.ask(command_format)
            return self.channel[key]
        except:
            print(
                "Error: A failure has occurred writing",
                command_format,
                "to the scope at channel_element getter. Possible scope timeout. No data received",
            )
            return

    def __setitem__(self, key, value):
        print(
            "Error: Trying to set preamble at channel",
            str(key),
            "with value",
            str(value),
            "Cannot set wave premable, can only receive wave premable",
        )


# This class serves as a method to set and get a dictionary object where the key of the dictionary is the channel of the scope for the display status.
# The input parameters are the instr to commicate with the scope, the channel format for example C or CHAN. The command that is associated with the oscilloscope
# parameter and the command_query (usually ?)
class Display(Channel_Element):
    def __init__(self, instr, channel_format, command, command_query):
        self.__instr = instr
        super().__init__(instr, channel_format, command, command_query)

    # This function is a getter for the dictionary for a given key. It sends a command to the oscilloscope to see the current value of the wanted parameter and compares what
    # is currently stored. If the actual scope value and stored value differ then prints an warning message and sets the stored value as the actual scope value
    def __getitem__(self, key):
        # Check if the key is not included in the dictionary. If not included then print an error message and return
        if not (key in self.channel):
            print("Error: Invalid key:", key, "at display_element getter. No data received")
            return

        command_format = self.channel_format + str(key) + self.command + self.command_query
        # Ask the command to the scope. If a timeout occurs or some other error catch and print a message
        try:
            scope_value = self.__instr.ask(command_format)
        except:
            print(
                "Error: A failure has occurred writing",
                command_format,
                "to the scope at display_element getter. Possible scope timeout. No data received",
            )

        return_value = None
        # Search for keywords ON or OFF to determine display state and set the return value
        if str(scope_value).find("ON"):
            return_value = "ON"
        elif str(scope_value).find("OFF"):
            return_value = "OFF"
        else:
            print(
                "Error: Unexpected return value for display_element. The string does not inlclude OFF or ON"
            )

        # If the return value from the scope is different from the currently stored value then print a warning message and set the returned scope value to the currently stored value.
        if self.channel[key] != return_value:
            print(
                "Warning:",
                self.command,
                "on channel",
                str(key),
                "is set to",
                self.channel[key],
                "but the scope is set to",
                scope_value,
                ". Changing to scope value",
            )
            self.channel[key] = return_value

        return self.channel[key]

    # This function is a setter for the dictionary for a given key and value. A command is send to the scope when the value is set, making the stored value and scope value the same (if the value is a valid parameter to the scope)
    def __setitem__(self, key, value):
        # Check if the key is not included in the dictionary. If not included then print an error message and return
        if not (key in self.channel):
            print("Error: Invalid key:", key, "at display_element setter. No changes made to scope")
            return

        # Check the type of value being set (since most scopes accept ON and OFF but may not expect 1 or 0 as a parameter). Deal with int, bool and string types
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
            print(
                "Error: Unexpected input:",
                value,
                "on channel,",
                str(key),
                "at display_element setter. Setting channel,",
                str(key),
                "to ON",
            )
            self.channel[key] = "ON"

        # Check if the value being set is something other than None. If so, write to the scope and set the store the value in a variable. Catch a timeout error occurs
        if self.channel[key] != None:
            command_format = (
                self.channel_format + str(key) + self.command + " " + str(self.channel[key])
            )
            self.__instr.write(command_format)


# This class holds
class Wave_Data:
    def __init__(self, instr, channel_format, one_line_command, command, command_query):
        self.__instr = instr
        self.channel_format = channel_format
        self.command = command
        self.command_query = command_query
        self.one_line_command = one_line_command
        self.channel = {1: None, 2: None, 3: None, 4: None}

    def __getitem__(self, key):
        print("Test the wave function")
        if self.one_line_command:
            command_format = (
                self.channel_format + str(key) + self.command + self.command_query + " DAT2"
            )
            self.__instr.write(command_format)
            wave_data = self.__instr.read_raw()
            self.channel[key] = wave_data[21:]
            print("Here is the data")
            print(self.channel[key])
            while 1:
                i = 0
        return self.channel[key]

    def __setitem__(self, key, value):
        print("Error cannot set wave data, can only retrieve")


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


class Trigger_Type:
    def __init__(self, instr, trigger_command, channel_format, command, command_query):
        self.__instr = instr
        self.trigger_command = trigger_command
        self.channel_format = channel_format
        self.command = command
        self.command_query = command_query
        self.channel = {1: None, 2: None, 3: None, 4: None, "EX": None}

    def __getitem__(self, key):
        return self.channel[key]

    def __setitem__(self, key, value):
        self.channel = self.channel.fromkeys(self.channel, None)
        self.channel[key] = value
        if self.channel[key]:
            if type(key) == int:
                if self.trigger_command["one_command_mode"]:
                    command_format = (
                        self.command
                        + " "
                        + self.trigger_command[value]
                        + ", "
                        + self.trigger_command["source"]
                        + ", "
                        + self.channel_format
                        + str(key)
                    )
                else:
                    command_format = (
                        self.channel_format + str(key) + self.command + " " + str(self.channel[key])
                    )
            else:
                if self.trigger_command["one_command_mode"]:
                    command_format = (
                        self.command
                        + " "
                        + self.trigger_command[value]
                        + ", "
                        + self.trigger_command["source"]
                        + ", "
                        + key
                    )
                else:
                    command_format = (
                        self.channel_format + str(key) + self.command + " " + str(self.channel[key])
                    )
            self.__instr.write(command_format)
