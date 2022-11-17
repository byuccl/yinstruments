import subprocess
import time

import argparse

import pyhubctl

from utils import error, print_color, TermColors

# TODO: At one point uhubctl failed with the following error:
# uhubctl: symbol lookup error: uhubctl: undefined symbol: libusb_free_container_id_descriptor
# I restarted the NUC and it worked, but I don't know what went wrong.
# That error was invisible to the other scripts...


class USBPortPower:
    """
    This is a simple wrapper around the pyhubctl package and can be used to power on/off USB ports
    (provided that the USB hub supports this functionality)
    """

    def __init__(self, usb_phys_port):
        self.usb_location = ".".join(usb_phys_port.split(".")[:-1])
        self.usb_port = usb_phys_port.split(".")[-1]
        self.phc = pyhubctl.PyHubCtl()

    def cycle(self):
        """Power cycle port.  Can raise subprocess.CalledProcessError"""
        self.phc.run(
            pyhubctl.Configuration(action="cycle", location=self.usb_location, ports=self.usb_port)
        )

    def off(self):
        """Turn off port.  Can raise subprocess.CalledProcessError"""
        self.phc.run(
            pyhubctl.Configuration(action="off", location=self.usb_location, ports=self.usb_port)
        )

    def on(self):
        """Turn on port.  Can raise subprocess.CalledProcessError"""
        self.phc.run(
            pyhubctl.Configuration(action="on", location=self.usb_location, ports=self.usb_port)
        )


def usbPowerCycle(usb_phys_port):

    usb_location = ".".join(usb_phys_port.split(".")[:-1])
    usb_port = usb_phys_port.split(".")[-1]
    print(" ".join(["uhubctl", "-a", "off", "-l", usb_location, "-p", usb_port]))
    proc_off = subprocess.run(
        ["uhubctl", "-a", "off", "-l", usb_location, "-p", usb_port],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)
    proc_on = subprocess.run(
        ["uhubctl", "-a", "on", "-l", usb_location, "-p", usb_port],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)

    if proc_off.returncode or proc_on.returncode:
        return False
    else:
        return True


def power_off(usb_phys_port, print_output=False):
    usb_location = ".".join(usb_phys_port.split(".")[:-1])
    usb_port = usb_phys_port.split(".")[-1]

    cmd = ["uhubctl", "-a", "off", "-l", usb_location, "-p", usb_port, "-r", "10"]
    proc_off = subprocess.run(cmd, capture_output=True, universal_newlines=True)

    if print_output:
        print(" ".join(cmd))
        print(proc_off.stdout)

    if proc_off.returncode:
        return False
    else:
        return True


def power_on(usb_phys_port, print_output=False):
    usb_location = ".".join(usb_phys_port.split(".")[:-1])
    usb_port = usb_phys_port.split(".")[-1]
    cmd = ["uhubctl", "-a", "on", "-l", usb_location, "-p", usb_port, "-r", "10"]
    proc_on = subprocess.run(cmd, capture_output=True, universal_newlines=True)

    if print_output:
        print(" ".join(cmd))
        print(proc_on.stdout)

    if proc_on.returncode:
        return False
    else:
        return True


def main():
    #  Power cycle UART USB port
    print("Power cycling UART")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "usb_physical_port", help="The physical port of the USB (1-1.1 for example)"
    )

    args = parser.parse_args()

    result = usbPowerCycle(args.usb_physical_port)

    if True:
        print_color(TermColors.GREEN, "Success")
    else:
        error("USB power cycle failed")


if __name__ == "__main__":
    main()
    # usbPowerCycle("1-1.1")
