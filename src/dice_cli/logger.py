import logging
from typing import Dict

from rich.logging import RichHandler

from .utils import current_date, current_linux_user


class LevelFormatter(logging.Formatter):
    """
    From https://stackoverflow.com/a/28636024/362457
    """

    def __init__(self, fmt: str, datefmt: str, level_fmts: Dict):
        self._level_formatters = {}
        for level, format in level_fmts.items():
            # Could optionally support level names too
            self._level_formatters[level] = logging.Formatter(
                fmt=format, datefmt=datefmt
            )
        # self._fmt will be the default format
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        if record.levelno in self._level_formatters:
            return self._level_formatters[record.levelno].format(record)

        return super().format(record)


admin_logger = logging.getLogger("dice_admin")
admin_logger.setLevel(logging.INFO)

user_logger = logging.getLogger("dice_user")
user_logger.setLevel(logging.INFO)

console_formatter = LevelFormatter(
    fmt="%(asctime)s [%(name)s]  %(levelname)s: %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
    level_fmts={
        logging.INFO: "%(message)s",
        logging.WARNING: "%(levelname)s: %(message)s",
        logging.ERROR: "%(levelname)s: %(message)s",
    },
)
console_handler = RichHandler(
    # rich_tracebacks=True, # does not work with custom formatters
    markup=True,
    show_level=False,
    show_time=False,
)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)
console_handler.formatter = console_formatter

logfile_formatter = logging.Formatter(
    "%(asctime)s [%(name)s]  %(levelname)s: %(message)s"
)
logfile_handler = logging.FileHandler(
    f"/tmp/dice_commands_{current_linux_user()}_{current_date()}.log"
)
logfile_handler.setLevel(logging.DEBUG)
logfile_handler.setFormatter(logfile_formatter)

admin_logger.addHandler(console_handler)
admin_logger.addHandler(logfile_handler)

user_logger.addHandler(console_handler)
user_logger.addHandler(logfile_handler)
