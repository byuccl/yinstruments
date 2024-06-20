"""This file contains the top level PDU class"""

from abc import abstractmethod
from enum import Enum


class PDUType(Enum):
    Netbooter = 1
    Lindy = 2


class PDU:
    """Generic class for PDU"""

    DEFAULT_TIMEOUT_TIME = 3.0  # 3 seconds
    DEFAULT_COMMAND_DELAY = (
        1.0  # This is the original delay that may be needed by the Lindy. It is probably excessive
    )

    # initializes your PDU with callable characteristics
    @abstractmethod
    def __init__(
        self, ip_address, port, timeout=DEFAULT_TIMEOUT_TIME, command_delay=DEFAULT_COMMAND_DELAY
    ):
        self.sleep_time = command_delay
        self.timeout = timeout
        self.ip_address = ip_address
        self.port = port

    @abstractmethod
    def __str__(self):
        """This function returns a string describing the PDU's
        important attributes"""

    @abstractmethod
    def reboot(self, port_num):
        """This function will reboot a port you select"""

    @abstractmethod
    def on(self, port_num):
        """This funtion will turn on a port you select"""

    @abstractmethod
    def off(self, port_num):
        """This function will turn off a port you select"""

    @abstractmethod
    def is_on(self, port_num):
        """This function will return ON if selected port is on"""

    @abstractmethod
    def get_status(self):
        """This function will get the status of your PDU"""
