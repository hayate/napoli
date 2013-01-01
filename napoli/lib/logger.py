import os
import sys
import logging
import logging.handlers
from datetime import date
from config import Config


class Log(object):
    __state = {}
    """
    simple logging.Logger wrapper
    """
    def __init__(self):
        """ Borg pattern """
        self.__dict__ = self.__state
        if '_log' not in self.__dict__:
            config = Config.get_instance()
            path = config.logging.get('log_path', os.path.abspath(os.path.join(os.environ['APPPATH'], '../logs')))
            filepath = os.path.join(path, 'log-' + str(date.today()) + '.log')
            try:
                handler = logging.handlers.TimedRotatingFileHandler(filepath, 'midnight', 1, 10, 'UTF-8')
            except IOError as ex:
                # check if log directory exists
                if not os.path.exists(path):
                    # try to create the logs directory
                    os.makedirs(path, mode=0755)
                # and try again
                handler = logging.handlers.TimedRotatingFileHandler(filepath, 'midnight', 1, 10, 'UTF-8')

            level = getattr(logging, config.logging.get('level', 'DEBUG').upper(), int);
            formatter = logging.Formatter('%(levelname)s - %(asctime)s - File:%(pathname)s - Line:%(lineno)d - Func:%(funcName)s\n%(message)s')
            handler.setLevel(level)
            handler.setFormatter(formatter)
            self._log = logging.getLogger(__name__)
            self._log.setLevel(level)
            self._log.addHandler(handler)

    @classmethod
    def get_instance(self):
        return self()

    def debug(self, msg, *args, **kwargs):
        """
        logger.DEBUG: 10
        """
        self._log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        logger.INFO: 20
        """
        self._log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        logger.WARNING 30
        """
        self._log.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        logger.ERROR: 40
        """
        self._log.error(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        """
        logger.FATAL: 50
        """
        self._log.fatal(msg, *args, **kwargs)

    def exception(self, msg, *args):
        self._log.exception(msg, *args)

    def __getattr__(self, name):
        return getattr(self._log, name)