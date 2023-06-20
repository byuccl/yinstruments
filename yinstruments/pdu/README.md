This file will explain how to use, add to, and customize the files 
in the folder pdu

CLASS STRUCTURES: Located in PDU.py, Netbooter.py, and Lindy.py you'll
see several classes that help organization and drive connections to different
PDUs. The PDU class is the parent class to the Netbooter and Lindy. All of these 
classes have the following callable functions: get_status, reboot, off, and on.

SETUP: There are two things that you will need to do before the commands provided will work:

    1. make python enviornment and go into enviornment
        --> make env
        --> source .venv/bin/activate

    2. install snmp package into your enviornment
        --> sudo apt update
        --> sudo apt install snmp snmpd


HOW TO RUN: You will need 4 command line arguments NOT including this python file. 
The command line call will look something like this:
        
    pdu <dev_type> <ip_address> <command> <port_num>
        
