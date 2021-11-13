import os
import dearpygui.dearpygui as dpg

from common_types.project import Project

from gui.logger import Logger
import config.config as config
from .ProjectViewer import ProjectViewer

class ProjectExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.windows
        self.projects = []
        self.selection = None
        self.log = Logger("PM.Window.ProjectExplorer")

        self.Window = "ProjectExplorer"
        self.Pre = "pe"

        with dpg.window(tag=self.Window, label="Project Explorer", no_close=True):
            dpg.add_input_text(tag=f"{self.Pre}_CreateInput", hint="Create new", on_enter=True, callback=self.CreateProject)
            dpg.add_separator(tag=f"{self.Pre}_CreateSeparator")
            self.GetProjects()
            self.DrawProjects()

        self.ProjectViewer = ProjectViewer(self)

    def CreateProject(self, sender, app_data, user_data):
        self.log.debug(f"Creating new project '{app_data}'")
        self.projects.append(app_data)
        self.SetSelection(len(self.projects) - 1)
        prj = Project()
        prj.SetName(app_data)
        prj.Export(config.PATH_CURRENT_PROJECT)
        self.DrawProjects()

    def GetProjects(self):
        for file in os.listdir(config.PATH_ROOT):
            if os.path.isdir(config.PATH_ROOT + "/" + file):
                self.projects.append(file)
        self.log.debug(f"Got projects: {str(self.projects)}")

    def DrawProjects(self):
        if len(self.projects) == 0:
            dpg.add_text(parent=self.Window, default_value="No projects found!", tag=f"{self.Pre}_Project.0")
        else:
            for index in range(len(self.projects)):
                try:
                    dpg.delete_item(f"{self.Pre}_Project.{index}")
                except SystemError:
                    pass
            index = 0
            for project in self.projects:
                dpg.add_button(parent=self.Window, label=project, tag=f"{self.Pre}_Project.{index}", callback=self.SetSelection)
                index += 1

    def SetSelection(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[1])
        if index < 0 or index > len(self.projects):
            self.selection = None
            config.PATH_CURRENT_PROJECT = None
            self.log.debug(f"Set {self.selection = }")
            return
        self.selection = index
        self.log.debug(f"Set {self.selection = }, '{self.projects[index]}'")
        self.ProjectViewer.InitProject(self.projects[index])
