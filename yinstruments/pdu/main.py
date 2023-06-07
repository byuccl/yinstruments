from netbooter import Netbooter
from lindy import Lindy
import os
import argparse

def print_usage():
    print("Incorrect usage!")
    print(os.path.splitext(__file__)[0], "<on|off|reboot|status> <port_num>")


def main():
    #create instance of argparse
    arguments = argparse.ArgumentParser(description="Command Line Arguments")
    arguments.add_argument('dev_type', type=str, help = "DEVELOPER TYPE: What brand of pdu you are communicating with --> 1st command line argument after file name")
    arguments.add_argument('ip_address', type=str, help = "IP ADDRESS: IP of your pdu --> 2nd command line argument")
    arguments.add_argument('command', type = str, help = "COMMAND: A string of what port number you would like to call a function on --> 3rd command line argument")
    arguments.add_argument('port_num', type=str, help = "PORT NUMBER: Which port you would like to interact with on your pdu --> 4th command line argument")
    args = arguments.parse_args()
    

    # These four variables are your arguments you will enter into the command line 
    dev_type = args.dev_type
    ip_address = args.ip_address
    cmd = args.command
    port_num = args.port_num
    # These four variables are your arguments you will enter into the command line 

    if dev_type.lower() == 'netbooter':
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

    elif dev_type == 'lindy':
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



