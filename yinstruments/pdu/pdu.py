"""This file contains the top level PDU class"""

from abc import abstractmethod
from enum import Enum


class PDUType(Enum):
    Netbooter = 1
    Lindy = 2


class PDU:

    """Generic class for PDU"""

    # initializes your PDU with callable characteristics
    @abstractmethod
    def __init__(self, ip_address, port, timeout=3.0):
        self.sleep_time = 1.0
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
