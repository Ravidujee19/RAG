from loguru import logger


def setup_logging() -> None:
    logger.remove()
    logger.add(lambda msg: print(msg, end=""))
