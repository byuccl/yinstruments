import telnetlib
import time
import sys
import os
import re
import pysnmp as snmp
from abc import ABC, abstractmethod



class PDU_Port:
    # generic class structure for any PDU systems port

    def __init__(self, ip_addr, ip_port) -> None:
        return 0

    def __str__(self):
        return 0

    def reboot(self):
        return 0

    def on(self):
        return 0

    def off(self):
        return 0


class PDU:
    # generic class for PDU devices

    # initializes your PDU with callable characteristics
    def __init__(self, ip_address, port, timeout=3.0):
        self._SLEEP_TIME = 1.0
        self.timeout = timeout
        self.ip_address = ip_address
        self.port = port

    def __str__(self):
        return 0
    
    def reboot(self):
        return 0
    
    def on(self):
        return 0
    
    def off(self):
        return 0
    
    def get_status(self):
        return 0
    
class Lindy_Port(PDU_Port):
    def __init__(self, ip_addr, lindy_port, timeout = 3.0) -> None:
        pass


#try monday to use the subprocess command to implement a working Lindy_class
#command = sys.argv[1]
# port_num = sys.argv[2]
# subprocess([]) 

class Lindy(PDU):
    def __init__(self, ip_addr, port, timeout=3.0):
        #creates Lindy with characteristics of generic PDU class
        super().__init__(ip_addr, port, timeout)


class Netbooter_Port(PDU_Port):
    
    def __init__(self, ip_addr, ip_port, netbooter_port, timeout = 3.0) -> None:
        #creates a netbooter object that can be pointed to and acted upon later in code
        self.netbooter = Netbooter(ip_addr, ip_port, timeout)
        self.netbooter_port = netbooter_port

    @abstractmethod
    def __str__(self):
        #string function for Netbooter_Port class
        return f"{self.netbooter}-{self.netbooter_port}"

    @abstractmethod
    def reboot(self):
        #reboots selected port
        self.netbooter.reboot(self.netbooter_port)

    @abstractmethod
    def on(self):
        #turns on selected port
        self.netbooter.on(self.netbooter_port)

    @abstractmethod
    def off(self):
        #turns off selected port 
        self.netbooter.off(self.netbooter_port)

class Netbooter(PDU):

    def __init__(self, ip_addr, port, timeout = 3.0):
        #creates Netbooter with characteristics of generic PDU class
        super().__init__(ip_addr, port, timeout)



    @abstractmethod
    #string function for Netbooter
    def __str__(self):
        return f"{self.ip_address}:{self.port}"
    
    @abstractmethod
    #reboots port on netbooter
    def reboot(self, port_num):
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("rb " + str(port_num)).encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    @abstractmethod
    #turns port_num on
    def on(self, port_num):
        print("On:", port_num)
        tn = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)

        s = tn.read_some()
        time.sleep(self._SLEEP_TIME)

        s = ("pset " + str(port_num) + " 1").encode("ascii") + b"\r\n\r\n"
        tn.write(s)
        time.sleep(self._SLEEP_TIME)
        tn.close()

    @abstractmethod
    #turns port_num off
    def off(self, port_num):
        print("Off:", port_num)
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
            m = re.match(r"\d+\|\s+Outlet" + str(port_num) + r"\|\s+(\w+)\s*\|", l.strip())
            if m:
                return m.group(1) == "ON"
        return None

def print_usage():
    print("Incorrect usage!")
    print(os.path.splitext(__file__)[0], "<on|off|reboot|status> <port_num>")


def main():
    ip_address = "192.168.1.100"
    port = 23
    netbooter = Netbooter(ip_address, port)
    # Get command
    """if you dont give the command line the following arguments you will get an error:
        sys[0]: PDU_main.py
        sys[1]: "on" "off" or "reboot"
        sys[2]: <port_number> --note: should be an int value
        """
    if len(sys.argv) < 2:
        print_usage()
        return

    cmd = sys.argv[1].lower()
    if cmd == "status":
        print(netbooter.get_status())
        return

    if len(sys.argv) != 3:
        print_usage()
        return

    if cmd not in ("on", "off", "reboot"):
        print_usage()
        return

    port_num = sys.argv[2]

    if cmd == "on":
        netbooter.on(port_num)
    elif cmd == "off":
        netbooter.off(port_num)
    elif cmd == "reboot":
        netbooter.reboot(port_num)


if __name__ == "__main__":
    main()

    


