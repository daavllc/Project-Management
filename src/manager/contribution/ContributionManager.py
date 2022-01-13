import os

import helpers as hp
import config.config as config

from objects.contribution import Contribution
from manager.command import Command
from manager.controller import Sources
from manager.contribution.Serializer import Serializer

class ContributionManager:
    def __init__(self, manager):
        self.log = hp.Logger("PM.Manager.Contributions", "manager.log")
        self.manager = manager # manager.project.ProjectManager
        self.Serializer = Serializer()

        self.m_ProjectUUID = None
        self.m_Contributions: list[Contribution] = []
        self.m_Selected = None
        self.m_LiveContribution = None
        self.m_ContributionSaved = True

    # General Methods
    class CreateContributor(Command): # can't be implemented in commands
        def __init__(self, parent, index: int):
            self.parent = parent
            self.index = index
            self.ctb: Contribution = Contribution()

        def Details(self) -> str:
            return f"created contribution [{self.ctb.GetUUIDStr()}]"

        def Execute(self) -> None:
            self.ctb.SetNumber(self.index + 1)
            self.parent.m_Contributions.insert(0, self.ctb)

        def Undo(self) -> None:
            self.parent.m_Contributions.remove(self.ctb)
            if self.parent.m_Selected == self.index + 1:
                self.parent.Deselect()

        def Redo(self) -> None:
            self.parent.m_Contributions.insert(0, self.ctb)

    def Create(self) -> bool:
        self.manager.ClearHistory(Sources.CONTRIBUTION)
        self._Execute(self.CreateContributor(self, len(self.m_Contributions)))
        self._Select(len(self.m_Contributions) - 1)
        return True

    class SelectContribution(Command):
        def __init__(self, parent, ctb: Contribution, index: int):
            self.parent = parent
            self.ctb = ctb
            self.index = index

        def Details(self) -> str:
            return f"selected contribution [{self.ctb.GetUUIDStr()}]"

        def Execute(self) -> None:
            self.parent._Select(self.index)

        def Undo(self) -> None:
            self.parent.Deselect()

        def Redo(self) -> None:
            self.parent.Select(self.index)

    def Select(self, index: int) -> bool:
        if index < 0 and index >= len(self.m_Contributions):
            return False
        self.manager.ClearHistory(Sources.CONTRIBUTION)
        self._Execute(self.SelectContribution(self, self.m_Contributions[index], index))
        return True

    def Deselect(self) -> bool:
        self.m_LiveContribution = None
        self.m_Selected = None
        self.m_ContributionSaved = True
        return True

    def GetTitles(self) -> list[str]:
        contributions: list[str] = []
        for ctb in self.m_Contributions:
            contributions.append(ctb.GetTitle())
        return contributions

    def HasProject(self) -> bool:
        if self.m_ProjectUUID is None:
            return False
        return True

    def GetProject(self) -> str:
        return self.m_ProjectUUID

    def HasSelected(self) -> bool:
        if self.m_Selected is None:
            return False
        return True

    def GetSelected(self) -> Contribution:
        return self.m_LiveContribution

    def GetAll(self) -> list[Contribution]:
        return self.m_Contributions

    def IsSaved(self) -> bool:
        return self.m_ContributionSaved

    def GetByName(self, name: str) -> Contribution:
        for ctb in self.m_Contributions:
            if ctb.GetTitle() == name:
                return ctb

    # Live Project Methods
    def GetContributorNames(self):
        return self.manager.GetContributorNames()


    # Internal methods
    def _Execute(self, command: Command):
        self.manager.Execute(Sources.CONTRIBUTION, command)

    def _Select(self, index):
        self.m_LiveContribution = self.m_Contributions[index]
        self.m_Selected = index

    def _Init(self, ProjectUUID: str):
        self.m_ProjectUUID = ProjectUUID
        self.m_Contributions = self.Serializer.GetContributions(ProjectUUID)
        self.log.debug(f"Found {len(self.m_Contributions)} contributions(s)")
        self._Sort()
        return True

    def _Sort(self) -> list[Contribution]:
        ctbs = []
        for ctb in self.m_Contributions:
            num = ctb.GetNumber()
            if num >= len(ctbs):
                ctbs.append(num)
            else:
                ctbs.insert(num - 1, ctb)

    def _Deinit(self):
        self.m_ProjectUUID = None
        self.m_Contributions = []