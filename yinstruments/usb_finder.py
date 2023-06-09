from pathlib import Path
import re
import subprocess

import pyudev


class USBFindError(Exception):
    pass


def find_dev_file_ttyUSB(usb_phys_port, interface):
    """This will find the correct /dev/ttyUSBX file for a given physical USB port and interface.

    Interface for Ultra96 (0 = jtag, 1 = uart)
    """

    match_str = match_str = "/devices/.*?/.*?/usb\d+/.*/(.*?)/ttyUSB\d+/tty/ttyUSB\d+$"
    return _find_dev_file(usb_phys_port, "USB", match_str, interface)


def find_dev_file_ttyACM(usb_phys_port, interface):
    """This will find the correct /dev/ttyACMX file for a given physical USB port and interface."""

    match_str = match_str = "/devices/.*?/.*?/usb\d+/.*/(.*?)/tty/ttyACM\d+$"
    return _find_dev_file(usb_phys_port, "ACM", match_str, interface)


def _find_dev_file(usb_phys_port, ttyType, match_str, interface):
    """This function will search through all /dev devices and find the one that maps to the given
    usb_phys_port, ttyType, regex match string and interface.

    This function works by running "udevadm info -q path -n /dev/ttyUSB0" for each serial port,
    and looking for the output that matches the location.  For example, if it is located at
    1-10.1, the output of interface 1 will be
    /devices/pci0000:00/0000:00:14.0/usb1/1-10/1-10.1/1-10.1:1.1/ttyUSB3/tty/ttyUSB3
    """

    # Iterate over all files in /dev
    match_found = None
    p = None
    for f in Path("/dev").iterdir():
        if re.match("/dev/tty" + ttyType + "\d+", str(f)):
            p = subprocess.run(
                ["udevadm", "info", "-q", "path", "-n", str(f)], stdout=subprocess.PIPE
            )
            # print(p.stdout.decode())
            # print(match_str)
            m = re.match(match_str, p.stdout.decode())
            if not m:
                raise USBFindError("Serial find regex error")
            if m.group(1) == (usb_phys_port + ":1." + str(interface)):
                if match_found is not None:
                    raise USBFindError(
                        "Multiple serial device matches for USB location "
                        + usb_phys_port
                        + ": "
                        + match_found
                        + " and "
                        + f
                    )
                match_found = f
                # print(p.stdout.decode())
            if not m:
                print(p.stdout.decode(), "did not match regex.")
                assert False
    if match_found is None:
        raise USBFindError(
            "Could not find serial device at USB location " + usb_phys_port + ":1." + str(interface)
        )

    return match_found


def find_dev_file_usb_bus(usb_phys_port):
    """
    For a given usb physical port, this function finds the USB bus device file.

    For example, a USB device at physical port 1-7.1 may be mapped to bus=3,device=7, which
    would mean that the associated usb bus device file would be
    /dev/bus/usb/003/007
    """
    context = pyudev.Context()
    devPath = None
    for device in context.list_devices(subsystem="tty"):
        if "DEVPATH" in device.properties and usb_phys_port in device.properties["DEVPATH"]:
            devPath = device.properties["DEVPATH"]
            break

    if devPath is None:
        raise USBFindError("Could not find serial device at USB location " + usb_phys_port)

    # we need the first 5 directories of the path.
    # for example if the result from udevadm is /devices/pci0000:00/0000:00:14.0/usb1/1-2/1-2:1.1/ttyUSB1/tty/ttyUSB1
    # then we want /devices/pci0000:00/0000:00:14.0/usb1/1-2/

    # easy trick to see what level of a USB-Hub the device is is to count the number of '.' in the port
    # (none indicates it's not part of a USB-Hub)
    usb_level = usb_phys_port.count(".")

    usb_dir = "/sys/" + "/".join(devPath.split("/")[1 : 6 + usb_level])
    # print(usb_dir)

    with open(usb_dir + "/devnum", "r") as f:
        dev_num = int(f.read())

    with open(usb_dir + "/busnum", "r") as f:
        bus_num = int(f.read())

    # print(bus_num, dev_num)
    return Path(f"/dev/bus/usb/{bus_num:03}/{dev_num:03}")
