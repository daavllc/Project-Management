# Project-Management.logger - helper for logging
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os
import logging

import config.config as config

class Logger:
    def __new__(cls, name: str, filename: str, writeConsole: bool = True, writeFile: bool = True):
        """Generates helpers.Logger instance

        Args:
            name (str): specify the logger's name
            file (str): specify log file name

        Returns:
            helpers.Logger
        """

        formatter = logging.Formatter('%(asctime)s <%(name)s> %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)

        if writeConsole:
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(formatter)
            log.addHandler(sh)

        if writeFile and not filename is None:
            if not os.path.exists(f"{config.PATH_ROOT}/logs"):
                os.mkdir(f"{config.PATH_ROOT}/logs")
            fh = logging.FileHandler(filename=f"{config.PATH_ROOT}/logs/{filename}")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            log.addHandler(fh)

        return log