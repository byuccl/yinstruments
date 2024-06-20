This file will explain how to use, add to, and customize the files 
in the folder pdu

CLASS STRUCTURES: Located in PDU.py, Netbooter.py, and Lindy.py you'll
see several classes that help organization and drive connections to different
PDUs. The PDU class is the parent class to the Netbooter and Lindy. All of these 
classes have the following callable functions: get_status, reboot, off, and on.

    CLI:


        SETUP: There are two things that you will need to do before the commands provided will work:

            --> make env
            --> source .venv/bin/activate
        
        PACKAGE: You will need to install the snmp package into your enviorment or where you will be running commands:

            --> sudo apt update
            --> sudo apt install snmp snmpd

        To instance a version of your pdu in a different file, add the following code:

            from yinstruments.pdu.lindy import Lindy
            from yinstruments.pdu.netbooter import Netbooter


        Example of calling an instance of a pdu:

            lindy = Lindy(192.168.1.250, 80) (where 80 is the communication port)



        HOW TO RUN: You will need 4 command line arguments NOT including this python file. The command line would look something like this:
        
            pdu <dev_type> <ip_address> <command> <port_num>

            Example with values:

            pdu lindy 192.168.1.250 on 2
        
