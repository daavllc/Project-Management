
import os
import dearpygui.dearpygui as dpg

from common_types.project import Project

from gui.logger import Logger
import config.config as config
from .ContributionExplorer import ContributionExplorer
from .ContributorExplorer import ContributorExplorer

class ProjectViewer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.windows
        self.project = None
        self.log = Logger("PM.Window.ProjectViewer")

        self.Window = "ProjectViewer"
        self.Pre = "pv"

        with dpg.window(tag=self.Window, label="Project Viewer", no_close=True):
            self.DrawProjectInfo()

        self.ContributionExplorer = ContributionExplorer(self)
        self.ContributorExplorer = ContributorExplorer(self)

    def InitProject(self, name: str):
        prj = Project()
        prj.Import(config.PATH_ROOT, name)
        self.SetProject(prj)

    def SetProject(self, project: Project):
        self.project = project
        try:
            dpg.delete_item(f"{self.Pre}_NotSelected")
        except SystemError:
            pass
        self.ContributionExplorer.GetContributions()
        self.ContributionExplorer.DrawContributions()
        self.ContributorExplorer.GetContributors()
        self.ContributorExplorer.DrawContributors()
        self.DrawProjectInfo()

    def DrawProjectInfo(self):
        if self.project is None:
            dpg.add_text(parent=self.Window, default_value="No project selected", tag=f"{self.Pre}_NotSelected")
            return
        for name in ["_ProjectName", "_ProjectUUID", "_ProjectDate", "_ProjectLead", "_ProjectVersion" "_ProjectTitleGroup"]:
            try:
                dpg.delete_item(f"{self.Pre}{name}")
            except SystemError:
                pass
        with dpg.group(parent=self.Window, horizontal=True, tag=f"{self.Pre}_ProjectTitleGroup"):
            dpg.add_text(default_value=f"Project: '{self.project.GetName()}' :", tag=f"{self.Pre}_ProjectName")
            dpg.add_text(default_value=self.project.GetUUIDStr(), tag=f"{self.Pre}_ProjectUUID")
        dpg.add_text(parent=self.Window, default_value=f"Creation date: {self.project.GetDateStr()}", tag=f"{self.Pre}_ProjectDate")
        dpg.add_text(parent=self.Window, default_value=f"Project Lead: {self.project.GetLead()}", tag=f"{self.Pre}_ProjectLead")
        dpg.add_text(parent=self.Window, default_value=f"Version: {self.project.GetVersionStr()}", tag=f"{self.Pre}_ProjectVersion")