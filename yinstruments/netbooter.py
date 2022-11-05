import telnetlib
import time
import re


class Netbooter:
    def __init__(self, ip, port, timeout=3.0):
        self.ip = ip
        self.port = port
        self._SLEEP_TIME = 1
        self.timeout = timeout

    def port_reboot(self, port_num):
        tn = telnetlib.Telnet(self.ip, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("rb " + str(port_num)).encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    def port_on(self, port_num, do_sleep=True):
        # print("On:", port_num)
        tn = telnetlib.Telnet(self.ip, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("pset " + str(port_num) + " 1").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        if do_sleep:
            time.sleep(self._SLEEP_TIME)
        tn.close()

    def port_off(self, port_num, do_sleep=True):
        # print("Off:", port_num)
        tn = telnetlib.Telnet(self.ip, self.port, timeout=self.timeout)

        s = tn.read_some()
        # print(s)
        time.sleep(self._SLEEP_TIME)

        s = ("pset " + str(port_num) + " 0").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        if do_sleep:
            time.sleep(self._SLEEP_TIME)
        tn.close()

    def get_status(self, do_sleep=True):
        tn = telnetlib.Telnet(self.ip, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = "pshow".encode("ascii") + b"\r\n"
        tn.write(s)
        if do_sleep:
            time.sleep(self._SLEEP_TIME)

        s = ""
        while True:
            text = tn.read_eager()
            s += text.decode()
            if len(text) == 0:
                break

        tn.close()

        return s

    def is_port_on(self, port_num):
        text = self.get_status()
        lines = text.splitlines()

        for l in lines:
            m = re.match(r"\d+\|\s+Outlet" + str(port_num) + r"\|\s+(\w+)\s*\|", l.strip())
            if m:
                return m.group(1) == "ON"
        return None
