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
        self.show: list[bool] = []
        self.log = hp.Logger("PM.GUI.Windows.ContributionExplorer", "gui.log")

        self.Window: str = "ContributionExplorer"
        self.Pre: str = "ctbX"

        with dpg.window(tag=self.Window, label="Project Contributions", no_close=True):
            with dpg.group(parent=self.Window, tag=f"{self.Pre}.Header"):
                dpg.add_input_text(parent=self.Window, tag=f"{self.Pre}.Header.Search", hint="Search", callback=self.SearchCallback)
            dpg.add_separator(parent=self.Window, tag=f"{self.Pre}.Header.Separator")
            self.Refresh()

    def SetSelection(self, index: int) -> None:
        self.parent.SetContribution(self.contributions[index])

    def GetContributions(self):
        self.contributions = []
        if config.PATH_CURRENT_PROJECT is None:
            return
        self.contributions = self.parent.parent.project.GetContributions()
        self.show = [True for _ in self.contributions]
        self.log.debug(f"Found {len(self.contributions)} contribution(s): {[ctb.GetName() for ctb in self.contributions]}")

    def DrawContributions(self):
        utils.DeleteItems(f"{self.Pre}.Contributions")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Contributions"):
            if self.parent.parent.project is None:
                dpg.add_text(tag=f"{self.Pre}.Contributions.NoProject", default_value="No project selected")
            elif len(self.contributions) == 0:
                dpg.add_text(tag=f"{self.Pre}.Contributions.NoneFound", default_value="No contributions found!")
            else:
                total = len(self.contributions)
                if total == 1:
                    dpg.add_text(tag=f"{self.Pre}.Contributions.Total", default_value=f"{len(self.contributions)} total contribution")
                else:
                    dpg.add_text(tag=f"{self.Pre}.Contributions.Total", default_value=f"{len(self.contributions)} total contributions")
                for idx, ctb in enumerate(self.contributions):
                    if self.show[idx] is True:
                        dpg.add_button(tag=f"{self.Pre}.Contributions.Ctr.{idx}", label=ctb.GetTitle(), callback=self.SelectCallback)

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[-1])
        self.contributions[index].Import(self.contributions[index].GetUUIDStr())
        self.SetSelection(index)

    def CreateCallback(self):
        ctb = self.parent.parent.project.AddContribution()
        self.contributions.append(ctb)
        self.show.append(True)
        self.DrawContributions()

        self.SetSelection(len(self.contributions) - 1)

    def SearchCallback(self, sender, app_data, user_data) -> None:
        if app_data == '' or app_data is None:
            self.show = [True for _ in self.show]
        else:
            for idx, ctb in enumerate(self.contributions):
                if ctb.GetName().startswith(app_data):
                    self.show[idx] = True
                else:
                    self.show[idx] = False
        self.DrawContributions()

    def Refresh(self):
        self.GetContributions()
        self.DrawContributions()

    def GetCtb(self, name: str) -> Contribution:
        for ctb in self.contributions:
            if ctb.GetTitle() == name:
                return ctb