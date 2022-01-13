# Project-Management.gui.windows.ContributionExplorer - GUI explorer window for viewing project contributions
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import os

import dearpygui.dearpygui as dpg

import helpers as hp
import config.config as config
import gui.utils as utils

from objects.contribution import Contribution

class ContributionExplorer:
    def __init__(self, parent, manager):
        self.parent = parent # gui.gui.windows.ProjectProperty
        self.manager = manager # manager.contribution.ContributionManager
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
        self.manager.Select(index)
        #self.parent.SetContribution(self.contributions[index])

    def SyncShow(self) -> None:
        self.show = [True for title in self.manager.GetTitles()]

    def DrawContributions(self):
        utils.DeleteItems(f"{self.Pre}.Contributions")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Contributions"):
            if not self.manager.HasProject():
                dpg.add_text(tag=f"{self.Pre}.Contributions.NoProject", default_value="No project selected")
                return
            total = len(self.manager.GetTitles())
            if total == 0:
                dpg.add_text(tag=f"{self.Pre}.Contributions.NoneFound", default_value="No contributions found!")
            else:
                if total == 1:
                    dpg.add_text(tag=f"{self.Pre}.Contributions.Total", default_value=f"{total} contribution found")
                else:
                    dpg.add_text(tag=f"{self.Pre}.Contributions.Total", default_value=f"{total} contributions found")
                for idx, title in enumerate(self.manager.GetTitles()):
                    if self.show[idx] is True:
                        dpg.add_button(tag=f"{self.Pre}.Contributions.Ctr.{idx}", label=title, callback=self.SelectCallback)

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[-1])
        self.SetSelection(index)

    def CreateCallback(self):
        self.manager.Create()
        self.show.append(True)
        self.DrawContributions()

    def SearchCallback(self, sender, app_data, user_data) -> None:
        if app_data == '' or app_data is None:
            self.show = [True for _ in self.show]
        else:
            for idx, title in enumerate(self.manager.GetTitles()):
                if title.startswith(app_data):
                    self.show[idx] = True
                else:
                    self.show[idx] = False
        self.DrawContributions()

    def Refresh(self):
        self.SyncShow()
        self.DrawContributions()

    def GetCtb(self, name: str) -> Contribution:
        return self.manager.GetByName(name)