# Project-Management.gui.windows.ContributorExplorer - GUI explorer window for viewing project Contributors
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import os

import dearpygui.dearpygui as dpg

import helpers as hp
import config.config as config
import gui.utils as utils

from objects.contributor import Contributor

class ContributorExplorer:
    def __init__(self, parent, manager):
        self.parent = parent # gui.gui.windows.ProjectViewer
        self.manager = manager # manager.contributior.ContributorManager
        self.contributors: list[Contributor] = []
        self.show: list[bool] = []
        self.log = hp.Logger("PM.GUI.Windows.ContributorExplorer", "gui.log")

        self.Window = "ContributorExplorer"
        self.Pre = "ctrX"

        with dpg.window(tag=self.Window, label="Project Contributors", no_close=True):
            with dpg.group(parent=self.Window, tag=f"{self.Pre}.Header"):
                dpg.add_input_text(parent=self.Window, tag=f"{self.Pre}.Header.Search", hint="Search", callback=self.SearchCallback)
            dpg.add_separator(parent=self.Window, tag=f"{self.Pre}.Header.Separator")
            self.Refresh()

    def SetSelection(self, index: int):
        self.manager.Select(index)

    def SyncShow(self) -> None:
        self.show = [True for name in self.manager.GetNames()]

    def DrawContributors(self):
        utils.DeleteItems(f"{self.Pre}.Contributors")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Contributors"):
            total = len(self.manager.GetNames())
            if not self.manager.HasProject():
                dpg.add_text(tag=f"{self.Pre}.Contributors.NoProject", default_value="No project selected")
            elif total == 0:
                dpg.add_text(tag=f"{self.Pre}.Contributors.NoneFound", default_value="No contributors found!")
            else:
                if total == 1:
                    dpg.add_text(tag=f"{self.Pre}.Contributors.Total", default_value=f"{total} contributor found")
                else:
                    dpg.add_text(tag=f"{self.Pre}.Contributors.Total", default_value=f"{len(self.contributors)} contributors found")
                for idx, name in enumerate(self.manager.GetNames()):
                    if self.show[idx] is True:
                        dpg.add_button(tag=f"{self.Pre}.Contributors.Ctr.{idx}", label=name, callback=self.SelectCallback)

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[-1])
        self.SetSelection(index)

    def CreateCallback(self):
        self.manager.Create()
        self.show.append(True)
        self.DrawContributors()
        #self.parent.Refresh() # TODO: implement updating Project Header because 'Lead' combo

    def SearchCallback(self, sender, app_data, user_data) -> None:
        if app_data == '' or app_data is None:
            self.show = [True for _ in self.show]
        else:
            for idx, name in enumerate(self.manager.GetNames()):
                if name.startswith(app_data):
                    self.show[idx] = True
                else:
                    self.show[idx] = False
        self.DrawContributors()

    def Refresh(self):
        self.SyncShow()
        self.DrawContributors()

    def GetCtr(self, name: str) -> Contributor:
        return self.manager.GetByName(name)
