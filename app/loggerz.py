import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger():
    # create path to logs if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    #handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=2000000, backupCount=5)

    #formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
