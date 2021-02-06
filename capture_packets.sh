#!/usr/bin/env bash

readonly HERE=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)
sudo tcpdump -i en0 -s 65535 -w ${HERE}/analyze/output.pcap -C 1
