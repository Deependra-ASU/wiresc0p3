# Wiresc0p3

Setup:

- List active interfaces: `netstat -i`
- Capture/Filter traffic using tcpdump:
-    `sudo tcpdump -i <interface> -s 65535 -w ${HERE}/out/tcpdump/capture-%s -G 15 -Z <user>`
-    `python3 ./process_tcpdump.py [<portnum1>,<portnum2>,...]`
-    
- Capture tcpflow from tcpdump:
-    `sudo tcpdump -s 65535 -w out/tcpdump/output.pcap -C 1 -W 2 -Z root`
-    `./tcp_flow.sh`

Test applications:

- Start sample web application: `docker run --name webapp --rm -itd -p 8090:80 vulnerables/web-dvwa`
- Stop sample web application: `docker stop webapp`
- Look at the logs of the docker: `docker logs webapp`

Python libraries:

- To get `file` command capability: https://github.com/ahupp/python-magic
