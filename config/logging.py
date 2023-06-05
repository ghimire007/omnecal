import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
format = logging.Formatter(
    "[%(asctime)s %(name)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
)
filehandler = logging.FileHandler("debug.log")
filehandler.setFormatter(format)
logger.addHandler(filehandler)
