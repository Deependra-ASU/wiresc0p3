#!/usr/bin/env python

import os
import re

watch_ports = ['8090']

curr_dir = os.path.dirname(os.path.realpath(__file__))
flow_root_dir = f'{curr_dir}/out/tcpflow'


def construct_response_file_name(fname):
    fname_segments = fname.split("-")
    opt_suffix = ''
    # handle cases where the file name contains suffixes like c1, c2, etc
    if 'c' in fname_segments[1]:
        split_suffix = fname_segments[1].split('c')
        fname_segments[1] = split_suffix[0]
        opt_suffix = 'c' + split_suffix[1]
    resp_file_name = f'{fname_segments[1]}-{fname_segments[0]}{opt_suffix}'
    return resp_file_name


def extract_port_numbers(file_name):
    file_name_segments = file_name.split("-")
    from_port = int(file_name_segments[0][len(file_name_segments[0]) - 5:])
    if 'c' in file_name_segments[1]:
        file_name_segments[1] = file_name_segments[1].split('c')[0]
    to_port = int(file_name_segments[1][len(file_name_segments[1]) - 5:])
    return from_port, to_port


def process_request_file(root_dir, file_name):
    fq_file_name = os.path.join(root_dir, file_name)
    requests = []
    ri = -1
    with open(fq_file_name, 'r') as f:
        content = f.read()
        lines = content.splitlines()
        for line in lines:
            if len(line) > 0:
                print(f'processing line: {line}')
                all_matches = re.finditer("(GET|HEAD|POST|PUT|DELETE) (/?/?)[^\\s]+ HTTP/.*", line)
                match_count = 0
                for match in all_matches:
                    match_count += 1
                    if match.start(0) > 0:
                        requests[ri]['request_line'] = line[:match.start(0)]
                        requests.append({'request_header': line[match.start(0):]})
                        ri = len(requests) - 1
                if match_count == 0:
                    requests[ri]['request_headers'] = line
                else:
                    requests.append({'request_line': line})
                    ri = len(requests) - 1
    return requests


def process_response_file(root_dir, file_name):
    pass


def extract_http_interaction(root_dir, file_name):
    fq_filename = os.path.join(root_dir, file_name)
    filtered_ports = [port for port in watch_ports if (port in fq_filename)]
    if len(filtered_ports) > 0:
        from_port, to_port = extract_port_numbers(file_name)
        if str(from_port) in watch_ports:
            process_response_file(root_dir, file_name)
        if str(to_port) in watch_ports:
            # print(f'processing request file: {file_name}')
            reqs = process_request_file(root_dir, file_name)
            # for req in reqs:
            #     print(f'request: {req}')


def main():
    for root_dir, dirs, files in os.walk(flow_root_dir):
        for file_name in files:
            extract_http_interaction(root_dir, file_name)


if __name__ == '__main__':
    main()
