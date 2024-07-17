
#  *******************************************************
#  *          SINCE THIS IS A DOCKER CONTAINER.          *
#  * AND IN EFFORT TO KEEP IT AS LIGHWEIGHT AS POSSIBLE  *
#  *       WE WILL NOT BE LOGGING TO BULKY FILES.        *
#  *              ONLY LOG TO STREAMHANDLER              *
#  *******************************************************

# Call initlogging() ASAP when starting the container

import logging
import os
from logging import LogRecord


def initlogging():
    """Inits global logging configuration"""
    envLogLevel = os.getenv('LOG_LEVEL', 'INFO').upper()
    if envLogLevel not in ['DEBUG', 'INFO']:
        envLogLevel = 'INFO'
    
    if envLogLevel == 'DEBUG':
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO


    class CustomFormatter(logging.Formatter):
        if logLevel == logging.DEBUG:
            FORMAT = '[%(asctime)s]  [%(funcName)s @ %(module)s] %(message)s'
        else:
            FORMAT = '[%(asctime)s] %(message)s'
        FORMATS = {
            logging.DEBUG: "[%(levelname)s] - " + FORMAT,
            logging.INFO: "[%(levelname)s] - " + FORMAT,
            logging.WARNING: "[%(levelname)s] - " + FORMAT,
            logging.ERROR: "[%(levelname)s] - " + FORMAT,
            logging.CRITICAL: "[%(levelname)s] - " + FORMAT
        }

        def format(self, record: LogRecord) -> str:
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)
    
    logger = logging.getLogger()
    logger.setLevel(logLevel)

    ch = logging.StreamHandler()
    ch.setLevel(logLevel)
    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)

    logger.debug(f'Logging level set to {envLogLevel}')
