import re

def filter_payload(payload, portnum, isIncoming):
    filter_all_result = filter_all(payload, isIncoming)
    if filter_all_result == 0:
        return False
    if filter_all_result == 1:
        return True
    
    # Example for branching logic for services.  Once ports are known,
    #   add more cases/functions here
    if portnum == 20000:
        return filter20000(payload, isIncoming)
    return False;

def filter_all(payload, isIncoming):
    # Return values: 0: exclude, 1: include, 2: defer to port-specific filter
    # Modify this during gameplay as desired
    if not isIncoming and re.search('FLG\w{20}\s', payload): # Example
        return 1
    return 2

def filter20000(payload, isIncoming):
    # Example filter for function on port 20000.  During environment setup, create a
    #   similarly named filter function for each port on which a service is listening.
    if isIncoming and (len(payload) > 1000 or 'bin' in payload):
        return True
    return False
