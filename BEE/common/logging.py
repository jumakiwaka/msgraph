import logging


def get_logger(name):

    logger = logging.getLogger(name)

    sh = logging.StreamHandler()

    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.setLevel(level=logging.DEBUG)

    return logger
