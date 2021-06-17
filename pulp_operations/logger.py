"""parent logging settings"""

import logging
import logging.handlers as handlers

#create instance 'logger' with base logging level
logger = logging.getLogger('pulp_operations')
logger.setLevel(logging.DEBUG)

#using this format so splunk picks up the fields automatically
formatter = logging.Formatter(
    fmt='Time="%(asctime)s", Module="%(name)s", Level="%(levelname)s", Message="%(message)s"',
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)

#define time-based rotating file handler
fh = handlers.TimedRotatingFileHandler(
    '/var/log/pulp_operations.log', #path
    when = "d", #rotate on days
    interval = 1, #number of days
    backupCount = 30 #automatically delete after this qty
)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

#define console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

#add handlers to instance 'logger'
logger.addHandler(fh)
logger.addHandler(ch)
