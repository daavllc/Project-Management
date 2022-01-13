# Project-Management.gui.windows.ProjectProperty - GUI window for viewing/editing project properties (the header, contributions and contributors)
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import datetime as dt
import os
import dearpygui.dearpygui as dpg

import helpers as hp
import config.config as config
import gui.utils as utils

from .ContributionExplorer import ContributionExplorer
from .ContributorExplorer import ContributorExplorer
from .ContributionEditor import ContributionEditor
from .ContributorEditor import ContributorEditor

class ProjectProperty:
    def __init__(self, parent, manager):
        self.parent = parent # gui.gui.windows.windows
        self.manager = manager # manager.project.ProjectManager
        self.log = hp.Logger("PM.GUI.Windows.ProjectPropertyExplorer", "gui.log")

        self.Window: str = "ProjectPropertyExplorer"
        self.Pre: str = "ppX"

        with dpg.window(tag=self.Window, label="Project Property Explorer", no_close=True):
            self.Refresh()

        self.width = dpg.get_item_width(self.Window)
        self.height = dpg.get_item_height(self.Window)

        self.ContributionExplorer = ContributionExplorer(self, self.manager.GetContributionManager())
        self.ContributionEditor = ContributionEditor(self, self.manager.GetContributionManager())

        self.ContributorExplorer = ContributorExplorer(self, self.manager.GetContributorManager())
        self.ContributorEditor = ContributorEditor(self, self.manager.GetContributorManager())

    def DrawHeader(self):
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Header"):
            if not self.manager.HasSelected():
                dpg.add_text(tag=f"{self.Pre}.Header.NotSelected", default_value="No project selected")
            else:
                with dpg.group(tag=f"{self.Pre}.Header.Group1", horizontal=True):
                    dpg.add_text(default_value="Project:", tag=f"{self.Pre}.Header.Group1.Project")
                    dpg.add_input_text(tag=f"{self.Pre}.Header.Group1.NameInput", hint=self.manager.GetSelected().GetName(), width=150, on_enter=True, callback=self.SetProjectName)
                    dpg.add_text(default_value=self.manager.GetSelected().GetUUIDStr(), tag=f"{self.Pre}.Header.Group1.ProjectUUID")
                    dpg.add_button(tag=f"{self.Pre}.Header.Group1.AddCtb", label="Add Contribution", callback=self.AddCtb)
                    dpg.add_button(tag=f"{self.Pre}.Header.Group1.AddCtr", label="Add Contributor", callback=self.AddCtr)
                with dpg.group(tag=f"{self.Pre}.Header.Group2", horizontal=True):
                    dpg.add_text(tag=f"{self.Pre}.Header.Group2.ProjectVersion", default_value=f"Version: {self.manager.GetSelected().GetVersionStr()},")
                    dpg.add_text(tag=f"{self.Pre}.Header.Group2.ProjectDate", default_value="Creation date:")
                    dpg.add_input_text(tag=f"{self.Pre}.Header.Group2.DateInput", hint=self.manager.GetSelected().GetDateStr(), width=80, on_enter=True, callback=self.SetProjectDate)
                    dpg.add_text(tag=f"{self.Pre}.Header.Group2.Lead", default_value="Lead:")
                    dpg.add_combo(tag=f"{self.Pre}.Header.Group2.LeadCombo", width=150, default_value=self.manager.GetSelected().GetLeadName(), items=[name for name in self.manager.GetContributorNames()], callback=self.SetProjectLead)
                with dpg.group(tag=f"{self.Pre}.Header.Group3", horizontal=True):
                    dpg.add_text(tag=f"{self.Pre}.Header.Group3.Description", default_value="Description:")
                    dpg.add_input_text(tag=f"{self.Pre}.Header.Group3.DescriptionInput", hint=self.manager.GetSelected().GetDescription(), width=700, on_enter=True, callback=self.SetProjectDescription)
            dpg.add_spacer(tag=f"{self.Pre}.Header.SpacerTop", height=2)
            dpg.add_separator(tag=f"{self.Pre}.Header.Separator")
            dpg.add_spacer(tag=f"{self.Pre}.Header.SpacerBottom", height=2)

    def DrawBody(self):
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Body"):
            if self.manager.HasSelectedProperty():
                dpg.add_text(tag=f"{self.Pre}.Body.NotSelected", default_value="No project property selected")
                return
            elif self.manager.HasContributionSelected():
                self.ContributionEditor.Refresh()
            elif self.manager.HasContributorSelected():
                self.ContributorEditor.Refresh()

    def GetSize(self):
        self.width = dpg.get_item_width(self.Window)
        self.height = dpg.get_item_height(self.Window)
        return [self.width, self.height]

    def AddCtb(self):
        self.ContributionExplorer.CreateCallback()
        self.manager.SetUnsaved()
        self.parent.SyncProject()

    def AddCtr(self):
        self.ContributorExplorer.CreateCallback()
        self.manager.SetUnsaved()
        self.parent.SyncProject()

    def SetContribution(self, ctb):
        self.Refresh()

    def SetContributor(self, ctr):
        return
        self.contributor = ctr
        self.log.debug(f"Set self.contributor = {self.contributor.GetName()}")
        self.contribution = None
        self.Refresh()

    def Edited(self):
        return
        self.ContributionExplorer.Refresh()
        self.ContributorExplorer.Refresh()
        utils.DeleteItems(f"{self.Pre}.Body")
        self.DrawBody()

    def Refresh(self):
        utils.DeleteItems(f"{self.Pre}.Header")
        utils.DeleteItems(f"{self.Pre}.Body")
        self.DrawHeader()
        self.DrawBody()

    def RefreshAll(self):
        self.Refresh()
        self.ContributionExplorer.Refresh()
        self.ContributorExplorer.Refresh()

    def SetProjectName(self, sender, app_data, user_data):
        self.manager.SetName(app_data)
        self.parent.Refresh()

    def SetProjectDate(self, sender, app_data, user_data):
        try:
            date = app_data.split('-')
            date = dt.date(int(date[0]), int(date[1]), int(date[2]))
            self.manager.SetDate(date)
            self.parent.Refresh()
        except IndexError:
            pass
        except ValueError:
            pass

    def SetProjectLead(self, sender, app_data, user_data):
        self.manager.SetLead(app_data)
        self.parent.Refresh()

    def SetProjectDescription(self, sender, app_data, user_data):
        self.manager.SetDescription(app_data)
        self.parent.Refresh()
