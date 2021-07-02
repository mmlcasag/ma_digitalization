import logging
import os
import datetime


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=SingletonType):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s"
        )

        now = datetime.datetime.now()

        dirname = "./output"
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        dirname = "./output/logs"
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        fileHandler = logging.FileHandler(
            dirname + "/log_" + now.strftime("%Y-%m-%d_%H:%M:%S") + ".log", "w"
        )

        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

        print("Generate new instance of logger")

        print("Suppress logs from third-party modules")
        disable_loggers = ["PIL"]
        for logger_name in disable_loggers:
            logging.getLogger(logger_name).setLevel(logging.INFO)

    def get_logger(self):
        return self._logger


# a simple usecase
if __name__ == "__main__":
    logger = Logger.__call__().get_logger()
    logger.info("Hello, Logger")
    logger.debug("bug occured")
