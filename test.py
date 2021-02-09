import types, codecs, os, time, sys

from scapy.all import *
from scapy.layers.http import HTTP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Loopback

def get_file_list(port_nums):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_list = [];
    for port_num in port_nums:
        log_file = open("logs/service" + str(port_num), "a+")
        file_list.append(log_file)
    return file_list

def analyze_pcap(filename, port_nums, log_files):
    print('analyzing file ' + filename + '\n')
    pkts = rdpcap(filename)
    print(len(pkts))

    for pkt in pkts:
        # if Raw in pkt:
        #     raw = pkt[Raw]
        #     hexdump(raw)
        # TODO: if TCP, get portnum and match with log_file, get payload,
        # run against validator script, if passes write to log file

        # print(pkt.layers())
        layers = pkt.layers()
        log_files[0].write(str(layers) + '\n')

def main():
    if len(sys.argv) < 2:
        print("Usage: ./test.py [<portnum>, <portnum>, ...]")
        exit()

    port_nums = map(int, sys.argv[1].strip('[]').split(','))
    print(port_nums)

    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_files = [];
    for port_num in port_nums:
        log_file = open("logs/service" + str(port_num), "w+")
        log_files.append(log_file)
    
    pcap_filename = "analyze/output.pcap0"
    next_pcap_filename = "analyze/output.pcap1"
    while True:
        try:
            next_file = open(next_pcap_filename, "r")
            try:
                current_file = open(pcap_filename, "r")
                try:
                    analyze_pcap(pcap_filename, port_nums, log_files)
                except (Scapy_Exception):
                    print("Couldn't read packets from " + pcap_filename + " (may be empty)")
                current_file.close()
                os.remove(pcap_filename)
                temp = pcap_filename
                pcap_filename = next_pcap_filename
                next_pcap_filename = temp
            except (FileNotFoundError, IOError):
                print("Expected log file not found, skipping")
        except (FileNotFoundError, IOError):
            print("couldn't open file")
            time.sleep(1)

main()
