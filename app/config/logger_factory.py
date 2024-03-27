import http.client as http_client
import logging
from logging import LogRecord

from config.settings import settings, Environment


class OneLineExceptionFormatter(logging.Formatter):
    _spacer: str = '|'

    def set_spacer(self, spacer: str):
        self._spacer = spacer

    def formatException(self, ei) -> str:
        return repr(super().formatException(ei))

    def format(self, record: LogRecord) -> str:
        result = super().format(record)

        if record.exc_text:
            result = result.replace('\n', self._spacer)
        return result


def logger_factory():
    # Set logging level
    logging_level_interpreter = {
        Environment.PROD: 'WARNING',
        Environment.TEST: 'INFO',
        Environment.DEV: 'DEBUG'
    }
    logging_level = logging_level_interpreter[settings.ENVIRONMENT]

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)

    # Create logger
    logger = logging.getLogger('_api_')
    logger.setLevel(logging_level)
    logger.propagate = False

    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)

    # Create formatter
    formatter_format = '%(asctime)s - %(levelname)s - %(module)s - line:%(lineno)d - %(message)s'
    if settings.ENVIRONMENT == Environment.PROD:
        formatter = OneLineExceptionFormatter(formatter_format)
        formatter.set_spacer(' - ')
    else:
        formatter = logging.Formatter(formatter_format)

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)
    # Add ch to root logger
    root_logger.addHandler(ch)

    if settings.ENVIRONMENT == Environment.DEV:
        http_client.HTTPConnection.debuglevel = 1
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
