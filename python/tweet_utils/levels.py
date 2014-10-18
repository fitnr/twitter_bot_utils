import logging
from os import environ
from sys import stdout

if environ.get('FITNR_DEV', False) and not environ.get('FITNR_PROD', False):
    environment = 'development'
    log_threshold = logging.DEBUG
else:
    environment = 'production'
    log_threshold = logging.INFO

def add_stdout_logger(logger_name):
    logger = logging.getLogger(logger_name)
    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(filename)s:%(lineno)-3d %(message)s'))
    logger.addHandler(ch)
