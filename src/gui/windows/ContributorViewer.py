
import os
import dearpygui.dearpygui as dpg

from common_types.contributor import Contributor

from gui.logger import Logger
import config.config as config

class ContributorViewer:
    def __init__(self, parent):
        self.parent = parent # gui.gui.ContributorExplorer
        self.contributor = None
        self.log = Logger("PM.Window.ContributorViewer")

        self.Window = "ContributorViewer"
        self.Pre = "ctrV"

        with dpg.window(tag=self.Window, label="Contributor Viewer", no_close=True):
            self.DrawContributorInfo()

    def InitContributor(self, name: str):
        ctb = Contributor()
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}"
        ctb.Import(path, name)
        self.SetContributor(ctb)

    def SetContributor(self, ctr: Contributor):
        self.contributor = ctr
        try:
            dpg.delete_item(f"{self.Pre}_NotSelected")
        except SystemError:
            pass
        self.DrawContributorInfo()

    def DrawContributorInfo(self):
        if self.contributor is None:
            dpg.add_text(parent=self.Window, default_value="No contributor selected", tag=f"{self.Pre}_NotSelected")
            return
        for name in ["_ContributorName", "_ContributorUUID", "_ContributorDate", "_ContributorURL", "_ContributorTitleGroup"]:
            try:
                dpg.delete_item(f"{self.Pre}{name}")
            except SystemError:
                pass
        with dpg.group(parent=self.Window, horizontal=True, tag=f"{self.Pre}_ContributorTitleGroup"):
            dpg.add_text(default_value=f"Contributor: '{self.contributor.GetName()}' :", tag=f"{self.Pre}_ContributorName")
            dpg.add_text(default_value=self.contributor.GetUUIDStr(), tag=f"{self.Pre}_ContributorUUID")
        dpg.add_text(parent=self.Window, default_value=f"Date began: '{self.contributor.GetDateStr()}'", tag=f"{self.Pre}_ContributorDate")
        dpg.add_text(parent=self.Window, default_value=f"URL: '{self.contributor.GetURL()}'", tag=f"{self.Pre}_ContributorURL")