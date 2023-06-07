import enum
from main import main
from abc import abstractmethod


class PduType(enum.Enum):
    NETBOOTER = 1
    LINDY = 2


class PDU:
    # generic class for PDU devices

    # initializes your PDU with callable characteristics
    @abstractmethod
    def __init__(self, ip_address, port, timeout=3.0):
        self._SLEEP_TIME = 1.0
        self.timeout = timeout
        self.ip_address = ip_address
        self.port = port

    @abstractmethod
    def __str__(self):
        return f"{self.ip_address}:{self.port}"

    @abstractmethod
    def reboot(self):
        pass

    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    def get_status(self):
        pass


"""This file will explain how to use, add to, and customize the files 
in the folder PDU_CONTROL"""


"""CLASS STRUCTURES: Located in PDU.py, Netbooter.py, and Lindy.py you'll
see several classes that help organization and drive connections to different
PDUs. The PDU class is the parent class to the Netbooter and Lindy. All of these 
classes have the following callable functions: get_status, reboot, off, and on."""

"""HOW TO CALL FUNCTIONS: All edits to change the behavior of script are made in main.py.
The variable that you should look for are:

ip_address: A string of the ip_address of your PDU device
cmd: A string of the callable function you want to call on a port (note: It does not matter what port_num is when you call get_status())
port_num: A string of what port number you would like to call a function on
dev_type: What class object you are calling the function on

If you are not looking to add to this folder, those are the only edits you will have to make."""


"""HOW TO RUN: Once you have set the variables to what you want, just run the following
in a terminal:
        
    python3 PDU.py
        
        """



if __name__ == "__main__":
    main()
