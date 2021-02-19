all: portscan.c
	gcc -o portscan portscan.c
	mkdir -p out/tcpdump
	mkdir -p out/tcpflow
	chmod u+x checkfile.py
	chmod u+x honeypot.py
	chmod u+x mongo_connect.py
	chmod u+x process_tcpdump.py
	chmod u+x process_tcpflow.py
