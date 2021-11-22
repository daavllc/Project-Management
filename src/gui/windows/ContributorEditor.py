import datetime as dt
import os
import dearpygui.dearpygui as dpg

from objects.contributor import Contributor
from objects.base_types.version import Version

import helpers as hp
import config.config as config

class PushDetails:
    contribution = None
    hours: float = None
    date: dt.date = dt.date.today()
    description: str = "Description"
class ContributorEditor:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectProperty
        self.log = hp.Logger("PM.GUI.Windows.ContributorEditor", "gui.log")

        self.PushDetails = PushDetails()

    def DrawInfo(self):
        with dpg.group(parent=f"{self.parent.Pre}.Body.Contributor"):
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Info.1", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Info.1.Name", default_value="Contributor:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.1Info..NameInput", hint=self.parent.contributor.GetName(), width=150, on_enter=True, callback=self.SetName)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.1Info..UUID", default_value=self.parent.contributor.GetUUIDStr())
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Info.2", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Info.2.Date", default_value="Start date:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.Info.2.DateInput", hint=self.parent.contributor.GetDateStr(), width=80, on_enter=True, callback=self.SetDate)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Info.2.URL", default_value="URL:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.Info.2.URLInput", hint=self.parent.contributor.GetURL(), width=300, on_enter=True, callback=self.SetURL)
            
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contributor.Info.SpacerTop", width=2)
            dpg.add_separator(tag=f"{self.parent.Pre}.Body.Contributor.Info.Separator")
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contributor.Info.SpacerBottom", width=2)

            with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Generated", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Generated.1", default_value=f"{self.parent.contributor.GetTotalAdditions()} additions over {self.parent.contributor.GetTotalHours()} hours.")
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Generated.2", default_value=f"Worked on {len(self.parent.contributor.GetWorkedContributions())} contributions")

            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contributor.Generated.SpacerTop", width=2)
            dpg.add_separator(tag=f"{self.parent.Pre}.Body.Contributor.Generated.Separator")
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contributor.Generated.SpacerBottom", width=2)

            with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Update.1", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.Commit", default_value="Commit:")
                dpg.add_combo(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.Ctb", width=150, items=[ctb.GetTitle() for ctb in self.parent.ContributionExplorer.contributions], callback=self.PushContribution)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.Hours", default_value="Hours: ")
                dpg.add_drag_float(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.HoursInput", default_value=0.0, width=40, min_value=0.0, speed=0.25, format='%0.2f',callback=self.PushHours)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.Date", default_value="Date:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.DateInput", hint=f"{str(self.PushDetails.date)}", width=80, on_enter=True, callback=self.PushDate)
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.DescriptionInput", hint=self.PushDetails.description, width=300, callback=self.PushDescription)
                dpg.add_button(tag=f"{self.parent.Pre}.Body.Contributor.Update.1.Push", label="Push", callback=self.Push)

            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contributor.Update.SpacerTop", width=2)
            dpg.add_separator(tag=f"{self.parent.Pre}.Body.Contributor.Update.Separator")
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contributor.Update.SpacerBottom", width=2)

            with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Viewer"):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Viewer.Title", default_value="Contribution Explorer")
                if self.parent.contributor.GetTotalAdditions() == 0:
                    dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Viewer.NoCtbs", default_value="No contribution additions found")
                else:
                    with dpg.group(tag=f"{self.parent.Pre}.Body.Contributor.Viewer.Ctb"):
                        for idx, cID in enumerate(self.parent.contributor.GetWorkedContributions()):
                            ctb = None
                            for c in self.parent.ContributionExplorer.contributions:
                                if c.GetUUID() == cID:
                                    ctb = c
                                    break
                            else:
                                continue
                            with dpg.tree_node(tag=f"{self.parent.Pre}.Body.Contributor.Viewer.Ctb.{idx}", label=ctb.GetTitle()):
                                for j, add in enumerate(self.parent.contributor.GetContributionInfo(cID)):
                                    with dpg.tree_node(tag=f"{self.parent.Pre}.Body.Contributor.Viewer.Ctb.{idx}.Addition.{j}", label=add[2]):
                                        dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Viewer.Ctb.{idx}.Addition.{j}.Hours", default_value=f"{add[0]} hours")
                                        dpg.add_text(tag=f"{self.parent.Pre}.Body.Contributor.Viewer.Ctb.{idx}.Addition.{j}.Date", default_value=f"{add[1]}")

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
            date = dt.date(int(date[0]), int(date[1]), int(date[2]))
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

    def Push(self, sender, app_data, user_data):
        if self.PushDetails.contribution is None:
            self.log.debug(f"No push because ctb")
            return
        elif self.PushDetails.hours is None:
            self.log.debug(f"No push because hours")
            return
        elif self.PushDetails.description == "Description":
            self.log.debug(f"No push because description")
            return
        else:
            self.parent.contributor.Push(self.PushDetails.hours, self.PushDetails.date, self.PushDetails.description, self.PushDetails.contribution)
            self.PushDetails = PushDetails()
            self.parent.contributor.Export()
            self.parent.Edited()

    def PushContribution(self, sender, app_data, user_data) -> None:
        ctb = self.parent.ContributionExplorer.GetCtb(app_data)
        self.PushDetails.contribution = ctb.GetUUID()

    def PushHours(self, sender, app_data, user_data):
        self.PushDetails.hours = app_data

    def PushDate(self, sender, app_data, user_data):
        date = None
        try:
            date = app_data.split('-')
            date = dt.date(int(date[0]), int(date[1]), int(date[2]))
            self.PushDetails.date = date
        except IndexError:
            pass
        except ValueError:
            pass

    def PushDescription(self, sender, app_data, user_data):
        self.PushDetails.description = app_data
