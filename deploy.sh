#!/usr/bin/env bash

if [[ "$#" -ne 3 ]]
then
  echo "Usage: ./deploy.sh <path/to/sshkey> <path/to/local/wiresc0p3/src> <ctf@IP:/path/to/dst>"
else
  rsync -r -e "ssh -i $1" $2 $3
fi

