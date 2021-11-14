# Project-Management.gui.windows.PropertyEditor - GUI window for editing project properties (contributions and contributors)
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import datetime
import os
import dearpygui.dearpygui as dpg

from common_types.contribution import Contribution
from common_types.contributor import Contributor
from common_types.base_types.version import Version

from gui.logger import Logger
import config.config as config

from .ContributionExplorer import ContributionExplorer
from .ContributorExplorer import ContributorExplorer


class PropertyEditor:
    def __init__(self, parent):
        self.parent = parent # gui.gui.ProjectProperty
        self.log = Logger("PM.Window.PropertyEditor")
        self.editor = None

        self.Window = "PropertyEditor"
        self.Pre = "pE"

        with dpg.window(tag=self.Window, label="Property Editor", no_close=True):
            self.Refresh()

    def CheckProperty(self):
        if self.editor is None:
            try:
                dpg.delete_item(f"{self.Pre}_NoProperty")
            except SystemError:
                pass
        else:
            for name in self.editor.GetTags():
                try:
                    dpg.delete_item(f"{self.Pre}{name}")
                except SystemError:
                    pass
        if type(self.parent.property) == Contribution:
            self.editor = ContributionEditor(self)
        elif type(self.parent.property) == Contributor:
            self.editor = ContributorEditor(self)
        else:
            self.editor = None

    def DrawProperty(self):
        if self.editor is None:
            dpg.add_text(parent=self.Window, default_value="No project property selected", tag=f"{self.Pre}_NoProperty")
            return
        self.editor.Refresh(self.parent.property)

    def Refresh(self):
        self.CheckProperty()
        self.DrawProperty()

    def Edited(self):
        self.parent.Refresh()

    def InitContribution(self, filename: str = None) -> None:
        ctb = Contribution()
        if filename is None:
            ctb.Export()
            self.parent.property = ctb
            self.log.debug(f"Created new contribution {ctb.GetUUIDStr()}")
        else:
            ctb.Import(filename)
            self.parent.property = ctb
            self.log.debug(f"Loaded contribution {ctb.GetUUIDStr()}")
        self.parent.Refresh()

    def InitContributor(self, filename: str = None):
        ctr = Contributor()
        if filename is None:
            ctr.Export()
            self.parent.property = ctr
            self.log.debug(f"Created new contribution {ctr.GetUUIDStr()}")
        else:
            ctr.Import(filename)
            self.parent.property = ctr
            self.log.debug(f"Loaded contribution {ctr.GetUUIDStr()}")
        self.parent.Refresh()

class ContributionEditor:
    def __init__(self, parent):
        self.parent= parent
        self.Window = parent.Window
        self.Pre = parent.Pre
        self.prop = None
    
    def GetTags(self) -> list[str]:
        return ["_HGContribution", "_HGNameInput", "_HGNumber", "_Group1",
                "_HGDate", "_HGDateInput", "_HGVersion", "_HGVersionInput", "_HGLead", "_HGLeadInput", "_Group2"]

    def Draw(self):
        for name in self.GetTags():
            try:
                dpg.delete_item(f"{self.Pre}{name}")
            except SystemError:
                pass
        with dpg.group(parent=self.Window, tag=f"{self.Pre}_Group1", horizontal=True):
            dpg.add_text(default_value="Contribution:", tag=f"{self.Pre}_HGContribution")
            dpg.add_input_text(tag=f"{self.Pre}_HGNameInput", hint=self.prop.GetName(), width=150, on_enter=True, callback=self.SetName)
            dpg.add_text(default_value=f"Number: {self.prop.GetNumberStr()}", tag=f"{self.Pre}_HGNumber")
        with dpg.group(parent=self.Window, tag=f"{self.Pre}_Group2", horizontal=True):
            dpg.add_text(default_value="Creation date:", tag=f"{self.Pre}_HGDate")
            dpg.add_input_text(tag=f"{self.Pre}_HGDateInput", hint=self.prop.GetDateStr(), width=80, on_enter=True, callback=self.SetDate)
            dpg.add_text(default_value="Version change:", tag=f"{self.Pre}_HGVersion")
            dpg.add_input_text(tag=f"{self.Pre}_HGVersionInput", hint=self.prop.GetVersionChangeStr(), width=80, on_enter=True, callback=self.SetVersion)
            dpg.add_text(default_value="Lead:", tag=f"{self.Pre}_HGLead")
            dpg.add_input_text(tag=f"{self.Pre}_HGLeadInput", hint=self.prop.GetLead(), width=80, on_enter=True, callback=self.SetLead)


    def SetName(self, sender, app_data, user_data) -> None:
        self.prop.SetName(app_data)
        self.prop.Export()
        self.parent.Edited()

    def SetDate(self, sender, app_data, user_data) -> None:
        date = None
        try:
            date = app_data.split('-')
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            self.prop.SetDate(date)
            self.prop.Export()
            self.parent.Edited()
        except IndexError:
            pass
        except ValueError:
            pass

    def SetVersion(self, sender, app_data, user_data) -> None:
        try:
            self.prop.SetVersionChange(Version(app_data))
            self.prop.Export()
            self.parent.Edited()
        except Version.Errors.InvalidInitializationArgs:
            pass
        except Version.Errors.InvalidVersionString:
            pass

    def SetLead(self, sender, app_data, user_data) -> None:
        self.prop.SetLead(app_data)
        self.prop.Export()
        self.parent.Edited()

    def Refresh(self, prop: Contribution):
        self.prop = prop
        self.Draw()

class ContributorEditor:
    def __init__(self, parent):
        self.parent= parent
        self.Window = parent.Window
        self.Pre = parent.Pre
        self.prop = None
    
    def GetTags(self) -> list[str]:
        return ["_HGContributor", "_HGNameInput", "_HGurl", "_HGUrlInput", "_Group1", 
                "_HGDate", "_HGDateInput", "_Group2"]

    def Draw(self):
        for name in self.GetTags():
            try:
                dpg.delete_item(f"{self.Pre}{name}")
            except SystemError:
                pass
        with dpg.group(parent=self.Window, tag=f"{self.Pre}_Group1", horizontal=True):
            dpg.add_text(default_value="Contributor:", tag=f"{self.Pre}_HGContributor")
            dpg.add_input_text(tag=f"{self.Pre}_HGNameInput", hint=self.prop.GetName(), width=150, on_enter=True, callback=self.SetName)
            dpg.add_text(default_value="URL:", tag=f"{self.Pre}_HGurl")
            dpg.add_input_text(tag=f"{self.Pre}_HGUrlInput", hint=self.prop.GetURL(), width=300, on_enter=True, callback=self.SetURL)
        with dpg.group(parent=self.Window, tag=f"{self.Pre}_Group2", horizontal=True):
            dpg.add_text(default_value="Creation date:", tag=f"{self.Pre}_HGDate")
            dpg.add_input_text(tag=f"{self.Pre}_HGDateInput", hint=self.prop.GetDateStr(), width=80, on_enter=True, callback=self.SetDate)

    def SetName(self, sender, app_data, user_data) -> None:
        self.prop.SetName(app_data)
        self.prop.Export()
        self.parent.Edited()

    def SetURL(self, sender, app_data, user_data) -> None:
        self.prop.SetURL(app_data)
        self.prop.Export()
        self.parent.Edited()

    def SetDate(self, sender, app_data, user_data) -> None:
        date = None
        try:
            date = app_data.split('-')
            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            self.prop.SetDate(date)
            self.prop.Export()
            self.parent.Edited()
        except IndexError:
            pass
        except ValueError:
            pass
    def Refresh(self, prop: Contributor):
        self.prop = prop
        self.Draw()