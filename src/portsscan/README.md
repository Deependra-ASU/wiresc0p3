## PortsScanner

This tool is used to check if given ports are open or closed of other teams. 

## Usage
This tool scans every port to see if there is a response. To launch this tool just make sure the IPs are set manually. The only thing required is the port range, then fill out the array hostname which is a list of the teams that will be scanned.

Example:

a)Run 

    gcc portsscan.c -o portscan

b)Then 

    ./portscan <port no>

Make sure to edit hostname array manually and enter Ip's to scan.

## References
https://stackoverflow.com/questions/20636558/c-port-scanner/20639783


