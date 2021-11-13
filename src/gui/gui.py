
import logging

from common_types.base_types.version import Version as Version
from common_types.contributor import Contributor
from common_types.contribution import Contribution
import config.config as config

class GUI:
    def __init__(self):
        self.parent = None

    def Launch(self, parent):
        self.parent = parent
        print("Launching GUI...")
        self._Start()

    def _Start(self):
        print("Not currently implemented!")
        input("Press enter to continue...")
        exit(-1)