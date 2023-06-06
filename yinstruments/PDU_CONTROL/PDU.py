import enum


class PduType(enum.Enum):
    NETBOOTER = 1
    LINDY = 2


class PDU:
    # generic class for PDU devices

    # initializes your PDU with callable characteristics
    def __init__(self, ip_address, port, timeout=3.0):
        self._SLEEP_TIME = 1.0
        self.timeout = timeout
        self.ip_address = ip_address
        self.port = port

    def __str__(self):
        pass

    def reboot(self):
        pass

    def on(self):
        pass

    def off(self):
        pass

    def get_status(self):
        pass
