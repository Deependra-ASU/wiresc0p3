#!/usr/bin/env python

import os
import magic

curr_dir = os.path.dirname(os.path.realpath(__file__))
tcpf_root = f'{curr_dir}/outdir'

processed_dirs = []

for root, dirs, files in os.walk(tcpf_root):
    for fname in files:
        fq_filename = os.path.join(root, fname)
        file_type = magic.from_file(f'{fq_filename}')
        # request files have ASCII content
        if 'ASCII text' in file_type:
            print(f'REQUEST: {fname}')
            with open(fq_filename, 'r') as f:
                print(f.read())
            fname_parts = fname.split("-")
            # split and reverse the file name to get the response file name
            resp_fname = f'{fname_parts[1]}-{fname_parts[0]}'
            print(f'RESPONSE: {fq_filename}')
            # response file has binary content
            with open(os.path.join(root, resp_fname), 'rb') as f:
                print(f.read())
            print('........')
