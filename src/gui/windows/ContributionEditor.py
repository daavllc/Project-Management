import datetime as dt
import os
import dearpygui.dearpygui as dpg

from objects.contribution import Contribution
from objects.base_types.version import Version

import helpers as hp
import config.config as config
import gui.utils as utils

class PushDetails:
    contributor = None
    hours: float = None
    date: dt.date = dt.date.today()
    description: str = "Description"

class ProgressDetails:
    progress: float = None
    date: dt.date = dt.date.today()

class ContributionEditor:
    def __init__(self, parent):
        self.parent = parent # gui.gui.windows.ProjectProperty
        self.log = hp.Logger("PM.GUI.Windows.ContributionEditor", "gui.log")

        self.PushDetails = PushDetails()
        self.ProgressDetails = ProgressDetails()

    def DrawInfo(self):
        with dpg.group(parent=f"{self.parent.Pre}.Body.Contribution"):
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Info.1", horizontal=True):
                dpg.add_text(default_value="Contribution:", tag=f"{self.parent.Pre}.Body.Contribution.Info.1.Name")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.1.NameInput", hint=self.parent.contribution.GetName(), width=150, on_enter=True, callback=self.SetName)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.1.Number", default_value=f"Number: {self.parent.contribution.GetNumberStr()}")
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.1.UUID", default_value=self.parent.contribution.GetUUIDStr())
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Info.2", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.2.Date", default_value="Creation date:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.2.DateInput", hint=self.parent.contribution.GetDateStr(), width=80, on_enter=True, callback=self.SetDate)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.2.Lead", default_value="Lead:")
                dpg.add_combo(tag=f"{self.parent.Pre}.Body.Contribution.Info.2.Ctr", width=150, default_value=self.parent.contribution.GetLeadName(), items=[ctr.GetName() for ctr in self.parent.ContributorExplorer.contributors], callback=self.SetLead)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.2.VersionChange", default_value=f"Version change: ")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.2.VersionInput", hint=self.parent.contribution.GetVersionChangeStr(), width=80, on_enter=True, callback=self.SetVersionChange)
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Info.3", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.3.Description", default_value="Description:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.3.DescriptionInput", hint=self.parent.contribution.GetDescription(), width=700, on_enter=True, callback=self.SetDescription)
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Info.4", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.Commit", default_value="Commit:")
                dpg.add_combo(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.Ctr", width=150, items=[ctr.GetName() for ctr in self.parent.ContributorExplorer.contributors], callback=self.PushContributor)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.Hours", default_value="Hours: ")
                dpg.add_drag_float(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.HoursInput", default_value=0.0, width=40, min_value=0.0, speed=0.25, format='%0.2f',callback=self.PushHours)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.Date", default_value="Date:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.DateInput", hint=f"{str(self.PushDetails.date)}", width=80, on_enter=True, callback=self.PushDate)
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.DescriptionInput", hint=self.PushDetails.description, width=300, callback=self.PushDescription)
                dpg.add_button(tag=f"{self.parent.Pre}.Body.Contribution.Info.4.Push", label="Push", callback=self.Push)
            with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Info.5", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.5.Progress", default_value="Progress:")
                dpg.add_drag_float(tag=f"{self.parent.Pre}.Body.Contribution.Info.5.ProgressInput", default_value=0.0, width=40, min_value=0.0, max_value=100.0, speed=0.50, format='%0.2f',callback=self.ProgressValue)
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.5.Date", default_value="Date:")
                dpg.add_input_text(tag=f"{self.parent.Pre}.Body.Contribution.Info.5.DateInput", hint=f"{str(self.PushDetails.date)}", width=80, on_enter=True, callback=self.ProgressDate)
                dpg.add_button(tag=f"{self.parent.Pre}.Body.Contribution.Info.5.Update", label="Update", callback=self.UpdateProgress)
                
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contribution.InfoSpacerTop", width=2)
            dpg.add_separator(tag=f"{self.parent.Pre}.Body.Contribution.InfoSeparator")
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contribution.InfoSpacerBottom", width=2)

            with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Generated", horizontal=True):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Generated.Percent", default_value=f"{self.parent.contribution.GetTotalProgress():.2f}% complete")
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Generated.Contributors", default_value=f"over {self.parent.contribution.GetTotalHours():.1f} hours with {self.parent.contribution.GetTotalContributors()} contributors and {self.parent.contribution.GetTotalAdditions()} additions.")
            
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contribution.GeneratedSpacerTop", width=2)
            dpg.add_separator(tag=f"{self.parent.Pre}.Body.Contribution.GeneratedSeparator")
            dpg.add_spacer(tag=f"{self.parent.Pre}.Body.Contribution.GeneratedSpacerBottom", width=2)

            with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Viewer"):
                dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Title", default_value="Contributor Explorer")
                with dpg.group(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors"):
                    i = 0
                    for ctr in self.parent.contribution.GetContributors():
                        with dpg.tree_node(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors.Ctr.{i}", label=ctr.GetName()):
                            dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors.Ctr.{i}.Hours", default_value=f"Total hours: {ctr.GetTotalContributionHours(self.parent.contribution.GetUUID())}")
                            dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors.Ctr.{i}.LastDate", default_value=f"Last: {ctr.GetContributionLastDate(self.parent.contribution.GetUUID())}, First: {ctr.GetContributionFirstDate(self.parent.contribution.GetUUID())} ({ctr.GetContributionLastDate(self.parent.contribution.GetUUID()) - ctr.GetContributionFirstDate(self.parent.contribution.GetUUID())} days)")
                            with dpg.tree_node(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors.Ctr.{i}.Additons", label=f"{ctr.GetTotalContributionAdditions(self.parent.contribution.GetUUID())} additions"):
                                additions = ctr.GetContributionInfo(self.parent.contribution.GetUUID())
                                for j in range(len(additions)):
                                    with dpg.tree_node(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors.Ctr.{i}.Additons.{j}", label=f"{additions[j][2]}"):
                                        dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors.Ctr.{i}.Additions.{j}.Hours", default_value=f"{additions[j][0]} hours")
                                        dpg.add_text(tag=f"{self.parent.Pre}.Body.Contribution.Viewer.Contributors.Ctr.{i}.Additions.{j}.Date", default_value=f"{additions[j][1]}")
                        i += 1

    def HeaderSize(self):
        self.log.info(f"Header size: {str(self.parent.GetSize())}")
    def Refresh(self):
        self.DrawInfo()

    def SetName(self, sender, app_data, user_data) -> None:
        self.parent.contribution.SetName(app_data)
        self.parent.contribution.SaveInfo()
        self.parent.Edited()

    def SetDate(self, sender, app_data, user_data) -> None:
        date = None
        try:
            date = app_data.split('-')
            date = dt.date.Set(int(date[0]), int(date[1]), int(date[2]))
            self.parent.contribution.SetDate(date)
            self.parent.contribution.SaveInfo()
            self.parent.Edited()
        except IndexError:
            pass
        except ValueError:
            pass

    def SetLead(self, sender, app_data, user_data) -> None:
        ctr = self.parent.ContributorExplorer.GetCtr(app_data)
        self.parent.contribution.SetLead(ctr.GetUUID())
        self.parent.contribution.SaveInfo()
        self.parent.Edited()

    def SetVersionChange(self, sender, app_data, user_data) -> None:
        try:
            self.parent.contribution.SetVersionChange(Version(app_data))
            self.parent.contribution.SaveInfo()
            self.parent.parent.project.UpdateVersion(Version(app_data), self.parent.contribution.GetUUID())
            self.parent.Refresh()
        except Version.Errors.InvalidInitializationArgs:
            pass
        except Version.Errors.InvalidVersionString:
            pass

    def SetDescription(self, sender, app_data, user_data) -> None:
        self.parent.contribution.SetDescription(app_data)
        self.parent.contribution.SaveInfo()
        self.parent.Edited()

    def Push(self, sender, app_data, user_data):
        if self.PushDetails.contributor is None:
            self.log.debug(f"No push because ctr")
            return
        elif self.PushDetails.hours is None:
            self.log.debug(f"No push because hours")
            return
        elif self.PushDetails.description == "Description":
            self.log.debug(f"No push because description")
            return
        else:
            self.parent.contribution.Push(self.PushDetails.contributor.GetUUID(), self.PushDetails.hours, self.PushDetails.date, self.PushDetails.description)
            self.PushDetails = PushDetails()
            self.parent.contribution.Export()
            self.parent.Edited()

    def PushContributor(self, sender, app_data, user_data) -> None:
        ctr = self.parent.ContributorExplorer.GetCtr(app_data)
        self.PushDetails.contributor = ctr

    def PushHours(self, sender, app_data, user_data):
        self.PushDetails.hours = app_data

    def PushDate(self, sender, app_data, user_data):
        date = None
        try:
            date = app_data.split('-')
            date = dt.date.Set(int(date[0]), int(date[1]), int(date[2]))
            self.PushDetails.date = date
        except IndexError:
            pass
        except ValueError:
            pass

    def PushDescription(self, sender, app_data, user_data):
        self.PushDetails.description = app_data

    def UpdateProgress(self):
        if self.ProgressDetails is None or 0.0:
            return
        else:
            self.parent.contribution.UpdateProgress(self.ProgressDetails.progress, self.ProgressDetails.date)
            self.ProgressDetails = ProgressDetails()
            self.parent.contribution.Export()
            self.parent.Edited()

    def ProgressValue(self, sender, app_data, user_data):
        self.ProgressDetails.progress = app_data

    def ProgressDate(self, sender, app_data, user_data):
        date = None
        try:
            date = app_data.split('-')
            date = dt.date.Set(int(date[0]), int(date[1]), int(date[2]))
            self.ProgressDetails.date = date
        except IndexError:
            pass
        except ValueError:
            pass