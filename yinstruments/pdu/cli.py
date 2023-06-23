"""This the file that will run to execute calls on your PDU"""
import argparse
from .netbooter import Netbooter
from .lindy import Lindy


def main():
    """Main function: creates instance of argparse and lays out the
    logic for your inputs."""

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
        choices=("on", "off", "is_on", "reboot", "get_status"),
    )
    arguments.add_argument("port_num", type=str, help="Port number to perform action on")
    args = arguments.parse_args()

    # These four variables are your arguments you will enter into the command line
    dev_type = args.dev_type
    ip_address = args.ip_address
    cmd = args.command
    port_num = args.port_num
    # These four variables are your arguments you will enter into the command line

    if dev_type.lower() == "netbooter":
        port = 23
        pdu = Netbooter(ip_address, port)
    elif dev_type == "lindy":
        port = 80
        pdu = Lindy(ip_address, port)

    if cmd == "on":
        pdu.on(port_num)
    elif cmd == "off":
        pdu.off(port_num)
    elif cmd == "reboot":
        pdu.reboot(port_num)
    elif cmd == "is_on":
        print(pdu.is_on(port_num))
    elif cmd == "get_status":
        print(pdu.get_status())


if __name__ == "__main__":
    main()
