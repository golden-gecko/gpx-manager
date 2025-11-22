import logging


class Logger:
    def __init__(self):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S'))

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)

    def set_level(self, level):
        self.logger.setLevel(level)

    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)
