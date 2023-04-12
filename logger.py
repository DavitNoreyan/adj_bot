import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Logger:
    debug = logging.debug
    info = logging.info
    warning = logging.warning
    error = logging.error
    critical = logging.critical

    def get_logger(self):
        return self
