##
# @file Logger.py
import logging

def initlog(logfile):
    logger = logging.getLogger()
    hdlr = logging.StreamHandler()
    hdlr = logging.FileHandler(logfile)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger
