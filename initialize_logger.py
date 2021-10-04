import logging
from logging import Formatter, StreamHandler


class StreamHandlerErrorsOnly(StreamHandler):
    def emit(self, record):
        if record.levelno != logging.ERROR:
            return
        super().emit(record)

class StreamHandlerInfoOnly(StreamHandler):
    def emit(self, record):
        if record.levelno != logging.INFO:
            return
        super().emit(record)

info_log_format = "%(message)s"
error_log_format = "[%(levelname)s]: %(message)s"

output_logger = logging.getLogger(name="penguin")
output_logger.setLevel(logging.INFO)

error_console_handler = StreamHandlerErrorsOnly()
error_console_handler.setLevel(logging.ERROR)
error_console_handler.setFormatter(Formatter(error_log_format))

info_console_handler = StreamHandlerInfoOnly()
info_console_handler.setLevel(logging.INFO)
info_console_handler.setFormatter(Formatter(info_log_format))

output_logger.addHandler(error_console_handler)
output_logger.addHandler(info_console_handler)
