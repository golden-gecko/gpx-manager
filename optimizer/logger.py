import logging


class Logger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

        if not logging.getLogger(name).hasHandlers():
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)5s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S'))

            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)
