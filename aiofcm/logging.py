import logging


logging.getLogger("aioopenssl").setLevel(logging.CRITICAL)
logging.getLogger("aiosasl").setLevel(logging.CRITICAL)

logger = logging.getLogger("aiofcm")
