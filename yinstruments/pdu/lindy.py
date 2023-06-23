"""This file contains the Lindy class which inherits from the 
PDU class"""

import subprocess
from .pdu import PDU

# standard OID for the functions we will be doing
OID = "iso.3.6.1.4.1.17420.1.2.9.1.13.0"


class Lindy(PDU):
    """This is the Lindy class"""

    def __init__(self, ip_address, port, timeout=3.0):
        super().__init__(ip_address, port)

    def __str__(self):
        return f"{self.ip_address}:{self.port}"

    def on(self, port_num):
        if int(port_num) > 8:  # Since we are working with the LindyIPowerClassic8,
            # we don't want to accept a larger integer than 8
            raise Exception("ERROR: port_num given out of range")

        status_list = self.get_status().split(",")

        for i in range(
            1, len(status_list) + 1
        ):  # search the newly formed list for the index of the port num
            if i == int(port_num):
                status_list[i - 1] = "1"

        status_string = ",".join(
            status_list
        )  # joins list back together as string to be ready to use in command
        command = [
            "snmpset",
            "-v1",
            "-c",
            "public",
            f"{self.ip_address}",
            f"{OID}",
            "s",
            status_string,
        ]

        # execute the command
        subprocess.check_output(command)

        # print that the port_num is now on
        # print("On:", port_num)

    def off(self, port_num):
        if int(port_num) > 8:  # Since we are working with the LindyIPowerClassic8,
            # we don't want to accept a larger integer than 8
            raise Exception("ERROR: port_num given out of range")

        status_list = self.get_status().split(",")

        for i in range(
            1, len(status_list) + 1
        ):  # search the newly formed list for the index of the port num
            if i == int(port_num):
                status_list[i - 1] = "0"

        status_string = ",".join(
            status_list
        )  # joins list back together as string to be ready to use in command
        command = [
            "snmpset",
            "-v1",
            "-c",
            "public",
            f"{self.ip_address}",
            f"{OID}",
            "s",
            status_string,
        ]

        # execute the command
        subprocess.check_output(command)

    def reboot(self, port_num):
        self.off(port_num)
        self.on(port_num)

    def get_status(self):
        # command that is going to be executed
        command = [
            "snmpwalk",
            "-v1",
            "-c",
            "public",
            f"{self.ip_address}",
            f"{OID}",
        ]
        # Run the command and capture the output
        output = subprocess.check_output(command)
        # return output
        string = output.decode()[43:60]
        # return string is a string of comma separated 1's and 0's.
        return string[1:16]

    def is_on(self, port_num):
        if int(port_num) > 8:  # Since we are working with the LindyIPowerClassic8,
            # we don't want to accept a larger integer than 8
            raise Exception("ERROR: port_num given out of range")

        status_list = self.get_status().split(",")
        if status_list[int(port_num) - 1] == "1":
            return "ON"
        return "OFF"
