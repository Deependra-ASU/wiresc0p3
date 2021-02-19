import logging
import os
import filters.tcpflow_filter as tcpflow_filter
from logging.handlers import RotatingFileHandler

def filter(trafficList, portnum, isRequest):
    log_dir = 'logs/tcpflow' + str(portnum)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logfilename = log_dir + '/tcpflow' + str(portnum)
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        handler = RotatingFileHandler(logfilename, maxBytes=1048576, backupCount=5)
        logger.addHandler(handler)

    for traffic in trafficList:
        if tcpflow_filter.filter_traffic(traffic, portnum, isRequest):
            logger.info(str(traffic))
