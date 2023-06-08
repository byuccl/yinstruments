from pdu import PDU
import telnetlib
import re
import time


class Netbooter(PDU):

    # reboots port on netbooter
    def reboot(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("rb " + str(port_num)).encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    # turns port_num on
    def on(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("pset " + str(port_num) + " 1").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    # turns port_num off
    def off(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()

        time.sleep(self._SLEEP_TIME)

        s = ("pset " + str(port_num) + " 0").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

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
        # returns a organized graphic of the ports and the status of the ports
        return s

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
