from Pyoscilloscope.elements.channel_element import Measure_Element
from Pyoscilloscope.Oscilloscope import Interface, TriggerMode
def main():
    print("hello there :)")
    ip = "10.0.0.228"
    command_file = "oscilloscope_commands_Siglent_SDS_1052DL+.json"
    scope = Interface(ip, command_file)
    scope.clear()
    scope.reset()
    #scope.voltage_offset[1] = .5
    scope.display_measurement(2, "vmax")
if __name__ == "__main__":
    main()