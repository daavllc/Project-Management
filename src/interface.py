# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python 3.10
# License: GPLv3

from enum import Enum, auto
import os

from cui.cui import CUI
from gui.gui import GUI

import config.config as config

class Type(Enum):
    CUI = CUI()
    GUI = GUI()

class UI:
    def __init__(self, args):
        self.inst = args.UI

    def Start(self):
        self.inst = self.inst.value
        if not os.path.exists(config.PATH_ROOT):
            os.mkdir(config.PATH_ROOT)
        self.inst.Launch(self) # pass in UI as parent