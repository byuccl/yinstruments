from yinstruments.powersupply import PowerSupply

IP_ADDRESS = "10.35.120.85"
PIN_1 = 1
PIN_2 = 2
PIN_3 = 3

ps = PowerSupply(IP_ADDRESS)

# --- Read a digital input pin ---
pin_to_read = PIN_3
ps.configure_dio_input(pin_to_read)
print(f"Pin {pin_to_read} value: {ps.read_dio_pin(pin_to_read)}")

# --- Set a digital output pin high ---
(pin_to_set, val) = (PIN_2, True)
ps.configure_dio_output(pin_to_set)
print(f"Setting pin {pin_to_set} high...")
ps.write_dio_pin(pin_to_set, val)
print(f"Pin {pin_to_set} value: {ps.read_dio_pin(pin_to_set)}")

# --- Make a loop that reads the state of one pin and sets another pin to the same state ---
input_pin = PIN_3
output_pin = PIN_2
ps.configure_dio_input(input_pin)
ps.configure_dio_output(output_pin)
while True:
    val = ps.read_dio_pin(input_pin)
    ps.write_dio_pin(output_pin, val)

# --- Set a digital output pin low ---
# ps.configure_dio_output(PIN)
# ps.write_dio_pin(PIN, False)

# --- Toggle a digital output pin ---
# ps.configure_dio_output(PIN)
# ps.write_dio_pin(PIN, True)
# import time
# time.sleep(1)
# ps.write_dio_pin(PIN, False)

# --- Read all 3 pins as inputs ---
# for p in range(1, ps.num_digital_io_channels + 1):
#     ps.configure_dio_input(p)
#     print(f"Pin {p} value: {ps.read_dio_pin(p)}")
