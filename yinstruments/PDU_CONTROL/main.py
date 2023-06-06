import telnetlib
import time
import sys
import os
import re
import pysnmp
from abc import ABC, abstractmethod
import subprocess
from Lindy import Lindy
from Netbooter import Netbooter
from PDU import PduType, PDU


def print_usage():
    print("Incorrect usage!")
    print(os.path.splitext(__file__)[0], "<on|off|reboot|status> <port_num>")


def main():

    # pointers for which class to create
    LINDY = PduType.LINDY
    NETBOOTER = PduType.NETBOOTER

    # change these 4 variables
    ip_address = "192.168.1.250"
    cmd = "get_status"
    port_num = "2"
    dev_type = PduType.LINDY
    # change these 4 variables

    if dev_type == NETBOOTER:
        port = 23
        netbooter = Netbooter(ip_address, port)

        if cmd == "on":
            netbooter.on(port_num)
        elif cmd == "off":
            netbooter.off(port_num)
        elif cmd == "reboot":
            netbooter.reboot(port_num)
        elif cmd == "get_status":
            print(netbooter.get_status())

    elif dev_type == LINDY:
        port = 80
        lindy = Lindy(ip_address, port)

        if cmd == "on":
            lindy.on(port_num)
        elif cmd == "off":
            lindy.off(port_num)
        elif cmd == "reboot":
            lindy.reboot(port_num)
        elif cmd == "get_status":
            print(lindy.get_status())
