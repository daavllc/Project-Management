import dearpygui.dearpygui as dpg

from .ProjectHierarchy import ProjectHierarchy
from .ProjectManager import ProjectManager
from .ProjectViewer import ProjectViewer

from enum import Enum

class WinID(Enum):
    HIERARCHY = [0, "ProjectHierarchy"]
    MANAGER   = [1, "ProjectManager"]
    VIEWER    = [2, "ProjectViewer"]

class Windows:
    def __init__(self, parent):
        self.parent = parent
        self.ProjectHierarchy = ProjectHierarchy(self)
        self.ProjectManager = ProjectManager(self)
        self.ProjectViewer = ProjectViewer(self)

        self.Status = [True, True, True]

    # Invert window show/hide
    def _InvertWindow(self, win: WinID):
        if self.Status[win.value[0]]:
            dpg.hide_item(win.value[1])
        else:
            dpg.show_item(win.value[1])
        self.Status[win.value[0]] = not self.Status[win.value[0]]

    def InvertProjectHierarchy(self):
        self._InvertWindow(WinID.HIERARCHY)

    def InvertProjectManager(self):
        self._InvertWindow(WinID.MANAGER)

    def InvertProjectViewer(self):
        self._InvertWindow(WinID.VIEWER)
