import socket
import atexit
import sys
# Local IP/Port for the honeypot to listen on (TCP)
LHOST = '0.0.0.0'
LPORT = int(sys.argv[1])

TIMEOUT = 10

def main():
    print ('[*] Honeypot starting on ' + LHOST + ':' + str(LPORT))
    atexit.register(exit_handler)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((LHOST, LPORT))
    listener.listen(5)
    while True:
        (insock, address) = listener.accept()
        insock.settimeout(TIMEOUT)
        print ('[*] Honeypot connection from ' + address[0] + ':' + str(address[1]) + ' on port ' + str(LPORT))
        insock.close()

def exit_handler():
    print ('\n[*] Honeypot is shutting down!')
    listener.close()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
