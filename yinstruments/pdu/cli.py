from netbooter import Netbooter
from lindy import Lindy
import argparse


def main():
    # create instance of argparse
    arguments = argparse.ArgumentParser(description="Command Line Arguments")
    arguments.add_argument(
        "dev_type",
        type=str,
        help="Brand of pdu you are communicating with",
        choices=("netbooter, lindy"),
    )
    arguments.add_argument("ip_address", type=str, help="IP of your pdu")
    arguments.add_argument(
        "command",
        type=str,
        help="string of command type to issue to PDU",
        choices=("on", "off", "reboot", "get_status"),
    )
    arguments.add_argument(
        "port_num", type=str, help="Port number to perform action on"
    )
    args = arguments.parse_args()

    # These four variables are your arguments you will enter into the command line
    dev_type = args.dev_type
    ip_address = args.ip_address
    cmd = args.command
    port_num = args.port_num
    # These four variables are your arguments you will enter into the command line

    if dev_type.lower() == "netbooter":
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

    elif dev_type == "lindy":
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


if __name__ == "__main__":
    main()
