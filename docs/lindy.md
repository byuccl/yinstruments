# Lindy PDU

* [Link to web page](https://www.lindy-international.com/IPower-Switch-Classic-8.htm?websale8=ld0101.ld021102&pi=32657)
* [Link to user manual](https://www.lindy.co.uk/downloads/Manual_LINDY_32652_uk.pdf) 
  *Info on snmp commands starts on page 9 
* [Link to snmp guide](https://blog.b-nm.at/2016/06/17/lindy-ipower-switch-classic-8-snmp/)


Provide a brief description on how you got this to work
* To install this package on Ubuntu, follow these steps:
    * First, create a python enviornment
        * An example of this would be: conda create -n <name your env> python=<version of python you would like to use (suggested is 3.9 or newer)>
    * Once in that enviornment, run the following commands: 
        * sudo apt update
        * sudo apt install snmp snmpd
    * Now these commands should work when you are in your enviornment:
      * To get the status of your lindy ports:
        * snmpget -v1 -c public <ip_address of lindy> iso.3.6.1.4.1.17420.1.2.9.1.13.0
          * This will return a string of comma separated 1's and 0's, depending on what ports are turned on or off
      * To change the status of the ports:
        * snmpset -v1 -c public <ip_address of lindy> iso.3.6.1.4.1.17420.1.2.9.1.13.0 s "1,1,1,1,1,1,1,1" 
          *This command would turn all ports on
      * To get all high level OID's:
        * snmpwalk -v1 -c public <ip_address of lindy>
          *Will give you the base OID (iso.3.6.1.4.1.17420) along with a few other stored values
      * To get all OID's:
         * snmpwak -v1 -c public <ip_address of lindy> iso.3.6.1.4.1.17420
  
  //will edit these changes once I create the driver
* Provide a link to your lyndy python driver (in this repository)
* Provide an example
