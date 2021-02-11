# Wiresc0p3

To capture pcap file we can use either wireshark or tcpdump. To use tcpdump run the following
command: `sudo tcpdump -s 65535 -w ${HERE}/analyze/output-%s -G 15 -Z root`
To capture tcpflow run the following command: `tcpflow -o outdir -Fk -r analyze/output_00001_20210206152809`

To get `file` command capability: https://github.com/ahupp/python-magic
