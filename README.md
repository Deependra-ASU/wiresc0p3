# Wiresc0p3

Setup:

- List active interfaces: `netstat -i`
- Capture traffic using tcpdump: `sudo tcpdump -i <interface> -s 65535 -w ${HERE}/analyze/capture-%s -G 15 -Z <user>`
- Capture tcpflow from tcpdump: `tcpflow -o outdir -Fk -r analyze/output_00001_20210206152809`

Test applications:

- Start sample web application: `docker run --name webapp --rm -itd -p 8090:80 vulnerables/web-dvwa`
- Stop sample web application: `docker stop webapp`
- Look at the logs of the docker: `docker logs webapp`

Python libraries:

- To get `file` command capability: https://github.com/ahupp/python-magic
