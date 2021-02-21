# Wiresc0p3

## Setup

- List active interfaces: `netstat -i`

### Capture/Filter traffic using tcpdump

- `sudo tcpdump -i <interface> -s 65535 -w ./out/tcpdump/capture-%s -G 15 -Z $(whoami)`
- `python3 ./process_tcpdump.py [<portnum1>,<portnum2>,...]`

### Capture tcpflow from tcpdump

- `sudo tcpdump -s 65535 -w out/tcpdump/output.pcap -C 1 -W 2 -Z root`
- `./tcp_flow.sh`

### Process tcpflow capture

- `chmod u+x process_tcpflow.py && ./process_tcpflow.py`

## Test applications

- Start sample web application: `docker run --name webapp --rm -itd -p 8090:80 vulnerables/web-dvwa`
- Stop sample web application: `docker stop webapp`
- Look at the logs of the docker: `docker logs webapp`

## Python libraries

- To get `file` command capability: https://github.com/ahupp/python-magic

## Complete set of steps to capture HTTP traffic

1. Run tcpdump to capture live
   traffic: `sudo tcpdump -i <interface> -s 65535 -w ./out/tcpdump/capture-%s -G 15 -Z $(whoami)`
2. Start mongodb: `docker-compose up -d`
3. Start process_tcpflow.py: `chmod u+x process_tcpflow.py && ./process_tcpflow.py`
4. Run tcpflow capture to interpret the captured tcpdump: `./tcp_flow.sh`
5. Copy tcpdump to local incrementally: `rsync -avzhe ssh ctf@34.208.182.250:~/src/network_monitor/out/tcpdump/* ./out/tcpdump`

## References

- http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/
- https://www.systutorials.com/docs/linux/man/1-tcpflow/

rsync -avzhe ssh root@192.168.0.100:/root/install.log /tmp/