import os
import dearpygui.dearpygui as dpg

from common_types.contributor import Contributor
from gui.logger import Logger
import config.config as config
from .ContributorViewer import ContributorViewer

class ContributorExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectViewer
        self.contributors = []
        self.selection = None
        self.log = Logger("PM.Window.ContributorExplorer")

        self.Window = "ContributorExplorer"
        self.Pre = "ctrE"

        with dpg.window(tag=self.Window, label="Contributor Explorer", no_close=True):
            dpg.add_input_text(tag=f"{self.Pre}_CreateInput", hint="Create new", on_enter=True, callback=self.CreateContributor)
            dpg.add_separator(tag=f"{self.Pre}_CreateSeparator")
            self.GetContributors()
            self.DrawContributors()

        self.ContributorViewer = ContributorViewer(self)

    def CreateContributor(self, sender, app_data, user_data):
        self.log.debug(f"Creating new contributor '{app_data}'")
        self.contributors.append(app_data)
        self.SetSelection(len(self.contributors) - 1)
        ctr = Contributor()
        ctr.SetName(app_data)
        ctr.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}")
        self.DrawContributors()

    def GetContributors(self):
        if config.PATH_CURRENT_PROJECT is None:
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}"
        for file in os.listdir(path):
            if os.path.isdir(path + "/" + file):
                self.contributors.append(file)
        self.log.debug(f"Got contributors: {str(self.contributors)}")

    def DrawContributors(self):
        if len(self.contributors) == 0:
            dpg.add_text(parent=self.Window, default_value="No contributors found!", tag=f"{self.Pre}_Contributors.0")
        else:
            for index in range(len(self.contributors)):
                try:
                    dpg.delete_item(f"{self.Pre}_Contributors.{index}")
                except SystemError:
                    pass
            index = 0
            for ctb in self.contributors:
                dpg.add_button(parent=self.Window, label=ctb, tag=f"{self.Pre}_Contributors.{index}", callback=self.SetSelection)
                index += 1

    def SetSelection(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[1])
        if index < 0 or index > len(self.contributors):
            self.selection = None
            self.log.debug(f"Set {self.selection = }")
            return
        self.selection = index
        self.log.debug(f"Set {self.selection = }, '{self.contributors[index]}'")
        self.ContributorViewer.InitContributor(self.contributors[index])
