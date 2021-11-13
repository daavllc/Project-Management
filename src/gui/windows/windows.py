from enum import Enum

import dearpygui.dearpygui as dpg

from gui.logger import Logger
from .ProjectExplorer import ProjectExplorer

class Windows:
    def __init__(self, parent):
        self.parent = parent # gui.gui.Application
        self.log = Logger("PM.Window")

        self.ProjectExplorer = ProjectExplorer(self)
