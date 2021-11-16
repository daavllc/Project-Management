# Project-Management.gui.windows.ContributionExplorer - GUI explorer window for viewing project contributions
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os

import dearpygui.dearpygui as dpg

import helpers as hp
import config.config as config
import gui.utils as utils

from objects.contribution import Contribution

class ContributionExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectProperty
        self.contributions: list[Contribution] = []
        self.log = hp.Logger("PM.GUI.Windows.ContributionExplorer", "gui.log")

        self.Window: str = "ContributionExplorer"
        self.Pre: str = "ctbX"

        with dpg.window(tag=self.Window, label="Project Contributions", no_close=True):
            self.Refresh()

    def SetSelection(self, index: int) -> None:
        self.parent.SetContribution(self.contributions[index])

    def GetContributions(self):
        self.contributions = []
        if config.PATH_CURRENT_PROJECT is None:
            return
        self.contributions = self.parent.parent.project.GetContributions()
        self.log.debug(f"Found {len(self.contributions)} contribution(s): {[ctb.GetName() for ctb in self.contributions]}")

    def DrawContributions(self):
        utils.DeleteItems(f"{self.Pre}.Contributions")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Contributions"):
            if self.parent.parent.project is None:
                dpg.add_text(tag=f"{self.Pre}.Contributions.NoProject", default_value="No project selected")
            elif len(self.contributions) == 0:
                dpg.add_text(tag=f"{self.Pre}.Contributions.NoneFound", default_value="No contributions found!")
            else:
                index = 0
                for ctb in self.contributions:
                    dpg.add_button(tag=f"{self.Pre}.Contributions.Ctr.{index}", label=ctb.GetName(), callback=self.SelectCallback)
                    index += 1

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[-1])
        self.contributions[index].Import(self.contributions[index].GetUUIDStr())
        self.SetSelection(index)

    def CreateCallback(self):
        ctb = self.parent.parent.project.AddContribution()
        self.contributions.append(ctb)
        self.DrawContributions()

        self.SetSelection(len(self.contributions) - 1)

    def Refresh(self):
        self.GetContributions()
        self.DrawContributions()