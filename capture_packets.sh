#!/usr/bin/env bash

readonly HERE=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
sudo tcpdump -s 65535 -w ${HERE}/analyze/output.pcap -C 1 -W 2 -Z root
