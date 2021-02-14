#!/usr/bin/env bash

set -o errexit

readonly HERE=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)

pushd ${HERE} > /dev/null
for file in ./out/tcpdump/*
do
  tcpflow -o ./out/tcpflow -e http -Fk -r "${file}"
done
popd > /dev/null
