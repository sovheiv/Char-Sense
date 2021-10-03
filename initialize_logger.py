import logging
from logging import Formatter


info_log_format = "%(message)s"
error_log_format = "[%(levelname)s]: %(message)s"

info_logger = logging.getLogger(name="penguin")
info_logger.setLevel(logging.INFO)

error_logger = logging.getLogger(name="kaban")
error_logger.setLevel(logging.ERROR)

info_console_handler = logging.StreamHandler()
info_console_handler.setLevel(logging.INFO)
info_console_handler.setFormatter(Formatter(info_log_format))

error_console_handler = logging.StreamHandler()
error_console_handler.setLevel(logging.ERROR)
error_console_handler.setFormatter(Formatter(error_log_format))

error_logger.addHandler(error_console_handler)
info_logger.addHandler(info_console_handler)
