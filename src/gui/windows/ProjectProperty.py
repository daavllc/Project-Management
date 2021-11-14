# Project-Management.gui.windows.ProjectProperty - GUI window for viewing/editing project properties (the header, contributions and contributors)
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import datetime
import os
import dearpygui.dearpygui as dpg

from gui.logger import Logger
import config.config as config
from .PropertyEditor import PropertyEditor
from .ContributionExplorer import ContributionExplorer
from .ContributorExplorer import ContributorExplorer

class ProjectPropertyExplorer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.ProjectExplorer
        self.property = None # either Contribution or Contributor
        self.log = Logger("PM.Window.ProjectPropertyExplorer")

        self.Window = "ProjectPropertyExplorer"
        self.Pre = "ppX"

        with dpg.window(tag=self.Window, label="Project Property Explorer", no_close=True, autosize=True):
            self.ContributionExplorer = ContributionExplorer(self)
            self.ContributorExplorer = ContributorExplorer(self)
            self.PropertyEditor = PropertyEditor(self)
            self.Refresh()


    def DrawHeader(self):
        for name in ["_NoProject", "_HGProject", "_HGNameInput", "_HGAddCtb", "_HGAddCtr", "_HeaderGroup1",
                      "_HGProjectVersion", "_HGProjectDate", "_HGDateInput", "_HGProjectLead", "_HGLeadInput", "_HeaderGroup2", 
                      "_HeaderDescription", "_HeaderDescriptionInput", "_HeaderGroup3"]:
            try:
                dpg.delete_item(f"{self.Pre}{name}")
            except SystemError:
                pass
        if self.parent.project is None:
            dpg.add_text(parent=self.Window, default_value="No project selected", tag=f"{self.Pre}_NoProject")
            return
        with dpg.group(parent=self.Window, tag=f"{self.Pre}_HeaderGroup1", horizontal=True):
            dpg.add_text(default_value="Project:", tag=f"{self.Pre}_HGProject")
            dpg.add_input_text(tag=f"{self.Pre}_HGNameInput", hint=self.parent.project.GetName(), width=150, on_enter=True, callback=self.SetProjectName)
            dpg.add_button(label="Add Contribution", callback=self.ContributionExplorer.CreateCallback, tag=f"{self.Pre}_HGAddCtb")
            dpg.add_button(label="Add Contributor", callback=self.ContributorExplorer.CreateCallback, tag=f"{self.Pre}_HGAddCtr")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}_HeaderGroup2", horizontal=True):
            dpg.add_text(default_value=f"Version: {self.parent.project.GetVersionStr()},", tag=f"{self.Pre}_HGProjectVersion")
            dpg.add_text(default_value="Creation date:", tag=f"{self.Pre}_HGProjectDate")
            dpg.add_input_text(tag=f"{self.Pre}_HGDateInput", hint=self.parent.project.GetDateStr(), width=80, on_enter=True, callback=self.SetProjectDate)
            dpg.add_text(default_value="Lead:", tag=f"{self.Pre}_HGProjectLead")
            dpg.add_input_text(tag=f"{self.Pre}_HGLeadInput", hint=self.parent.project.GetLead(), width=80, on_enter=True, callback=self.SetProjectLead)
        with dpg.group(parent=self.Window, tag=f"{self.Pre}_HeaderGroup3", horizontal=True):
            dpg.add_text(default_value="Description:", tag=f"{self.Pre}_HeaderDescription")
            dpg.add_input_text(tag=f"{self.Pre}_HeaderDescriptionInput", hint=self.parent.project.GetDescription(), width=700, on_enter=True, callback=self.SetProjectDescription)

    def DrawProperty(self):
        self.PropertyEditor.Refresh()

    def Refresh(self):
        self.DrawHeader()
        self.DrawProperty()
        self.ContributionExplorer.Refresh()
        self.ContributorExplorer.Refresh()

    def SetProjectName(self, sender, app_data, user_data):
        self.parent.project.SetName(app_data)
        self.parent.project.Export()
        self.parent.Refresh()

    def SetProjectDate(self, sender, app_data, user_data):
        date = None
        try:
            date = app_data.split('-')
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
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
