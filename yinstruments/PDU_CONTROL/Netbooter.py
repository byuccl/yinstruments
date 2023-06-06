from abc import abstractmethod
from PDU import PDU
import telnetlib
import re
import time


class Netbooter(PDU):
    def __init__(self, ip_addr, port, timeout=3.0):
        # creates Netbooter with characteristics of generic PDU class
        super().__init__(ip_addr, port, timeout)

    @abstractmethod
    # string function for Netbooter
    def __str__(self):
        return f"{self.ip_address}:{self.port}"

    @abstractmethod
    # reboots port on netbooter
    def reboot(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("rb " + str(port_num)).encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    @abstractmethod
    # turns port_num on
    def on(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("pset " + str(port_num) + " 1").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    @abstractmethod
    # turns port_num off
    def off(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()

        time.sleep(self._SLEEP_TIME)

        s = ("pset " + str(port_num) + " 0").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    @abstractmethod
    def get_status(self):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = "pshow".encode("ascii") + b"\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)

        s = ""
        while True:
            text = tn.read_eager()
            s += text.decode()
            if len(text) == 0:
                break

        tn.close()

        return s

    @abstractmethod
    def is_on(self, port_num):
        text = self.get_status()
        lines = text.splitlines()

        for l in lines:
            m = re.match(
                r"\d+\|\s+Outlet" + str(port_num) + r"\|\s+(\w+)\s*\|", l.strip()
            )
            if m:
                return m.group(1) == "ON"
        return None
