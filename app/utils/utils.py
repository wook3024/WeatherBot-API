import time

from .. import logger


def elapsed_time(fn):
    def inner(*args, **kwargs):
        start_time = time.time()
        to_execute = fn(*args, **kwargs)
        end_time = time.time()
        process_time = end_time - start_time
        logger.info("{0} process time: {1:.8f}s".format(fn.__name__, process_time))
        return to_execute

    return inner
