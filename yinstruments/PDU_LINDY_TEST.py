import subprocess
from time import sleep


outlets = list([-1] * 8)
def decodePowerValues(response):
    values = response[43:60]
    for i in range(1, 9):  # Loop from 1 to 8 (inclusive)
        outlets[i-1] = int(values[1 + (i - 1) * 2])


def printPowerValues():
    if outlets[0] == -1:
        updatePowerValues()
    print("Value of Outlets:")
    for i in range(1,9):
        print(f"\tOutlet {i}: {outlets[i-1]}")


def getPowerValues():
    # Command to be executed
    command = ['snmpwalk', '-v1', '-c', 'public', '192.168.0.216', 'iso.3.6.1.4.1.17420.1.2.9.1.13.0']
    # Run the command and capture the output
    output = subprocess.check_output(command)
    # Print the output
    return output.decode()


def setPowerValues(input):
        # Command to be executed
    if outlets[0] == -1:
        updatePowerValues()
    command = ['snmpset', '-v1', '-c', 'public', '192.168.0.216', 'iso.3.6.1.4.1.17420.1.2.9.1.13.0', "s", input]
    # Run the command and capture the output
    output = subprocess.check_output(command)
    # Print the output
    return output.decode()


def updatePowerValues(print=False):
    response = getPowerValues()
    decodePowerValues(response)
    if print:
        printPowerValues()


def setPowerValue(index, value=1, print=False):
    if outputs[0] == -1:
        updatePowerValues()
    if index > 8:
        raise Exception("ERROR: Index given out of range")
        return
            # Command to be executed
    input = "0,0,0,0,0,0,0,0"
    for i in range(1,9):
        string_list = list(input)
        string_list[i*2-2] = str(outlets[i-1])
        input = ''.join(string_list)
    string_list = list(input)
    string_list[index*2-2] = str(value)
    input = ''.join(string_list)
    command = ['snmpset', '-v1', '-c', 'public', '192.168.0.216', 'iso.3.6.1.4.1.17420.1.2.9.1.13.0', "s", input]
    # Run the command and capture the output
    output = subprocess.check_output(command)
    # Print the output
    if print:
        print(output.decode())
    return output.decode()


# updatePowerValues(True)
# print(setPowerValues("0,1,0,1,0,1,1,1"))
# sleep(8)
updatePowerValues(True)
setPowerValue(1, 0)
sleep(8)
updatePowerValues(True)