import logging
import sys

def setup_logger(name='AxonOpsLogger', level=logging.DEBUG):
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Clear existing handlers, and add new ones
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger