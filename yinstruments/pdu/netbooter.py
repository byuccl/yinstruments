"""This file contians the Netbooter class which inherits
from the PDU class"""

import telnetlib
import time
from .pdu import PDU


class Netbooter(PDU):
    """This is the Netbooter class"""

    def __init__(self, ip_address, port, timeout=3.0):
        super().__init__(ip_address, port)

    def __str__(self):
        return f"{self.ip_address}:{self.port}"

    # reboots port on netbooter
    def reboot(self, port_num):
        telnet = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        string = telnet.read_some()
        time.sleep(self.SLEEP_TIME)

        string = ("rb " + str(port_num)).encode("ascii") + b"\r\n\r\n"
        telnet.write(string)
        time.sleep(self.SLEEP_TIME)
        telnet.close()

    # turns port_num on
    def on(self, port_num):
        telnet = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        string = telnet.read_some()
        time.sleep(self.SLEEP_TIME)

        string = ("pset " + str(port_num) + " 1").encode("ascii") + b"\r\n\r\n"
        telnet.write(string)
        time.sleep(self.SLEEP_TIME)
        telnet.close()

    # turns port_num off
    def off(self, port_num):
        telnet = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        string = telnet.read_some()

        time.sleep(self.SLEEP_TIME)

        string = ("pset " + str(port_num) + " 0").encode("ascii") + b"\r\n\r\n"
        telnet.write(string)
        time.sleep(self.SLEEP_TIME)
        telnet.close()

    def get_status(self):
        telnet = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        string = telnet.read_some()
        time.sleep(self.SLEEP_TIME)

        string = "pshow".encode("ascii") + b"\r\n"
        telnet.write(string)
        time.sleep(self.SLEEP_TIME)
        string = ""
        while True:
            text = telnet.read_eager()
            string += text.decode()
            if len(text) == 0:
                break

        telnet.close()
        # returns a organized graphic of the ports and the status of the ports
        return string

    # def is_on(self, port_num):
    #     text = self.get_status()
    #     lines = text.splitlines()

    #     for line in lines:
    #         message = re.match(
    #             r"\d+\|\s+Outlet" + str(port_num) + r"\|\s+(\w+)\s*\|", line.strip()
    #         )
    #         if message:
    #             return message.group(1) == "ON"
    #     return None
