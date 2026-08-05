import os
import unittest

from yinstruments.powersupply import PowerSupply

TEST_IP = os.environ.get("TEST_PS_IP", None)
# TEST_IP = "10.85.1.221"


@unittest.skipIf(not TEST_IP, "Requires physical power supply")
class TestPowerSupplySlew(unittest.TestCase):
    def test_slew_control(self):
        ps = PowerSupply(TEST_IP)
        self.assertTrue(ps.supports_slew, "Power supply should support slew control")

        # Test setting and getting rising and falling voltage slew rates
        test_rising = 10.0
        test_falling = 5.0

        ps.set_channel_voltage_slew_rising(1, test_rising)
        ps.set_channel_voltage_slew_falling(1, test_falling)

        self.assertAlmostEqual(ps.get_channel_voltage_slew_rising(1), test_rising, places=2)
        self.assertAlmostEqual(ps.get_channel_voltage_slew_falling(1), test_falling, places=2)

        # Test setting combined voltage slew rate
        combined_slew = 12.5
        ps.set_channel_voltage_slew_rate(1, combined_slew)
        slew_tuple = ps.get_channel_voltage_slew_rate(1)
        self.assertAlmostEqual(slew_tuple[0], combined_slew, places=2)
        self.assertAlmostEqual(slew_tuple[1], combined_slew, places=2)

        # Test resetting slew rate using class constants SLEW_MAX and SLEW_MIN
        ps.set_channel_voltage_slew_rate(1, PowerSupply.SLEW_MIN)
        self.assertLess(ps.get_channel_voltage_slew_rising(1), 1.0)

        ps.set_channel_voltage_slew_rate(1, PowerSupply.SLEW_MAX)
        self.assertGreater(ps.get_channel_voltage_slew_rising(1), 1e9)
        self.assertGreater(ps.get_channel_voltage_slew_falling(1), 1e9)

    def test_slew_validation(self):
        ps = PowerSupply(TEST_IP)
        self.assertFalse(ps.validate_slew_rate(0))
        self.assertFalse(ps.validate_slew_rate(-1))
        self.assertFalse(ps.validate_slew_rate(500000))
        self.assertFalse(ps.validate_slew_rate("INVALID"))
        self.assertTrue(ps.validate_slew_rate("MAX"))
        self.assertTrue(ps.validate_slew_rate("MIN"))
        self.assertTrue(ps.validate_slew_rate(10.0))


if __name__ == "__main__":
    unittest.main()
