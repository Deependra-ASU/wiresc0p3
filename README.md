# Wiresc0p3

## Network Monitor

The network monitor is responsible for monitoring network calls and processing them into cohesive TCP exchange entries.

Source: src/network_monitor

### Setup

- Requires MongoDB, install locally using `docker-compose up -d`.
- Install [MongoDB](https://www.mongodb.com/products/compass) Compass to view the database and perform queries.

### Usage

_Note: It is assumed that you are in the ./network_monitor path when executing the following commands._
- Start the `process_tcpflow.py` script. This will start a file listener looking for new files in `./out/tcpflow/`.
- Find the interface you want to listen on `netstat -i`.
- Run tcpdump `sudo tcpdump -i <interface> -s 65535 -w ./out/tcpdump/capture-%s -G 60 -Z $(whoami)`.
- Run tcpflow bash script `./tcp_flow.sh`.

The tcpflow script can be executed periodically using a [cronjob](https://man7.org/linux/man-pages/man5/crontab.5.html).

### Test application

We used a sample web application with vulnerabilities called [damn vulnerable web application](https://dvwa.co.uk/).
- Start sample web application: `docker run --name webapp --rm -itd -p 8090:80 vulnerables/web-dvwa`
- Stop sample web application: `docker stop webapp`
- Look at the logs of the docker: `docker logs webapp`

### References

- http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/
- https://linux.die.net/man/8/tcpdump
- https://www.systutorials.com/docs/linux/man/1-tcpflow/
- https://docs.mongodb.com/manual/
