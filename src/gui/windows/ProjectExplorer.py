# Project-Management.gui.windows.ProjectExplorer - GUI explorer window for viewing projects
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import os
import dearpygui.dearpygui as dpg

from objects.project import Project

import helpers as hp
import gui.utils as utils
import config.config as config

class ProjectExplorer:
    def __init__(self, parent, manager):
        self.parent = parent # gui.gui.windows.windows
        self.manager = manager # manager.project.ProjectManager
        self.log = hp.Logger("PM.GUI.Windows.ProjectExplorer", "gui.log")

        self.Window = "ProjectExplorer"
        self.Pre = "pX"

        self.show: list[bool] = []

        with dpg.window(tag=self.Window, label="Project Explorer", no_close=True):
            with dpg.group(parent=self.Window, tag=f"{self.Pre}.Header", horizontal=True):
                dpg.add_input_text(tag=f"{self.Pre}.Header.Search", hint="Search", callback=self.SearchCallback)
                dpg.add_button(tag=f"{self.Pre}.Header.New", label="New", callback=self.CreateCallback)
            dpg.add_separator(parent=self.Window, tag=f"{self.Pre}.Header.CreateSeparator")

        self.width = dpg.get_item_width(self.Window)
        self.height = dpg.get_item_height(self.Window)

    def SetSelection(self, index: int):
        self.manager.Select(index)
        self.parent.SyncProject()

    def SyncShow(self):
        self.show = [True for name in self.manager.GetNames()]

    def DrawProjects(self):
        utils.DeleteItems(f"{self.Pre}.Projects")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Projects"):
            total = len(self.manager.GetNames())
            if total == 0:
                dpg.add_text(tag=f"{self.Pre}.Projects.NoneFound", default_value="No projects found!")
            else:
                if total == 1:
                    dpg.add_text(tag=f"{self.Pre}.Projects.Total", default_value=f"{total} project found")
                else:
                    dpg.add_text(tag=f"{self.Pre}.Projects.Total", default_value=f"{total} projects found")
                for idx, name in enumerate(self.manager.GetNames()):
                    if self.show[idx] is True:
                        dpg.add_button(tag=f"{self.Pre}.Projects.Prj.{idx}", label=name, callback=self.SelectCallback)

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[-1])
        self.SetSelection(index)

    def CreateCallback(self):
        self.manager.Create()
        self.show.append(True)
        self.parent.SyncProject()
        self.Refresh()

    def SearchCallback(self, sender, app_data, user_data) -> None:
        if app_data == '' or app_data is None:
            self.show = [True for _ in self.show]
        else:
            for idx, name in enumerate(self.manager.GetNames()):
                if name.startswith(app_data):
                    self.show[idx] = True
                else:
                    self.show[idx] = False
        self.DrawProjects()

    def Refresh(self):
        self.SyncShow()
        self.DrawProjects()
