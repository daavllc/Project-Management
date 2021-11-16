# Project-Management.gui.windows.windows - GUI window that serves as the GUI start point/launcher
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

import config.config as config
import helpers as hp
from .ProjectExplorer import ProjectExplorer
from .ProjectProperty import ProjectProperty

class Windows:
    def __init__(self, parent):
        self.parent = parent # gui.gui.Application
        self.log = hp.Logger("PM.GUI.Windows", "gui.log")
        self.project = None

        self.Window: str = "MainWindow"
        self.Pre: str = "mw"

        with dpg.window(id="MainWindow", width=1280, height=720):
            pass

        self.width = dpg.get_item_width(self.Window)
        self.height = dpg.get_item_height(self.Window)

        self.ProjectProperty = ProjectProperty(self)
        self.ProjectExplorer = ProjectExplorer(self)

    def SetProject(self, prj):
        if prj is None:
            config.PATH_CURRENT_PROJECT = None
            self.log.debug(f"Set self.project = None")
        else:
            self.project = prj
            self.log.debug(f"Set self.project = {self.project.GetUUIDStr()}")
        self.ProjectProperty.RefreshAll()

    def Refresh(self):
        self.ProjectExplorer.Refresh()
        self.ProjectProperty.Refresh()
