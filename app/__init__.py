import logging

from hydra import compose, initialize
from omegaconf import OmegaConf

from .log import configure_logging


configure_logging()
logger = logging.getLogger("default")

with initialize(config_path="conf", job_name="dev_app"):
    cfg = compose(config_name="config")

logger.debug("Hydra config: \n{}".format(OmegaConf.to_yaml(cfg)))

__all__ = ["cfg", "logger"]
