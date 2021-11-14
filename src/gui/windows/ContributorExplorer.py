# Project-Management.gui.windows.ContributorExplorer - GUI explorer window for viewing project Contributors
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os

import dearpygui.dearpygui as dpg

from gui.logger import Logger
import config.config as config

from common_types.contributor import Contributor

class ContributorExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectViewer
        self.contributors = []
        self.log = Logger("PM.Window.ContributorExplorer")

        self.Window = "ContributorExplorer"
        self.Pre = "ctrX"

        with dpg.window(tag=self.Window, label="Contributor Explorer", no_close=True):
            self.Refresh()

    def SetSelection(self, index: int):
        if index < 0 or index > len(self.contributors):
            self.parent.property = None
            self.log.debug(f"Set self.parent.property = None")
        else:
            self.parent.property = self.contributors[index]
            self.log.debug(f"Set self.parent.property = {self.parent.property.GetUUIDStr()}")
        self.parent.Refresh()

    def InitContributor(self, filename: str = None) -> Contributor:
        ctr = Contributor()
        if filename is None:
            ctr.Export()
            self.contributors.append(ctr)
            self.log.debug(f"Created new contributor {ctr.GetUUIDStr()}")
            self.DrawContributors()
        else:
            self.log.debug(f"Loading contributor: {filename}")
            ctr.Import(filename)
        return ctr

    def GetContributors(self):
        self.contributors = []
        if config.PATH_CURRENT_PROJECT is None:
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}"
        for file in os.listdir(path):
            if os.path.isdir(path + "/" + file):
                ctr = Contributor()
                ctr.LoadInfo(file)
                self.contributors.append(ctr)
        self.log.debug(f"Got {len(self.contributors)} contributors")

    def DrawContributors(self):
        for index in range(len(self.contributors) + 1):
            try:
                dpg.delete_item(f"{self.Pre}_Contributors.{index}")
            except SystemError:
                pass
        if len(self.contributors) == 0:
            dpg.add_text(parent=self.Window, default_value="No contributors found!", tag=f"{self.Pre}_Contributors.0")
        else:
            index = 0
            for ctr in self.contributors:
                dpg.add_button(parent=self.Window, label=ctr.GetName(), tag=f"{self.Pre}_Contributors.{index}", callback=self.SelectCallback)
                index += 1

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[1])
        if index < 0 or index > len(self.contributors):
            return
        self.InitContributor(self.contributors[index].GetUUIDStr())
        self.SetSelection(index)

    def CreateCallback(self):
        self.InitContributor()
        self.SetSelection(len(self.contributors) - 1)

    def Refresh(self):
        self.GetContributors()
        self.DrawContributors()
