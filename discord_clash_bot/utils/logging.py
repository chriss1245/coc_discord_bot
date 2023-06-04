"""
Logging utils
"""

import logging
from pathlib import Path

from .config import SECRETS, PROJECT_DIR

ROOT_LOGGER_NAME = "discord_coc_bot"
LOG_PATH = None
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
}

if "logging" in SECRETS:
    LOG_PATH = SECRETS["logging"]["path"]
    # if  log_path is not absolute, use the project dir
    if not Path(LOG_PATH).is_absolute():
        LOG_PATH = PROJECT_DIR / LOG_PATH
    else:
        LOG_PATH = Path(LOG_PATH)


def get_logger(name: str, level: str = "INFO"):
    """
    Create a logger

    Args:
        name (str): Name of the logger
        level (int, optional): Level of the logger. Defaults to logging.INFO.
        log_path (Path, optional): Path to the log file. Defaults to None.

    Returns:
        logging.Logger: Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS[level])

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if LOG_PATH is not None:
        logg_file = LOG_PATH / f"{name.replace('.', '-')}.log"
        logg_file.touch(exist_ok=True)
        file_handler = logging.FileHandler(logg_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_module_logger(module, level: str = "INFO"):
    """
    Create a logger for a module using the module name
    and the package name and the root logger name

    Args:
        module (module): Module to create the logger for
        level (int): Level of the logger

    Returns:
        logging.Logger: Logger
    """
    if module is None:
        return get_logger(ROOT_LOGGER_NAME, level)

    return get_logger(f"{ROOT_LOGGER_NAME}.{module}", level)
