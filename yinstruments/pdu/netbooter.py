""" This file contians the Netbooter class which inherits
from the PDU class.

"""

import telnetlib
import time
import re
from .pdu import PDU


class Netbooter(PDU):
    """This is the Netbooter class

    List of commands available to the Netbooter

    >help
    ip          Sets static IP addr. "ip xx.xx.xx.xx"
    gw          Sets Static gateway IP.
    mask        Sets Static network mask.
    dhcp   v    Sets IP in static or DHCP mode. "off"-Static. "on"-DHCP.
    emailsend   Sends a test mail.
    hp          Sets HTTP port #.
    tp          Sets TELNET port #.
    help or ?   Displays Help menu.
    login       Enters user login.
    logout      Exits current login.
    mac         Displays Ethernet port Mac address.
    nwset       Restarts Ethernet network interface.
    nwshow      Displays network Status.
    lc          Turns an outlet ON/OFF with loop control. See Help in web.
    ping        Pings a host. E.g.: ping 192.168.0.1, or ping yahoo.com.
    pset n v    Sets outlet #n to v(value 1-on,0-off).
    gpset n v   Sets outlet group #n to v(value 1-on,0-off).
    ps v        Sets all power outlets to v(value 1-on,0-off).
    pshow       Displays outlet status.
    reset       Reloads default settings.
    rb n        Reboots outlet #n.
    grb n       Reboots outlet group #n.
    sysshow     Displays system information.
    time        Displays current time.
    ver         Displays hardware and software versions.
    web v       Turns Web access ON/OFF. "1"=ON. "0"-OFF.

    """

    DEFAULT_NETBOOTER_PORT = 23
    DEFAULT_TIMEOUT_TIME = 3.0  # 3 seconds
    DEFAULT_NETBOOTER_DELAY = 0.5  # 500 ms

    def __init__(
        self,
        ip_address,
        port=DEFAULT_NETBOOTER_PORT,
        timeout=PDU.DEFAULT_TIMEOUT_TIME,
        command_delay=DEFAULT_NETBOOTER_DELAY,
    ):
        """Netbooter constructor.
        ip_address: IP address of the netbooter
        port: the TCP port used for the telnet session."""
        super().__init__(ip_address, port, timeout, command_delay)
        self.telnet = None

    def __str__(self):
        return f"{self.ip_address}:{self.port}"

    def create_telnet_session(self):
        """Creates a telnet session to the Netbooter."""
        self.telnet = telnetlib.Telnet(self.ip_address, self.port, timeout=self.timeout)
        return self.telnet

    def close_telnet_session(self):
        """Close Netbooter telnet session."""
        if self.telnet is not None:
            self.telnet.close()

    def read_some(self):
        """Read from the Netbooter."""
        if self.telnet is None:
            return None
        string = self.telnet.read_some()
        # Short time needed before next command
        time.sleep(self.sleep_time)
        return string

    def write(self, command):
        """Write data to the Netbooter."""
        if self.telnet is None:
            return
        self.telnet.write(command)
        # Short time needed before next command
        time.sleep(self.sleep_time)

    def encode_command(self, cmd: str):
        return cmd.encode("ascii") + b"\r\n\r\n"

    def encode_request(self, req: str):
        return req.encode("ascii") + b"\r\n"

    def send_command(self, cmd: str):
        """Send an aribitray command to the Netbooter."""
        self.create_telnet_session()
        string = self.read_some()
        string = self.encode_command(cmd)
        self.write(string)
        self.close_telnet_session()

    def request_response(self, req: str):
        """Send a request for a response from the Netbooter. Returns an array of strings.
        The initial and ending prompt are removed. In addition, the response is split into
        strings based on line termination."""
        self.create_telnet_session()
        string = self.read_some()
        string = self.encode_request(req)
        # Send request
        self.write(string)
        string = ""
        while True:
            text = self.telnet.read_eager()
            string += text.decode()
            if len(text) == 0:
                break
        self.close_telnet_session()
        # Remove the initial prompt "\r\n>" from string
        string = string[3:]
        # Remove the command and the following "\n\r" from teh string
        chars_to_remove = len(req) + 2
        string = string[chars_to_remove:]
        # Remove the ending prompt "\r\n>" from string
        string = string[:-3]
        # Split response into strings.
        strings = string.split("\n\r")
        return strings

    def reboot(self, port_num):
        """Issue 'reboot' command to a Netbooter port."""
        self.send_command("rb " + str(port_num))

    def on(self, port_num):
        """Turn on a Netbooter port."""
        self.send_command("pset " + str(port_num) + " 1")

    def off(self, port_num):
        """Turn off a Netbooter port."""
        self.send_command("pset " + str(port_num) + " 0")

    def get_status(self):
        """Executes the status command and resturns the string output."""
        return self.request_response("pshow")

    def get_port_status(self):
        """Returns a dictionary between the port number (int) and a boolean (True=ON, False = Off)"""
        status_str = self.get_status()
        status = {}
        for port_status_str in status_str:
            status_tuple = self._str_to_port_status(port_status_str)
            if status_tuple is not None:
                status[status_tuple[0]] = status_tuple[1]
        return status

    def _str_to_port_status(self, status_str):
        """Parses a status string and returns the tuple (port:int,status:Boolean)
        Returns None if the string doesn't match"""
        # Example String
        #    1 |     ZCU102 |   ON |
        status_re = r"\s+(\d+)\s+\|.+\|\s+(\w+).+"
        match = re.match(status_re, status_str)
        if match:
            port_num = int(match.group(1))
            if match.group(2) == "ON":
                value = True
            else:
                value = False
            return (port_num, value)
        return None

    def is_on(self, port_num):
        """Working?"""
        text = self.get_status()
        lines = text.splitlines()

        for line in lines:
            message = re.match(r"\d+\|\s+Outlet" + str(port_num) + r"\|\s+(\w+)\s*\|", line.strip())
            if message:
                return message.group(1) == "ON"
        return "OFF"
