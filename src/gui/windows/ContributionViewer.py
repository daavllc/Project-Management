
import os
import dearpygui.dearpygui as dpg

from common_types.contribution import Contribution

from gui.logger import Logger
import config.config as config

class ContributionViewer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.ContributionExplorer
        self.contribution = None
        self.log = Logger("PM.Window.ContributionViewer")

        self.Window = "ContributionViewer"
        self.Pre = "ctbV"

        with dpg.window(tag=self.Window, label="Contribution Viewer", no_close=True):
            self.DrawContributionInfo()

    def InitContribution(self, name: str):
        ctb = Contribution()
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"
        ctb.Import(path, name)
        self.SetContribution(ctb)

    def SetContribution(self, ctb: Contribution):
        self.contribution = ctb
        try:
            dpg.delete_item(f"{self.Pre}_NotSelected")
        except SystemError:
            pass
        config.UUID_CURRENT_CONTRIBUTION = self.contribution.GetUUID()
        self.DrawContributionInfo()

    def DrawContributionInfo(self):
        if self.contribution is None:
            dpg.add_text(parent=self.Window, default_value="No contribution selected", tag=f"{self.Pre}_NotSelected")
            return
        for name in ["_ContributionName", "_ContributionUUID", "_ContributionDate", "_ContributionLead", "_ContributionNumber", "_ContributionVersionChange", "_ContributionProgress", "_ContributionTitleGroup"]:
            try:
                dpg.delete_item(f"{self.Pre}{name}")
            except SystemError:
                pass
        with dpg.group(parent=self.Window, horizontal=True, tag=f"{self.Pre}_ContributionTitleGroup"):
            dpg.add_text(default_value=f"Contribution: '{self.contribution.GetName()}' :", tag=f"{self.Pre}_ContributionName")
            dpg.add_text(default_value=self.contribution.GetUUIDStr(), tag=f"{self.Pre}_ContributionUUID")
        dpg.add_text(parent=self.Window, default_value=f"Creation date: '{self.contribution.GetDateStr()}'", tag=f"{self.Pre}_ContributionDate")
        dpg.add_text(parent=self.Window, default_value=f"Lead: '{self.contribution.GetLead()}'", tag=f"{self.Pre}_ContributionLead")
        dpg.add_text(parent=self.Window, default_value=f"Number: '{self.contribution.GetNumber()}'", tag=f"{self.Pre}_ContributionNumber")
        dpg.add_text(parent=self.Window, default_value=f"Version Change: '{self.contribution.GetVersionChangeStr()}'", tag=f"{self.Pre}_ContributionVersionChange")
        dpg.add_text(parent=self.Window, default_value=f"Progress: '{self.contribution.GetTotalProgress()}'", tag=f"{self.Pre}_ContributionProgress")