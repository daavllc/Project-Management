import os
import dearpygui.dearpygui as dpg

from common_types.contribution import Contribution
from gui.logger import Logger
import config.config as config
from .ContributionViewer import ContributionViewer

class ContributionExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectViewer
        self.contributions = []
        self.selection = None
        self.log = Logger("PM.Window.ContributionExplorer")

        self.Window = "ContributionExplorer"
        self.Pre = "ctbE"

        with dpg.window(tag=self.Window, label="Contribution Explorer", no_close=True):
            dpg.add_input_text(tag=f"{self.Pre}_CreateInput", hint="Create new", on_enter=True, callback=self.CreateContribution)
            dpg.add_separator(tag=f"{self.Pre}_CreateSeparator")
            self.GetContributions()
            self.DrawContributions()

        self.ContributionViewer = ContributionViewer(self)

    def CreateContribution(self, sender, app_data, user_data):
        self.log.debug(f"Creating new contribution '{app_data}'")
        self.contributions.append(app_data)
        self.SetSelection(len(self.contributions) - 1)
        ctb = Contribution()
        ctb.SetName(app_data)
        ctb.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}")
        self.DrawContributions()

    def GetContributions(self):
        if config.PATH_CURRENT_PROJECT is None:
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"
        for file in os.listdir(path):
            if os.path.isdir(path + "/" + file):
                self.contributions.append(file)
        self.log.debug(f"Got contributions: {str(self.contributions)}")

    def DrawContributions(self):
        if len(self.contributions) == 0:
            dpg.add_text(parent=self.Window, default_value="No contributions found!", tag=f"{self.Pre}_Contribution.0")
        else:
            for index in range(len(self.contributions)):
                try:
                    dpg.delete_item(f"{self.Pre}_Contribution.{index}")
                except SystemError:
                    pass
            index = 0
            for ctb in self.contributions:
                dpg.add_button(parent=self.Window, label=ctb, tag=f"{self.Pre}_Contribution.{index}", callback=self.SetSelection)
                index += 1

    def SetSelection(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[1])
        if index < 0 or index > len(self.contributions):
            self.selection = None
            self.log.debug(f"Set {self.selection = }")
            return
        self.selection = index
        self.log.debug(f"Set {self.selection = }, '{self.contributions[index]}'")
        self.ContributionViewer.InitContribution(self.contributions[index])
