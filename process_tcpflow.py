#!/usr/bin/env python3

import os
import re
import time
import ntpath
import mongo_connect
import process_tcpflow_filter
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# list all the server ports that we want to watch
watch_server_ports = ['8090']
curr_dir = os.path.dirname(os.path.realpath(__file__))
flow_root_dir = f'{curr_dir}/out/tcpflow'


def extract_port_numbers(file_name):
    file_name_segments = file_name.split("-")
    from_port = int(file_name_segments[0][len(file_name_segments[0]) - 5:])
    if 'c' in file_name_segments[1]:
        file_name_segments[1] = file_name_segments[1].split('c')[0]
    to_port = int(file_name_segments[1][len(file_name_segments[1]) - 5:])
    return from_port, to_port


def process_request_file(root_dir, file_name):
    fq_file_name = os.path.join(root_dir, file_name)
    print(f'processing request file: {file_name}')
    http_requests = []
    with open(fq_file_name, 'r') as f:
        content = f.read()
        lines = content.splitlines()
        req_body = ''
        for line in lines:
            # append new requests to the end of the list
            req_idx = len(http_requests) - 1
            if len(line) > 0:
                http_header_matches = re.finditer("(GET|HEAD|POST|PUT|DELETE) /", line)
                http_header_found = False
                header_found_index = 0
                # request line which contains the http method marks the beginning of the request
                for http_header_match in http_header_matches:
                    http_header_found = True
                    header_found_index = http_header_match.start(0)
                if http_header_found:
                    # handle requests where http method is not at index 0 of line
                    if header_found_index > 0:
                        req_body = line[:header_found_index]
                        http_requests.append({'request_line': line[header_found_index:]})
                    else:
                        http_requests.append({'request_line': line})
                else:
                    req_body = line
            if ':' in req_body:
                http_requests[req_idx]['headers'] = req_body
            else:
                http_requests[req_idx]['payload'] = req_body
    return http_requests


def process_response_file(root_dir, file_name):
    fq_file_name = os.path.join(root_dir, file_name)
    print(f'processing response file {file_name}...')
    http_responses = []
    with open(fq_file_name, 'rb') as f:
        content = f.read()
        lines = content.splitlines()
        for line in lines:
            res_idx = len(http_responses) - 1
            try:
                str_line = line.decode()
                if 'HTTP/1.1' in str_line:
                    idx = str_line.index('HTTP/1.1')
                    if idx > 0:
                        http_responses[res_idx]['response_headers'] += f'{str_line[:idx]};'
                    resp = {'response_line': str_line[idx:], 'response_headers': '', 'response_bytes': ''}
                    http_responses.append(resp)
                else:
                    http_responses[res_idx]['response_headers'] += f'{str_line};'
            except UnicodeDecodeError as ude:
                if b'HTTP/1.1' in line:
                    idx = line.index(b'HTTP/1.1')
                    if idx > 0:
                        http_responses[res_idx]['response_bytes'] += str(line[:idx])
                    resp = {'response_line': line[idx:].decode(), 'response_headers': '', 'response_bytes': ''}
                    http_responses.append(resp)
                else:
                    http_responses[res_idx]['response_bytes'] += str(line)
    return http_responses


def convert_to_resp_filename(file_name):
    file_name_segments = file_name.split("-")
    opt_suffix = ''
    # handle cases where the file name contains suffixes like c1, c2, etc
    if 'c' in file_name_segments[1]:
        split_suffix = file_name_segments[1].split('c')
        file_name_segments[1] = split_suffix[0]
        opt_suffix = 'c' + split_suffix[1]
    resp_file_name = f'{file_name_segments[1]}-{file_name_segments[0]}{opt_suffix}'
    return resp_file_name


def extract_http_interaction(root_dir, file_name):
    fq_filename = os.path.join(root_dir, file_name)
    filtered_ports = [port for port in watch_server_ports if (port in fq_filename)]
    if len(filtered_ports) > 0:
        # only process request/response files initially
        from_port, to_port = extract_port_numbers(file_name)
        # communication from server to client are responses
        if str(from_port) in watch_server_ports:
            responses = process_response_file(root_dir, file_name)
            if responses is not None and len(responses) > 0:
                process_tcpflow_filter.filter(responses, from_port, False)
                return file_name, responses
        # communication from client to server are requests
        if str(to_port) in watch_server_ports:
            reqs = process_request_file(root_dir, file_name)
            if reqs is not None and len(reqs) > 0:
                process_tcpflow_filter.filter(reqs, to_port, True)
                rev_file_name = convert_to_resp_filename(file_name)
                return rev_file_name, reqs
    return '', []


def process_tcpflow_file(event):
    fq_file_name = event.src_path
    if os.path.isfile(fq_file_name) and not str(fq_file_name).endswith('report.xml'):
        root_dir, file_name = ntpath.split(fq_file_name)
        if 'HTTPBODY' not in file_name:
            key, http_items = extract_http_interaction(root_dir, file_name)
            interaction_count = mongo_connect.count_interactions_by_id(key)
            for http_item in http_items:
                # no interaction saved in database
                if interaction_count == 0:
                    if 'request_line' in http_item:
                        mongo_connect.save_interaction({'interaction_id': key, 'request': http_item})
                    elif 'response_line' in http_item:
                        mongo_connect.save_interaction({'interaction_id': key, 'response': http_item})
                else:
                    saved_interactions = mongo_connect.get_interactions_by_id(key)
                    for saved_interaction in saved_interactions:
                        if 'request' in saved_interaction and 'response_line' in http_item:
                            mongo_connect.update_interaction(saved_interaction['_id'], {'response': http_item})
                        elif 'response' in saved_interaction and 'request_line' in http_item:
                            mongo_connect.update_interaction(saved_interaction['_id'], {'request': http_item})
        else:
            with open(os.path.join(root_dir, file_name), 'rb') as f:
                content = f.read()
                file_name_frags = file_name.split("-")
                identifier = f'{file_name_frags[0]}-{file_name_frags[1]}'
                file_type = file_name[file_name.rindex('.') + 1:]
                interaction = {'interaction_id': identifier, 'type': file_type, 'content': content}
                mongo_connect.save_interaction(interaction)


if __name__ == '__main__':
    tcpflow_event_handler = PatternMatchingEventHandler("*", "", False, True)
    tcpflow_event_handler.on_created = process_tcpflow_file

    tcpflow_observer = Observer()
    tcpflow_observer.schedule(tcpflow_event_handler, flow_root_dir, recursive=True)
    tcpflow_observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        tcpflow_observer.stop()
    tcpflow_observer.join()
