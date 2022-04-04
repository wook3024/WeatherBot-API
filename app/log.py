import logging
import logging.config

from hydra import compose, initialize
from typing import Dict, Any
from pathlib import Path


with initialize(config_path="conf", job_name="dev_app"):
    cfg = compose(config_name="config")


MB = 1024 * 1024
BASE_DIR_PATH = Path(__file__).parent.parent
LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": cfg.log.disable_existing_loggers,
    "formatters": {
        "standard": {
            "format": "[%(levelname)4.4s %(asctime)s %(module)s:%(lineno)d] "
            "%(message)s",
            "datefmt": "%Y-%m-%d+%H:%M:%S",
        },
    },
    "handlers": {
        "internal": {
            "level": cfg.log.level,
            "class": "rich.logging.RichHandler",
            "omit_repeated_times": cfg.log.rich.omit_repeated_times,
            "rich_tracebacks": cfg.log.rich.rich_tracebacks,
            "show_path": cfg.log.rich.show_path,  # show log line # in debug mode
        },
        "uvicorn": {
            "level": cfg.log.level,
            "class": "rich.logging.RichHandler",
            "omit_repeated_times": cfg.log.rich.omit_repeated_times,
            "rich_tracebacks": cfg.log.rich.rich_tracebacks,
            "show_path": cfg.log.rich.show_path,  # show log line # in debug mode
        },
    },
    "loggers": {
        "default": {
            "handlers": ["internal"],
            "level": cfg.log.level,
            "propagate": cfg.log.propagate,
        },
        "uvicorn": {"handlers": [], "level": cfg.log.level},
        "uvicorn.error": {
            "handlers": ["uvicorn"],
            "level": cfg.log.level,
            "propagate": cfg.log.propagate,
        },
        "uvicorn.access": {
            "handlers": [],
            "level": cfg.log.level,
            "propagate": cfg.log.propagate,
        },
    },
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
