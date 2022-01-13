# Project-Management.gui.windows.windows - GUI window that serves as the GUI start point/launcher
# Copyright (C) 2021-2022  DAAV, LLC
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
        self.manager = self.parent.manager

        self.Window = "PrimaryWindow"
        self.Pre = "Primary"

        with dpg.window(tag=self.Window):
            self.ProjectProperty = ProjectProperty(self, self.manager.Projects)
            self.ProjectExplorer = ProjectExplorer(self, self.manager.Projects)


    def SyncProject(self):
        self.ProjectExplorer.Refresh()
        self.ProjectProperty.Refresh()
        self.ProjectProperty.ContributorExplorer.Refresh()
        self.ProjectProperty.ContributionExplorer.Refresh()

    def Refresh(self):
        self.ProjectExplorer.Refresh()
        self.ProjectProperty.Refresh()
        self.ProjectProperty.ContributorExplorer.Refresh()
        self.ProjectProperty.ContributionExplorer.Refresh()
