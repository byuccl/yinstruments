import vxi11


class PowerSupply:
    SLEW_MAX = "MAX"
    SLEW_MIN = "MIN"

    # GET_MEAS = "MEAS:{measurement}? (@{channel})"
    # MAX_TRIES = 10

    def __init__(self, ip_address):
        self.instr = vxi11.Instrument(ip_address)
        self.instr.open()

        self.model_name = self.get_power_supply_model_name()
        if self.model_name == "E36313A":
            self.num_channels = 3
            self.num_digital_io_channels = 3
            self.supports_slew = False
        elif self.model_name == "E36231A":
            self.num_channels = 1
            self.num_digital_io_channels = 3
            self.supports_slew = True
        elif self.model_name in ("N6705B", "N6705C"):
            self.num_channels = 4
            self.num_digital_io_channels = 0  # Haven't checked if these have digital I/O.
            self.supports_slew = True
        else:
            raise NotImplementedError("Unknown power supply model", self.model_name)

        self.volt_min = 0
        self.volt_max = 20.0

        # from an abstraction standpoint, should these be here? Not sure.
        # self.GET_VOLT = self.GET_MEAS.format(
        #     measurement="VOLT", channel=self.channel
        # )  # we need to change the self.channel to be able to get it to loop through all the channels
        # self.GET_CURR = self.GET_MEAS.format(measurement="CURR", channel=self.channel)
        # self.MEASUREMENTS = (self.GET_VOLT, self.GET_CURR)

    def enable_channel(self, channel_idx):
        if self.validate_channel(channel_idx):
            self.instr.write("OUTP ON, (@" + str(channel_idx) + ")")

    def disable_channel(self, channel_idx):
        if self.validate_channel(channel_idx):
            self.instr.write("OUTP OFF, (@" + str(channel_idx) + ")")

    def set_channel_voltage(self, channel_idx, voltage):
        if self.validate_channel(channel_idx) and self.validate_voltage(voltage):
            self.instr.write("VOLT " + str(voltage) + ", (@" + str(channel_idx) + ")")

    def get_channel_voltage(self, channel_idx):
        if self.validate_channel(channel_idx):
            return float(self.instr.ask("MEAS:VOLT? (@" + str(channel_idx) + ")"))
        return 0

    def get_channel_current(self, channel_idx):
        if self.validate_channel(channel_idx):
            return float(self.instr.ask("MEAS:CURR? (@" + str(channel_idx) + ")"))
        return 0

    def set_channel_current(self, channel_idx, current):
        if self.validate_channel(channel_idx) and self.validate_voltage(current):
            self.instr.write("CURR " + str(current) + ", (@" + str(channel_idx) + ")")

    def validate_channel(self, channel_idx):
        if not (1 <= channel_idx <= self.num_channels):
            print("Invalid channel. Must be between 1 and", self.num_channels)
            return False
        return True

    def validate_voltage(self, voltage):
        if not (self.volt_min <= voltage <= self.volt_max):
            print("Invalid voltage. Must be between", self.volt_min, "and", self.volt_max)
            return False
        return True

    def validate_slew_rate(self, slew_rate) -> bool:
        """Validate slew_rate. Accepts 'MAX', 'MIN', 'INF' strings or positive numeric values (0 < slew_rate <= 100,000)."""
        if isinstance(slew_rate, str):
            if slew_rate.upper() in ("MAX", "MIN", "INF"):
                return True
            try:
                slew_rate = float(slew_rate)
            except ValueError:
                print(f"Invalid slew rate string: {slew_rate}")
                return False

        if isinstance(slew_rate, (int, float)):
            if slew_rate < 0.002:
                print(
                    f"Slew rate {slew_rate} V/s is below minimum value (0.002). Use PowerSupply.SLEW_MIN for slowest rate."
                )
                return False
            if slew_rate > 100000:
                print(
                    f"Slew rate {slew_rate} V/s exceeds maximum numerical limit (100,000). Use PowerSupply.SLEW_MAX for fastest rate."
                )
                return False
            return True

        print(f"Invalid slew rate type: {type(slew_rate)}")
        return False

    # --- Digital I/O (E36313A and E36231A only) ---

    def validate_dio_pin(self, pin: int) -> bool:
        if not (1 <= pin <= self.num_digital_io_channels):
            print("Invalid DIO pin. Must be between 1 and", self.num_digital_io_channels)
            return False
        return True

    def configure_dio_input(self, pin: int) -> None:
        """Configure a digital I/O pin as an input with positive polarity."""
        if self.validate_dio_pin(pin):
            self.instr.write("DIG:PIN" + str(pin) + ":FUNC DINP")
            self.instr.write("DIG:PIN" + str(pin) + ":POL POS")

    def configure_dio_output(self, pin: int) -> None:
        """Configure a digital I/O pin as an output with positive polarity."""
        if self.validate_dio_pin(pin):
            self.instr.write("DIG:PIN" + str(pin) + ":FUNC DIO")
            self.instr.write("DIG:PIN" + str(pin) + ":POL POS")

    def read_dio_pin(self, pin) -> bool:
        """Read the state of a digital input pin. Returns True or False."""
        if self.validate_dio_pin(pin):
            data = int(self.instr.ask("DIG:INP:DATA?"))
            return bool((data >> (pin - 1)) & 1)
        return False

    def write_dio_pin(self, pin: int, value: bool) -> None:
        """Set the state of a digital output pin to 1 or 0."""
        if self.validate_dio_pin(pin):
            current = int(self.instr.ask("DIG:OUTP:DATA?"))
            if value:
                current |= 1 << (pin - 1)
            else:
                current &= ~(1 << (pin - 1))
            self.instr.write("DIG:OUTP:DATA " + str(current))

    def __del__(self):
        """This function calls the close function, which closes communication and connection with the power supply."""
        self.instr.close()

    def get_power_supply_model_name(self):
        return self.instr.ask("*IDN?").split(",")[1]

    # --- Slew Rate Control ---

    def set_channel_voltage_slew_rate(self, channel_idx, slew_rate):
        """Set the voltage slew rate in V/s for both rising and falling transitions."""
        if not self.supports_slew:
            raise NotImplementedError(
                f"Voltage slew rate control is not supported on model {self.model_name}"
            )
        if self.validate_channel(channel_idx) and self.validate_slew_rate(slew_rate):
            if self.model_name == "E36231A":
                self.instr.write(f"VOLT:SLEW:RIS {slew_rate}, (@{channel_idx})")
                self.instr.write(f"VOLT:SLEW:FALL {slew_rate}, (@{channel_idx})")
            elif self.model_name in ("N6705B", "N6705C"):
                self.instr.write(f"VOLT:SLEW {slew_rate}, (@{channel_idx})")

    def set_channel_voltage_slew_rising(self, channel_idx, slew_rate):
        """Set rising voltage slew rate in V/s."""
        if not self.supports_slew:
            raise NotImplementedError(
                f"Voltage slew rate control is not supported on model {self.model_name}"
            )
        if self.validate_channel(channel_idx) and self.validate_slew_rate(slew_rate):
            if self.model_name == "E36231A":
                self.instr.write(f"VOLT:SLEW:RIS {slew_rate}, (@{channel_idx})")
            elif self.model_name in ("N6705B", "N6705C"):
                self.instr.write(f"VOLT:SLEW {slew_rate}, (@{channel_idx})")

    def set_channel_voltage_slew_falling(self, channel_idx, slew_rate):
        """Set falling voltage slew rate in V/s."""
        if not self.supports_slew:
            raise NotImplementedError(
                f"Voltage slew rate control is not supported on model {self.model_name}"
            )
        if self.validate_channel(channel_idx) and self.validate_slew_rate(slew_rate):
            if self.model_name == "E36231A":
                self.instr.write(f"VOLT:SLEW:FALL {slew_rate}, (@{channel_idx})")
            elif self.model_name in ("N6705B", "N6705C"):
                self.instr.write(f"VOLT:SLEW {slew_rate}, (@{channel_idx})")

    def get_channel_voltage_slew_rising(self, channel_idx) -> float:
        """Get rising voltage slew rate in V/s."""
        if not self.supports_slew:
            raise NotImplementedError(
                f"Voltage slew rate control is not supported on model {self.model_name}"
            )
        if self.validate_channel(channel_idx):
            if self.model_name == "E36231A":
                return float(self.instr.ask(f"VOLT:SLEW:RIS? (@{channel_idx})"))
            elif self.model_name in ("N6705B", "N6705C"):
                return float(self.instr.ask(f"VOLT:SLEW? (@{channel_idx})"))
        return 0.0

    def get_channel_voltage_slew_falling(self, channel_idx) -> float:
        """Get falling voltage slew rate in V/s."""
        if not self.supports_slew:
            raise NotImplementedError(
                f"Voltage slew rate control is not supported on model {self.model_name}"
            )
        if self.validate_channel(channel_idx):
            if self.model_name == "E36231A":
                return float(self.instr.ask(f"VOLT:SLEW:FALL? (@{channel_idx})"))
            elif self.model_name in ("N6705B", "N6705C"):
                return float(self.instr.ask(f"VOLT:SLEW? (@{channel_idx})"))
        return 0.0

    def get_channel_voltage_slew_rate(self, channel_idx) -> tuple[float, float]:
        """Get voltage slew rate in V/s as a tuple of (rising, falling)."""
        return (
            self.get_channel_voltage_slew_rising(channel_idx),
            self.get_channel_voltage_slew_falling(channel_idx),
        )

    def set_channel_current_slew_rate(self, channel_idx, slew_rate):
        """Set current slew rate in A/s (N6705B/C only)."""
        if self.model_name not in ("N6705B", "N6705C"):
            raise NotImplementedError(
                f"Current slew rate control is not supported on model {self.model_name}"
            )
        if self.validate_channel(channel_idx) and self.validate_slew_rate(slew_rate):
            self.instr.write(f"CURR:SLEW {slew_rate}, (@{channel_idx})")

    def get_channel_current_slew_rate(self, channel_idx) -> float:
        """Get current slew rate in A/s (N6705B/C only)."""
        if self.model_name not in ("N6705B", "N6705C"):
            raise NotImplementedError(
                f"Current slew rate control is not supported on model {self.model_name}"
            )
        if self.validate_channel(channel_idx):
            return float(self.instr.ask(f"CURR:SLEW? (@{channel_idx})"))
        return 0.0

    # def get_measurement_float(
    #     self,
    # ):  # fix data so it reads as a list? or change channels to be in power_supply_server
    #     """This function gets measurement data from our power supply using get.measurement, and then proceeds to parse and alter the
    #     data to put in our database later on. We check to see if one data entry was tallied or multiple by checking the type of the data,
    #     and then we proceed to reclassify the strings to floats and reorder the lists to pair each voltage and current together for a given
    #     channel. We then return the list of all of the channels' voltage and current readings.

    #     Arguments:
    #         None
    #     Variables:
    #         data_list {list-tuple-float} -- The list holing the voltage and current data for all of the channels
    #         data {list/string} -- If multiple data values, this will be a list of strings containg voltage readings and
    #             current readings for the channels. If one value, it will be a string with the given numerical data reading.
    #         paired_measurements {list-str} -- A list holding the voltage and current of a given channel in a list.
    #         datapoint {tuple-float} -- A tuple containing the float number measurements of voltage and current.
    #     Returns:
    #         datapoint if we are querying multiple datapoints or multiple channels, data if its one measurement for one channel.
    #     """

    #     data_list = []
    #     # print("Taking Measurement for ", self.hostname)
    #     data = self.ask_command(self.MEASUREMENTS)
    #     # print(data)
    #     if type(data) is list:
    #         if self.check_power_supply_type("E36231A") != -1:
    #             data = tuple(map(float, data))
    #             data_list.append(data)
    #         # print(data[0])
    #         # print(type(data[0]))
    #         if type(data[0]) is str:  # new
    #             voltage = data[0].split(",")  # new
    #             current = data[1].split(",")
    #             for index in range(len(voltage)):  # new
    #                 paired_measurements = []
    #                 paired_measurements.append(voltage[index])
    #                 paired_measurements.append(current[index])
    #                 datapoint = tuple(map(float, paired_measurements))
    #                 data_list.append(datapoint)
    #     elif type(data) is str:
    #         # print("Its a string.")
    #         data = float(data)
    #         return data
    #     else:
    #         logging.error(
    #             "Data is not a list or a str. Type: {} Value: {}".format(type(data), data)
    #         )
    #         raise Exception(
    #             "Data is not a list or a str. Type: {} Value: {}".format(type(data), data)
    #         )

    #     # print("Data List: ", data_list)
    #     # print("Type: ", type(data_list))
    #     return data_list


if __name__ == "__main__":
    ip = "192.168.0.100"
    instr = PowerSupply(ip)

    instr.disable_channel(1)
    # instr.enable_channel(1)
