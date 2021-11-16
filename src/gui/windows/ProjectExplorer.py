# Project-Management.gui.windows.ProjectExplorer - GUI explorer window for viewing projects
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os
import dearpygui.dearpygui as dpg

from objects.project import Project

import helpers as hp
import gui.utils as utils
import config.config as config

class ProjectExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.windows
        self.projects = []
        self.log = hp.Logger("PM.GUI.Windows.ProjectExplorer", "gui.log")

        self.Window = "ProjectExplorer"
        self.Pre = "pX"

        with dpg.window(tag=self.Window, label="Project Explorer", no_close=True):
            dpg.add_button(parent=self.Window, tag=f"{self.Pre}_CreateProject", label="Create New", callback=self.CreateCallback)
            dpg.add_separator(parent=self.Window, tag=f"{self.Pre}_CreateSeparator")

        self.width = dpg.get_item_width(self.Window)
        self.height = dpg.get_item_height(self.Window)

        self.Refresh()

    def SetSelection(self, index: int):
        if index < 0 or index > len(self.projects):
            self.parent.SetProject(None)
        else:
            self.parent.SetProject(self.projects[index])

    def InitProject(self, filename: str = None) -> Project:
        prj = Project()
        if filename is None:
            prj.Export()
            self.projects.append(prj)
            self.log.debug(f"Created new project {prj.GetUUIDStr()}")
            config.PATH_CURRENT_PROJECT = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{prj.GetUUIDStr()}"
            self.log.debug(f"Set {config.PATH_CURRENT_PROJECT = }")
            self.DrawProjects()
        else:
            self.log.debug(f"Loading project: {filename}")
            prj.LoadHeader(filename)
        return prj

    def GetProjects(self):
        self.projects = []
        for file in os.listdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}"):
            if os.path.isdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{file}"):
                self.projects.append(self.InitProject(file))
        self.log.debug(f"Found {len(self.projects)} project(s): {[prj.GetName() for prj in self.projects]}")

    def DrawProjects(self):
        utils.DeleteItems(f"{self.Pre}.Projects")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Projects"):
            if len(self.projects) == 0:
                dpg.add_text(tag=f"{self.Pre}.Projects.NoneFound", default_value="No projects found!")
            else:
                index = 0
                for prj in self.projects:
                    dpg.add_button(tag=f"{self.Pre}.Projects.Prj.{index}", label=prj.GetName(), callback=self.SelectCallback)
                    index += 1

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[-1])
        if index < 0 or index > len(self.projects):
            return
        self.projects[index].Import(self.projects[index].GetUUIDStr())
        self.SetSelection(index)

    def CreateCallback(self):
        self.InitProject()
        self.SetSelection(len(self.projects) - 1)

    def Refresh(self):
        self.GetProjects()
        self.DrawProjects()
