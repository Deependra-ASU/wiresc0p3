import codecs

from scapy.all import *
from scapy.layers.http import HTTP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Loopback

pcap_files = []
for (dir_path, dir_names, file_names) in os.walk('analyze'):
    pcap_files.extend(file_names)

for pcap_file in pcap_files:
    print(f'analyzing file ./analyze/{pcap_file}...\n')
    pkts = rdpcap(f'analyze/{pcap_file}')

    for pkt in pkts:
        # if Raw in pkt:
        #     raw = pkt[Raw]
        #     hexdump(raw)
        print(pkt.layers())
