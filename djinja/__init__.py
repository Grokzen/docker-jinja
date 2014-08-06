# -*- coding: utf-8 -*-

""" dj - Docker-Jinja """

# import sys
import os

# init python std logging
import logging
import logging.config

__version__ = "14.07-dev"
__author__ = 'Grokzen <Grokzen@gmail.com>'

# Set to True to have revision from Version Control System in version string
__devel__ = True

# Global register dict of all registered methods and filters
# NOTE: This must be here so that it will be properly visible for all code and to make it work properly
_local_env = {
    "globals": {},
    "filters": {},
}

log_level_to_string_map = {
    5: "DEBUG",
    4: "INFO",
    3: "WARNING",
    2: "ERROR",
    1: "CRITICAL",
    0: "INFO"
}


def init_logging(log_level):
    """
    Init logging settings with default set to INFO
    """
    l = log_level_to_string_map[log_level]

    msg = "%(levelname)s - %(name)s:%(lineno)s - %(message)s" if l in os.environ else "%(levelname)s - %(message)s"

    logging_conf = {
        "version": 1,
        "root": {
            "level": l,
            "handlers": ["console"]
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": l,
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            }
        },
        "formatters": {
            "simple": {
                "format": " {}".format(msg)
            }
        }
    }

    logging.config.dictConfig(logging_conf)
