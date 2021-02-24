# Recovery

## Description
This recovery script can monitor the status of each service running in the PCTF virtual machine. If the status becames 'Down', the recovery script will automatically copy the backup files back to the service's running directory and restart the docker container. 

## Installation
1. pip install pwntools
2. pip install swpag_client*

## Run
python3 recovery.py