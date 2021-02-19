def filter_traffic(traffic, portnum, isRequest):
    enabled = True; # Set to False to disable all filtered output
    if not enabled:
        return False
    
    filter_all_result = filter_all(traffic, isRequest)
    if filter_all_result == 0:
        return False
    if filter_all_result == 1:
        return True
    
    # Example for branching logic for services.  Once ports are known,
    #   add more cases/functions here
    if portnum == 20000:
        return filter20000(traffic, isRequest)
    return False;

def filter_all(traffic, isRequest):
    # Return values: 0: exclude, 1: include, 2: defer to port-specific filter
    # Modify this during gameplay as desired

    # Keys in traffic:
    #  Request: request, headers, payload
    #  Response: response_code, response_headers, response_bytes
    
    #Example
#    if isRequest and 'request' in traffic and 'ls' in traffic['request']:
#        return 1
#    elif isRequest and 'payload' in traffic and 'ls' in traffic['payload']:
#        return 1
    return 2

def filter20000(traffic, isRequest):
    # Example filter for function on port 20000.  During environment setup, create a
    #   similarly named filter function for each port on which a service is listening.
    return False
