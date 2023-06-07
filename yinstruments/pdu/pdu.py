from abc import abstractmethod



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

    @abstractmethod
    def get_status(self):
        pass
