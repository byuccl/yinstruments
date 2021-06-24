from Pyoscilloscope.elements.channel_element import Measure_Element
from Pyoscilloscope.Oscilloscope import Interface, TriggerMode
def main():
    print("hello there :)")
    ip = "192.168.1.101"
    command_file = "oscilloscope_commands_Agilent_6000.json"
    scope = Interface(ip, command_file)
    scope.clear()
    scope.reset()
    scope.identify()
    scope.voltage_range[1] = 2
    scope.voltage_offset[1] = 12
    scope.time_range = 500e-6
    scope.time_division = 100e-6
    #scope.voltage_offset[1] = .5
    #scope.display_measurement(2, "vmax")
if __name__ == "__main__":
    main()