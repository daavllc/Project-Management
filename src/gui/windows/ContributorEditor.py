import os
import dearpygui.dearpygui as dpg

from objects.contributor import Contributor
from objects.base_types.version import Version

import helpers as hp
import config.config as config

class ContributorEditor:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectProperty
        self.log = hp.Logger("PM.GUI.Windows.ContributorEditor", "gui.log")

    def DrawInfo(self):
        with dpg.group(parent=f"{self.parent.Pre}.Body.Contributor"):
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Group1", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Group1.Name", default_value="Contributor:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.Group1.NameInput", hint=self.parent.contributor.GetName(), width=150, on_enter=True, callback=self.SetName)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Group1.UUID", default_value=self.parent.contributor.GetUUIDStr())
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Group2", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Group2.Date", default_value="Start date:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.Group2.DateInput", hint=self.parent.contributor.GetDateStr(), width=80, on_enter=True, callback=self.SetDate)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Group2.URL", default_value="URL:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.Group2.URLInput", hint=self.parent.contributor.GetURL(), width=300, on_enter=True, callback=self.SetURL)
            dpg.add_separator(tag=f"{self.parent.Pre}.Body.Contributor.InfoSeparator")

    def Refresh(self):
        self.DrawInfo()

    def SetName(self, sender, app_data, user_data) -> None:
        self.parent.contributor.SetName(app_data)
        self.parent.contributor.SaveInfo()
        self.parent.Edited()

    def SetDate(self, sender, app_data, user_data) -> None:
        date = None
        try:
            date = app_data.split('-')
            date = hp.Date.Set(int(date[0]), int(date[1]), int(date[2]))
            self.parent.contributor.SetDate(date)
            self.parent.contributor.SaveInfo()
            self.parent.Edited()
        except IndexError:
            pass
        except ValueError:
            pass

    def SetURL(self, sender, app_data, user_data) -> None:
        self.parent.contributor.SetURL(app_data)
        self.parent.contributor.SaveInfo()
        self.parent.Edited()
