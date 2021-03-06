# Project-Management.interface - Start UI based on user input
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

from enum import Enum
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
        if not os.path.exists(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}"):
            os.mkdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}")
        self.inst.Launch()
