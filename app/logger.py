import logging
import os

def logger(name) -> logging.Logger:
    if (not os.path.isdir("../logs/")):
        os.mkdir("../logs")
    logging.basicConfig(format=logging.BASIC_FORMAT, filename=f"../logs/{name}.log", filemode="a", level=logging.DEBUG)
    return logging.getLogger(name)
