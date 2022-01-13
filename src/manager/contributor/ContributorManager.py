import os

import helpers as hp
import config.config as config

from objects.contributor import Contributor
from manager.controller import Sources
from manager.command import Command
from manager.contributor.Serializer import Serializer

class ContributorManager:
    def __init__(self, manager):
        self.log = hp.Logger("PM.Manager.Contributors", "manager.log")
        self.manager = manager # manager.project.ProjectManager
        self.Serializer = Serializer()

        self.m_ProjectUUID = None
        self.m_Contributors: list[Contributor] = []
        self.m_Selected = None
        self.m_LiveContributor = None
        self.m_ContributorSaved = True

    # General Methods
    class CreateContributor(Command): # can't be implemented in commands
        def __init__(self, parent, index: int):
            self.parent = parent
            self.index = index
            self.ctr: Contributor = Contributor()

        def Details(self) -> str:
            return f"created contributor [{self.ctr.GetUUIDStr()}]"

        def Execute(self) -> None:
            self.parent.m_Contributors.append(self.ctr)

        def Undo(self) -> None:
            self.parent.m_Contributors.remove(self.ctr)
            if self.parent.m_Selected == self.index + 1:
                self.parent.Deselect()

        def Redo(self) -> None:
            self.parent.m_Contributors.append(self.ctr)

    def Create(self) -> bool:
        self.manager.ClearHistory(Sources.CONTRIBUTOR)
        self._Execute(self.CreateContributor(self, len(self.m_Contributors)))
        self._Select(len(self.m_Contributors) - 1)
        return True

    class SelectContributor(Command):
        def __init__(self, parent, ctr: Contributor, index: int):
            self.parent = parent
            self.ctr = ctr
            self.index = index

        def Details(self) -> str:
            return f"selected contributor [{self.ctr.GetUUIDStr()}]"

        def Execute(self) -> None:
            self.parent._Select(self.index)

        def Undo(self) -> None:
            self.parent.Deselect()

        def Redo(self) -> None:
            self.parent.Select(self.index)

    def Select(self, index: int) -> bool:
        if index < 0 and index >= len(self.m_Contributors):
            return False
        self.manager.ClearHistory(Sources.CONTRIBUTOR)
        self._Execute(self.SelectContributor(self, self.m_Contributors[index], index))
        return True

    def Deselect(self) -> bool:
        self.m_LiveContributor = None
        self.m_Selected = None
        self.m_ContributorSaved = True
        return True

    def GetNames(self) -> list[str]:
        contributors: list[str] = []
        for ctr in self.m_Contributors:
            contributors.append(ctr.GetName())
        return contributors

    def HasProject(self) -> bool:
        if self.m_ProjectUUID is None:
            return False
        return True

    def HasSelected(self) -> bool:
        if self.m_Selected is None:
            return False
        return True

    def GetSelected(self) -> Contributor:
        return self.m_LiveContributor

    def IsSaved(self) -> bool:
        return self.m_ContributorSaved

    def GetByName(self, name: str) -> Contributor:
        for ctr in self.m_Contributors:
            if ctr.GetName() == name:
                return ctr

    # Live Project Methods


    # Internal methodsself.manager.Execute(Sources.CONTRIBUTOR, self.CreateContributor(self, len(self.m_Contributors) - 1))
    def _Execute(self, command: Command):
        self.manager.Execute(Sources.CONTRIBUTOR, command)

    def _Select(self, index):
        self.m_LiveContributor = self.m_Contributors[index]
        self.m_Selected = index

    def _Init(self, ProjectUUID):
        self.m_ProjectUUID = ProjectUUID
        self.m_Contributors = self.Serializer.GetContributors(ProjectUUID)
        self.log.debug(f"Found {len(self.m_Contributors)} contributor(s)")
        self.m_Contributors.sort()
        return True

    def _Deinit(self):
        self.m_ProjectUUID = None
        self.m_Contributors = []