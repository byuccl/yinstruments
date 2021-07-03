from Pyoscilloscope.elements.channel_element import Measure_Element
from Pyoscilloscope.Oscilloscope import Interface, TriggerMode
def main():
    ip = "10.0.0.228"
    command_file = "Siglent_SDS_1052DL+.json"
    scope = Interface(ip, command_file)
    scope.identify()
    scope.reset()
    scope.trigger_sweep = "auto"
    scope.trigger_mode["EX"] = "edge"

if __name__ == "__main__":
    main()