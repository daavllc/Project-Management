# Project-Management.gui.windows.windows - GUI window that serves as the GUI start point/launcher
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

from enum import Enum

import dearpygui.dearpygui as dpg

from gui.logger import Logger
from .ProjectExplorer import ProjectExplorer

class Windows:
    def __init__(self, parent):
        self.parent = parent # gui.gui.Application
        self.log = Logger("PM.Window")

        self.ProjectExplorer = ProjectExplorer(self)
