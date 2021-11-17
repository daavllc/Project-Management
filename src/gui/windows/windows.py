# Project-Management.gui.windows.windows - GUI window that serves as the GUI start point/launcher
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

import config.config as config
import helpers as hp
from .ProjectExplorer import ProjectExplorer
from .ProjectProperty import ProjectProperty

class Windows:
    _instance = None
    def __init__(self, parent):
        self.parent = parent # gui.gui.Application
        self.log = hp.Logger("PM.GUI.Windows", "gui.log")
        self.project = None

        self.ProjectProperty = ProjectProperty(self)
        self.ProjectExplorer = ProjectExplorer(self)

    def SetProject(self, prj):
        if prj is None:
            config.PATH_CURRENT_PROJECT = None
            self.log.debug(f"Set self.project to None")
        else:
            self.project = prj
            self.project.SetCurrent()
        self.ProjectProperty.ContributorExplorer.Refresh()
        self.ProjectProperty.ContributionExplorer.Refresh()
        self.ProjectProperty.Refresh()

    def Refresh(self):
        self.ProjectExplorer.Refresh()
        self.ProjectProperty.Refresh()
