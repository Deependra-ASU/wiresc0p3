import types, codecs, os, time, sys, datetime
import filters.tcpdump_filter as tcpdump_filter

from scapy.all import *
from scapy.layers.http import HTTP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Loopback

def get_epoch_seconds(filename):
    seconds = None
    try:
        filename_list = filename.split('-')
        seconds = int(filename_list[1])
    except(IndexError, ValueError):
        print('Failed to parse filename ' + filename)
    return seconds

def analyze_pcap(filename, log_files):
    print('analyzing file ' + filename + '\n')
    try:
        pkts = rdpcap('out/tcpdump/' + filename)
        for pkt in pkts:
            # if Raw in pkt:
            #     raw = pkt[Raw]
            #     hexdump(raw)
            isIncoming = None
            if IP in pkt:
                if pkt[IP].src == '192.160.0.20': # Replace with game server IP
                    isIncoming = True
                elif pkt[IP].dst == '192.160.0.20': # Replace with game server IP
                    isIncoming = False
            if isIncoming is not None and TCP in pkt:
                portnum = None
                if isIncoming:
                    portnum = pkt[TCP].dport
                else:
                    portnum = pkt[TCP].sport
                if portnum in log_files:
                    payload = pkt[TCP].payload
                    if tcpdump_filter.filter_payload(payload, portnum, isIncoming):
                        log_files[portnum].write(str(payload))
                        log_files[portnum].write('\n----------------------------\n')
        os.rename('out/tcpdump/' + filename, 'archive/' + filename)
    except(FileNotFoundError, IOError, Scapy_Exception):
        print('Failed to process pcap file (might be empty)')

def main():
    if len(sys.argv) < 2:
        print('Usage: ./test.py [<portnum>,<portnum>,...]')
        exit()

    port_nums = map(int, sys.argv[1].strip('[]').split(','))

    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('archive'):
        os.makedirs('archive')
    
    log_files = {};
    for port_num in port_nums:
        log_file = open('logs/service' + str(port_num), 'w+')
        log_files[port_num] = log_file
    
    while True:
        current_time = time.time()
        for filename in os.listdir('out/tcpdump'):
            ctime = get_epoch_seconds(filename)
            if current_time - ctime > 30:
                analyze_pcap(filename, log_files)
        for filename in os.listdir('archive'):
            ctime = get_epoch_seconds(filename)
            if current_time - ctime > 120:
                os.remove('archive/' + filename)
        time.sleep(15)

main()
