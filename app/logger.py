# Python
import logging


def setup_logger():
    class PrintHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            print(log_entry)

    logger = logging.getLogger("my app")
    logger.setLevel(logging.DEBUG)

    ph = PrintHandler()
    ph.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ph.setFormatter(formatter)

    logger.addHandler(ph)

    return logger


logger = setup_logger()
