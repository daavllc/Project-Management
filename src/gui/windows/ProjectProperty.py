# Project-Management.gui.windows.ProjectProperty - GUI window for viewing/editing project properties (the header, contributions and contributors)
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

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
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.windows
        self.contributor = None
        self.contribution = None
        self.log = hp.Logger("PM.GUI.Windows.ProjectPropertyExplorer", "gui.log")

        self.Window: str = "ProjectPropertyExplorer"
        self.Pre: str = "ppX"

        with dpg.window(tag=self.Window, label="Project Property Explorer", no_close=True):
            self.Refresh()

        self.width = dpg.get_item_width(self.Window)
        self.height = dpg.get_item_height(self.Window)

        self.ContributionExplorer = ContributionExplorer(self)
        self.ContributorExplorer = ContributorExplorer(self)
        self.ContributionEditor = ContributionEditor(self)
        self.ContributorEditor = ContributorEditor(self)

    def DrawHeader(self):
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Header"):
            if self.parent.project is None:
                dpg.add_text(tag=f"{self.Pre}.Header.NotSelected", default_value="No project selected")
            else:
                with dpg.group(tag=f"{self.Pre}.Header.Group1", horizontal=True):
                    dpg.add_text(default_value="Project:", tag=f"{self.Pre}.Header.Group1.Project")
                    dpg.add_input_text(tag=f"{self.Pre}.Header.Group1.NameInput", hint=self.parent.project.GetName(), width=150, on_enter=True, callback=self.SetProjectName)
                    dpg.add_text(default_value=self.parent.project.GetUUIDStr(), tag=f"{self.Pre}.Header.Group1.ProjectUUID")
                    dpg.add_button(tag=f"{self.Pre}.Header.Group1.AddCtb", label="Add Contribution", callback=self.ContributionExplorer.CreateCallback)
                    dpg.add_button(tag=f"{self.Pre}.Header.Group1.AddCtr", label="Add Contributor", callback=self.ContributorExplorer.CreateCallback)
                with dpg.group(tag=f"{self.Pre}.Header.Group2", horizontal=True):
                    dpg.add_text(tag=f"{self.Pre}.Header.Group2.ProjectVersion", default_value=f"Version: {self.parent.project.GetVersionStr()},")
                    dpg.add_text(tag=f"{self.Pre}.Header.Group2.ProjectDate", default_value="Creation date:")
                    dpg.add_input_text(tag=f"{self.Pre}.Header.Group2.DateInput", hint=self.parent.project.GetDateStr(), width=80, on_enter=True, callback=self.SetProjectDate)
                    dpg.add_text(tag=f"{self.Pre}.Header.Group2.ProjectLead", default_value="Lead:")
                    dpg.add_input_text(tag=f"{self.Pre}.Header.Group2.LeadInput", hint=self.parent.project.GetLead(), width=80, on_enter=True, callback=self.SetProjectLead)
                with dpg.group(tag=f"{self.Pre}.Header.Group3", horizontal=True):
                    dpg.add_text(tag=f"{self.Pre}.Header.Group3.Description", default_value="Description:")
                    dpg.add_input_text(tag=f"{self.Pre}.Header.Group3.DescriptionInput", hint=self.parent.project.GetDescription(), width=700, on_enter=True, callback=self.SetProjectDescription)
            dpg.add_spacer(tag=f"{self.Pre}.Header.SpacerTop", height=2)
            dpg.add_separator(tag=f"{self.Pre}.Header.Separator")
            dpg.add_spacer(tag=f"{self.Pre}.Header.SpacerBottom", height=2)

    def DrawBody(self):
        with dpg.group(parent=self.Window, tag=f"{self.Pre}.Body"):
            if self.contribution is None and self.contributor is None:
                dpg.add_text(tag=f"{self.Pre}.Body.NotSelected", default_value="No project property selected")
                return
            elif not self.contribution is None:
                self.ContributionEditor.Refresh()
            elif not self.contributor is None:
                self.ContributorEditor.Refresh()

    def GetSize(self):
        self.width = dpg.get_item_width(self.Window)
        self.height = dpg.get_item_height(self.Window)
        return [self.width, self.height]

    def SetContribution(self, ctb):
        self.contribution = ctb
        self.log.debug(f"Set self.contribution = {self.contribution.GetName()}")
        self.contributor = None
        self.Refresh()

    def SetContributor(self, ctr):
        self.contributor = ctr
        self.log.debug(f"Set self.contributor = {self.contributor.GetName()}")
        self.contribution = None
        self.Refresh()

    def Edited(self):
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
        self.parent.project.SetName(app_data)
        self.parent.project.Export()
        self.parent.Refresh()

    def SetProjectDate(self, sender, app_data, user_data):
        try:
            date = app_data.split('-')
            date = hp.Date.Set(int(date[0]), int(date[1]), int(date[2]))
            self.log.info(f"Set date to {date} from input {app_data}")
            self.parent.project.SetDate(date)
            self.parent.project.Export()
            self.parent.Refresh()
        except IndexError:
            pass
        except ValueError:
            pass

    def SetProjectLead(self, sender, app_data, user_data):
        self.parent.project.SetLead(app_data)
        self.parent.project.Export()
        self.parent.Refresh()

    def SetProjectDescription(self, sender, app_data, user_data):
        self.parent.project.SetDescription(app_data)
        self.parent.project.Export()
        self.parent.Refresh()
