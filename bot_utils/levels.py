import logging
from os import environ, path
from sys import stdout

def log_threshold():
    if environ.get('FITNR_DEV', False) and not environ.get('FITNR_PROD', False):
        # environment = 'development'
        threshold = logging.DEBUG
    else:
        # environment = 'production'
        threshold = logging.INFO

    return threshold

def add_logger(logger_name, log_path="bots/logs"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_threshold())

    log_file = path.join(path.expanduser('~'), log_path, logger_name + '.log')
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter('%(asctime)s %(name)-16s line %(lineno)d %(levelname)-5s %(message)s'))

    logger.addHandler(fh)

    return logger

def add_stdout_logger(logger_name):
    logger = logging.getLogger(logger_name)

    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(filename)s:%(lineno)-3d %(message)s'))

    logger.addHandler(ch)
