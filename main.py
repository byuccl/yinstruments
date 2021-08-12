from Pyoscilloscope.Oscilloscope import Interface
def main():
    print("Hello Welcome to the scope test")
    ip = "10.0.0.228"
    command_file = "Siglent_SDS_1052DL+.json"
    scope = Interface(ip, command_file)
    print(scope.identify())
    scope.reset()
    print(scope.wave_preamble[1])
    
    

if __name__ == "__main__":
    main()