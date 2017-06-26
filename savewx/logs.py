import logging

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
frmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(frmt)
logger.addHandler(ch)