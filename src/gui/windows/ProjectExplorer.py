# Project-Management.gui.windows.ProjectExplorer - GUI explorer window for viewing projects
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os
import dearpygui.dearpygui as dpg

from common_types.project import Project

from gui.logger import Logger
import config.config as config
from .ProjectProperty import ProjectPropertyExplorer as ProjectProperty

class ProjectExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.windows
        self.projects = []
        self.project = None
        self.log = Logger("PM.Window.ProjectExplorer")

        self.Window = "ProjectExplorer"
        self.Pre = "pX"

        self.ProjectProperty = ProjectProperty(self)

        with dpg.window(tag=self.Window, label="Project Explorer", no_close=True):
            dpg.add_button(tag=f"{self.Pre}_CreateProject", label="Create New", callback=self.CreateCallback)
            dpg.add_separator(tag=f"{self.Pre}_CreateSeparator")
            self.Refresh()

    def SetSelection(self, index: int):
        if index < 0 or index > len(self.projects):
            self.project = None
            config.PATH_CURRENT_PROJECT = None
            self.log.debug(f"Set self.project = None")
        else:
            self.project = self.projects[index]
            config.PATH_CURRENT_PROJECT = f"{config.PATH_ROOT}/{self.project.GetUUIDStr()}"
            self.log.debug(f"Set self.project = {self.project.GetUUIDStr()}")
        self.log.debug(f"Set {config.PATH_CURRENT_PROJECT = }")
        self.ProjectProperty.Refresh()

    def InitProject(self, filename: str = None) -> Project:
        prj = Project()
        if filename is None:
            prj.Export()
            self.projects.append(prj)
            self.log.debug(f"Created new project {prj.GetUUIDStr()}")
            self.DrawProjects()
        else:
            self.log.debug(f"Loading project: {filename}")
            prj.Import(filename)
        return prj

    def GetProjects(self):
        self.projects = []
        for file in os.listdir(config.PATH_ROOT):
            if os.path.isdir(config.PATH_ROOT + "/" + file):
                prj = Project()
                prj.LoadHeader(file)
                self.projects.append(prj)
        self.log.debug(f"Got {len(self.projects)} projects")

    def DrawProjects(self):
        for index in range(len(self.projects) + 1):
            try:
                dpg.delete_item(f"{self.Pre}_Project.{index}")
            except SystemError:
                pass
        if len(self.projects) == 0:
            dpg.add_text(parent=self.Window, default_value="No projects found!", tag=f"{self.Pre}_Project.0")
        else:
            index = 0
            for project in self.projects:
                dpg.add_button(parent=self.Window, label=project.GetName(), tag=f"{self.Pre}_Project.{index}", callback=self.SelectCallback)
                index += 1

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[1])
        if index < 0 or index > len(self.projects):
            return
        self.InitProject(self.projects[index].GetUUIDStr())
        self.SetSelection(index)

    def CreateCallback(self):
        self.InitProject()
        self.SetSelection(len(self.projects) - 1)

    def Refresh(self):
        self.GetProjects()
        self.DrawProjects()
        self.ProjectProperty.Refresh()
