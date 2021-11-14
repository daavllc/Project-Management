# Project-Management.gui.windows.ContributionExplorer - GUI explorer window for viewing project contributions
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os

import dearpygui.dearpygui as dpg

from gui.logger import Logger
import config.config as config

from common_types.contribution import Contribution

class ContributionExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectViewer
        self.contributions = []
        self.log = Logger("PM.Window.ContributionExplorer")

        self.Window = "ContributionExplorer"
        self.Pre = "ctbX"

        with dpg.window(tag=self.Window, label="Contribution Explorer", no_close=True):
            self.Refresh()

    def SetSelection(self, index: int) -> None:
        if index < 0 or index > len(self.contributions):
            self.parent.property = None
            self.log.debug(f"Set self.parent.property = None")
        else:
            self.parent.property = self.contributions[index]
            self.log.debug(f"Set self.parent.property = {self.parent.property.GetUUIDStr()}")
        self.parent.Refresh()

    def InitContribution(self, filename: str = None) -> Contribution:
        ctb = Contribution()
        if filename is None:
            ctb.Export()
            self.contributions.append(ctb)
            self.log.debug(f"Created new contribution {ctb.GetUUIDStr()}")
            self.DrawContributions()
        else:
            self.log.debug(f"Loading contribution: {filename}")
            ctb.Import(filename)
        return ctb

    def GetContributions(self):
        self.contributions = []
        if config.PATH_CURRENT_PROJECT is None:
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"
        for file in os.listdir(path):
            if os.path.isdir(path + "/" + file):
                ctb = Contribution()
                ctb.LoadInfo(file)
                self.contributions.append(ctb)
        self.log.debug(f"Got {len(self.contributions)} contributions")

    def DrawContributions(self):
        for index in range(len(self.contributions) + 1):
            try:
                dpg.delete_item(f"{self.Pre}_Contribution.{index}")
            except SystemError:
                pass
        if len(self.contributions) == 0:
            dpg.add_text(parent=self.Window, default_value="No contributions found!", tag=f"{self.Pre}_Contribution.0")
        else:
            index = 0
            for ctb in self.contributions:
                dpg.add_button(parent=self.Window, label=ctb.GetName(), tag=f"{self.Pre}_Contribution.{index}", callback=self.SelectCallback)
                index += 1

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[1])
        if index < 0 or index > len(self.contributions):
            return
        self.InitContribution(self.contributions[index].GetUUIDStr())
        self.SetSelection(index)

    def CreateCallback(self):
        self.InitContribution()
        self.SetSelection(len(self.contributions) - 1)

    def Refresh(self):
        self.GetContributions()
        self.DrawContributions()