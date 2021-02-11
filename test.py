import types, codecs, os, time, sys, datetime

from scapy.all import *
from scapy.layers.http import HTTP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import Loopback

def get_epoch_seconds(filename):
    print("getting seconds from " + filename)
    seconds = None
    try:
        filename_list = filename.split('-')
        seconds = int(filename_list[1])
    except(IndexError, ValueError):
        print("Failed to parse filename" + filename)
    return seconds

def analyze_pcap(filename, port_nums, log_files):
    print('analyzing file ' + filename + '\n')
#    try:
    pkts = rdpcap('analyze/' + filename)

    for pkt in pkts:
        # if Raw in pkt:
        #     raw = pkt[Raw]
        #     hexdump(raw)
        # TODO: if TCP, get portnum and match with log_file, get payload,
        # run against validator script, if passes write to log file
        
        # print(pkt.layers())
        layers = pkt.layers()
        log_files[0].write(str(layers) + '\n')
    os.rename('analyze/' + filename, 'archive/' + filename)
#    except(FileNotFoundError, IOError, Scapy_Exception):
#        print("Failed to process pcap file (might be empty)")

def main():
    if len(sys.argv) < 2:
        print("Usage: ./test.py [<portnum>,<portnum>,...]")
        exit()

    port_nums = map(int, sys.argv[1].strip('[]').split(','))

    if not os.path.exists('logs'):
        os.makedirs('logs')
    if not os.path.exists('archive'):
        os.makedirs('archive')
    
    log_files = [];
    for port_num in port_nums:
        log_file = open("logs/service" + str(port_num), "w+")
        log_files.append(log_file)
    
    while True:
        print("new iteration")
        current_time = time.time()
        for filename in os.listdir('analyze'):
            ctime = get_epoch_seconds(filename)
            print("deltatime")
            print(current_time - ctime)
            if current_time - ctime > 30:
                analyze_pcap(filename, port_nums, log_files)
        for filename in os.listdir('archive'):
            ctime = get_epoch_seconds(filename)
            if ctime - current_time > 120:
                os.remove(filename)
        time.sleep(15)

main()
