import unittest

from yinstruments.pdu.lindy import Lindy
from yinstruments.pdu.netbooter import Netbooter


class TestPackaging(unittest.TestCase):
    def test_pdus(self):
        lindy = Lindy("192.168.0.0", "80")
        netbooter = Netbooter("192.168.0.0", "80")
