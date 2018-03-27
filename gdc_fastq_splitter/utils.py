import logging

LOGGERS = {}

def get_handler():
    """Return a stdout stream handler"""
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    return handler

def get_logger(name):
    """Return an opinionated basic logger named `name` that logs to
    stdout."""
    if LOGGERS.get(name):
        return LOGGERS.get(name)
    else:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        if not (len(logger.handlers) > 0
                and type(logger.handlers[0]) == logging.StreamHandler):
            logger.addHandler(get_handler())
            logger.propagate = False
    return logger
