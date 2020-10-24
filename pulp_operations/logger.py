"""parent logging settings"""

import logging
import logging.handlers as handlers

#create instance 'logger' with base logging level
logger = logging.getLogger('pulp_operations')
logger.setLevel(logging.DEBUG)

#define format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
