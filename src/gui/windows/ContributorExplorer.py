# Project-Management.gui.windows.ContributorExplorer - GUI explorer window for viewing project Contributors
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os

import dearpygui.dearpygui as dpg

import helpers as hp
import config.config as config
import gui.utils as utils

from objects.contributor import Contributor

class ContributorExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectViewer
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
        if index < 0 or index > len(self.contributors):
            self.parent.SetContributor(None)
        else:
            self.parent.SetContributor(self.contributors[index])

    def InitContributor(self, filename: str = None) -> Contributor:
        ctr = Contributor()
        if filename is None:
            ctr.Export()
            self.contributors.append(ctr)
            self.log.debug(f"Created new contributor {ctr.GetUUIDStr()}")
            self.DrawContributors()
        else:
            self.log.debug(f"Loading contributor: {filename}")
            ctr.LoadInfo(filename)
        return ctr

    def GetContributors(self):
        self.contributors = []
        if config.PATH_CURRENT_PROJECT is None:
            return
        self.contributors = self.parent.parent.project.GetContributors()
        self.show = [True for _ in self.contributors]
        self.log.debug(f"Found {len(self.contributors)} contributor(s): {[ctr.GetName() for ctr in self.contributors]}")

    def DrawContributors(self):
        utils.DeleteItems(f"{self.Pre}.Contributors")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Contributors"):
            if self.parent.parent.project is None:
                dpg.add_text(tag=f"{self.Pre}.Contributors.NoProject", default_value="No project selected")
            elif len(self.contributors) == 0:
                dpg.add_text(tag=f"{self.Pre}.Contributors.NoneFound", default_value="No contributors found!")
            else:
                total = len(self.contributors)
                if total == 1:
                    dpg.add_text(tag=f"{self.Pre}.Contributors.Total", default_value=f"{len(self.contributors)} total contributor")
                else:
                    dpg.add_text(tag=f"{self.Pre}.Contributors.Total", default_value=f"{len(self.contributors)} total contributors")
                for idx, ctr in enumerate(self.contributors):
                    if self.show[idx] is True:
                        dpg.add_button(tag=f"{self.Pre}.Contributors.Ctr.{idx}", label=ctr.GetName(), callback=self.SelectCallback)

    def SelectCallback(self, sender, app_data, user_data) -> None:
        index = int(sender.split('.')[-1])
        if index < 0 or index > len(self.contributors):
            return
        self.contributors[index].Import(self.contributors[index].GetUUIDStr())
        self.SetSelection(index)

    def CreateCallback(self):
        ctr = self.parent.parent.project.AddContributor()
        self.contributors.append(ctr)
        self.show.append(True)
        self.DrawContributors()

        self.SetSelection(len(self.contributors) - 1)

    def SearchCallback(self, sender, app_data, user_data) -> None:
        if app_data == '' or app_data is None:
            self.show = [True for _ in self.show]
        else:
            for idx, ctr in enumerate(self.contributors):
                if ctr.GetName().startswith(app_data):
                    self.show[idx] = True
                else:
                    self.show[idx] = False
        self.DrawContributions()

    def Refresh(self):
        self.GetContributors()
        self.DrawContributors()

    def GetCtr(self, name: str) -> Contributor:
        for ctr in self.contributors:
            if ctr.GetName() == name:
                return ctr
