import subprocess
import pysnmp as snmp
from pdu import PDU


# try Monday to use the subprocess.run() method command to implement a working Lindy_class
# command = sys.argv[1]
# port_num = sys.argv[2]
# subprocess.run([])


class Lindy(PDU):

    def on(self, port_num):
        if (
            int(port_num) > 8
        ):  # Since we are working with the LindyIPowerClassic8, we don't want to accept a larger integer than 8
            raise Exception("ERROR: port_num given out of range")
        OID = "iso.3.6.1.4.1.17420.1.2.9.1.13.0"  # standard OID for the functions we will be doing
        status_list = self.get_status(OID).split(",")

        for i in range(
            1, len(status_list) + 1
        ):  # search the newly formed list for the index of the port num
            if i == int(port_num):
                status_list[i - 1] = "1"

        status_string = ",".join(
            status_list
        )  # joins list back together as string to be ready to use in command
        command = [
            "snmpset",
            "-v1",
            "-c",
            "public",
            f"{self.ip_address}",
            f"{OID}",
            "s",
            status_string,
        ]

        # execute the command
        subprocess.check_output(command)

        # print that the port_num is now on
        # print("On:", port_num)

    
    def off(self, port_num):
        if (
            int(port_num) > 8
        ):  # Since we are working with the LindyIPowerClassic8, we don't want to accept a larger integer than 8
            raise Exception("ERROR: port_num given out of range")
        OID = "iso.3.6.1.4.1.17420.1.2.9.1.13.0"  # standard OID for the functions we will be doing
        status_list = self.get_status(OID).split(",")

        for i in range(
            1, len(status_list) + 1
        ):  # search the newly formed list for the index of the port num
            if i == int(port_num):
                status_list[i - 1] = "0"

        status_string = ",".join(
            status_list
        )  # joins list back together as string to be ready to use in command
        command = [
            "snmpset",
            "-v1",
            "-c",
            "public",
            f"{self.ip_address}",
            f"{OID}",
            "s",
            status_string,
        ]

        # execute the command
        subprocess.check_output(command)

    
    def reboot(self, port_num):
        self.off(port_num)
        self.on(port_num)

    
    def get_status(self):
        # command that is going to be executed
        command = [
            "snmpwalk",
            "-v1",
            "-c",
            "public",
            f"{self.ip_address}",
            "iso.3.6.1.4.1.17420.1.2.9.1.13.0",
        ]
        # Run the command and capture the output
        output = subprocess.check_output(command)
        # return output
        string = output.decode()[43:60]
        #return string is a string of comma separated 1's and 0's. 1 means the port is on, 0 means the port is off.
        return string[1:16]
