""" Logging utilities.
"""

import logging
import logging.handlers

from colorama import Fore, Style


COLORS = {
    'DEBUG': Style.DIM,
    'INFO': Style.NORMAL,
    'WARNING': Style.BRIGHT,
    'ERROR': Fore.RED,
    'CRITICAL': Style.BRIGHT + Fore.RED,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        return COLORS[record.levelname] + logging.Formatter.format(self, record) + Style.RESET_ALL


def setup_logging(verbose=True, color=True):
    """ Sets logging format. """

    logging.getLogger().setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG if verbose else logging.INFO)
    if color:
        stream_format = ColoredFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
    else:
        stream_format = logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
    stream.setFormatter(stream_format)
    logging.getLogger().addHandler(stream)
    logging.getLogger('requests').setLevel(logging.ERROR)
