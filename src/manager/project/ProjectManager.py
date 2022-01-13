import datetime as dt
import uuid

import helpers as hp

from objects.project import Project
from manager.command import Command
from manager.controller import Sources
import manager.project.commands as Commands
from manager.project.Serializer import Serializer

from manager.contribution.ContributionManager import ContributionManager
from manager.contributor.ContributorManager import ContributorManager

class ProjectManager:

    def __init__(self, manager):
        self.log = hp.Logger("PM.Manager.Projects", "manager.log")
        self.manager = manager # manager.manager
        self.Serializer = Serializer()

        self.m_Projects: list[Project] = []
        self.m_Selected: int = None
        self.m_LiveProject = None
        self.m_ProjectSaved = True

        self.m_SelectedProperty = None
        self.CtbManager = ContributionManager(self) # TODO: self shouldn't be needed
        self.CtrManager = ContributorManager(self) # TODO: self shouldn't be needed
        self.__Initialize()

    def GetContributionManager(self) -> ContributionManager:
        return self.CtbManager

    def GetContributorManager(self) -> ContributorManager:
        return self.CtrManager

    # General Methods
    class CreateProject(Command): # can't be implemented in commands
        def __init__(self, parent, index: int):
            self.parent = parent
            self.index = index
            self.prj: Project = Project()

        def Details(self) -> str:
            return f"created project [{self.prj.GetUUIDStr()}]"

        def Execute(self) -> None:
            self.parent.m_Projects.append(self.prj)

        def Undo(self) -> None:
            self.parent.m_Projects.remove(self.prj)
            if self.parent.m_Selected == self.index + 1:
                self.parent.Deselect()

        def Redo(self) -> None:
            self.parent.m_Projects.append(self.prj)

    def Create(self) -> bool:
        self.manager.ClearHistory(Sources.PROJECT)
        self._Execute(self.CreateProject(self, len(self.m_Projects)))
        self._Select(len(self.m_Projects) - 1)
        return True

    class SelectProject(Command):
        def __init__(self, parent, prj: Project, index: int):
            self.parent = parent
            self.prj = prj
            self.index = index

        def Details(self) -> str:
            return f"selected project [{self.prj.GetUUIDStr()}]"

        def Execute(self) -> None:
            self.parent._Select(self.index)

        def Undo(self) -> None:
            self.parent.Deselect()

        def Redo(self) -> None:
            self.parent.Select(self.index)

    def Select(self, index: int) -> bool:
        if index < 0 and index >= len(self.m_Projects):
            return False
        self.manager.ClearHistory(Sources.PROJECT)
        self._Execute(self.SelectProject(self, self.m_Projects[index], index))
        return True

    def Deselect(self) -> bool:
        self.m_LiveProject = None
        self.m_Selected = None
        self.m_ProjectSaved = True
        self.CtbManager._Deinit()
        self.CtrManager._Deinit()
        return True

    def Get(self, index: int) -> bool:
        if index < 0 and index >= len(self.m_Projects):
            raise Exception(f"Unknown project: {index}/{len(self.m_Projects)}")
        return self.m_Projects[index]

    def GetNames(self) -> list[str]:
        projects: list[str] = []
        for prj in self.m_Projects:
            projects.append(prj.GetName())
        return projects

    def HasSelected(self) -> bool:
        if self.m_Selected is None:
            return False
        return True

    def GetSelected(self) -> Project:
        return self.m_LiveProject

    def IsSaved(self) -> bool:
        return self.m_ProjectSaved

    def GetContributionTitles(self) -> list[str]:
        if not self.HasSelected():
            return
        return self.CtbManager.GetTitles()

    def GetContributions(self):
        if not self.HasSelected():
            return
        return self.CtbManager.GetAll()

    def GetContributorNames(self) -> list[str]:
        if not self.HasSelected():
            return
        return self.CtrManager.GetNames()

    def GetContributors(self) -> list[str]:
        if not self.HasSelected():
            return
        return self.CtrManager.GetAll()

    def HasSelectedProperty(self) -> bool:
        if self.m_SelectedProperty is None:
            return False
        return True

    def HasContributionSelected(self) -> bool:
        if self.m_SelectedProperty == Sources.CONTRIBUTION:
            return True
        return False

    def HasContributorSelected(self) -> bool:
        if self.m_SelectedProperty == Sources.CONTRIBUTOR:
            return True
        return False

    def HasSelectedContribution(self) -> bool:
        return self.CtbManager.HasSelected()

    def HasSelectedContributor(self) -> bool:
        return self.CtrManager.HasSelected()

    # Live Project Methods
    def SetName(self, name: str) -> bool:
        self._Execute(Commands.SetName(self.m_LiveProject, name))
        self.SetUnsaved()
        return True

    def SetDate(self, date: dt.date) -> bool:
        self._Execute(Commands.SetDate(self.m_LiveProject, date))
        self.SetUnsaved()
        return True

    def SetLead(self, name: str, uuid: uuid.UUID = uuid.uuid4()) -> bool:
        self._Execute(Commands.SetLead(self.m_LiveProject, name, uuid))
        self.SetUnsaved()
        return True

    def SetDescription(self, description: str) -> bool:
        self._Execute(Commands.SetDescription(self.m_LiveProject, description))
        self.SetUnsaved()
        return True

    def Load(self, ProjectUUID: str) -> Project:
        prj: Project = self.Serializer.Import(ProjectUUID)
        return prj

    def Save(self) -> bool:
        if self.m_Selected is None:
            return False
        if not self.m_ProjectSaved:
            self.m_ProjectSaved = True
            self.m_LiveProject.SetName(self.m_LiveProject.GetName()[:-1])
        self.Serializer.Export(self.m_LiveProject)
        self.m_Projects[self.m_Selected] = self.m_LiveProject
        return True

    def SetUnsaved(self):
        if self.m_ProjectSaved:
            self.m_ProjectSaved = False
            self.m_LiveProject.SetName(self.m_LiveProject.GetName() + "*")

    # Internal methods
    def _Execute(self, command: Command):
        self.manager.Execute(Sources.PROJECT, command)

    def Execute(self, source: Sources, command: Command): # Called by children
        self.manager.Execute(source, command)

    def ClearHistory(self, source: Sources):
        self.manager.ClearHistory(source)

    def _Select(self, index):
        self.m_LiveProject = self.m_Projects[index]
        self.m_Selected = index
        self.CtbManager._Init(self.m_LiveProject.GetUUIDStr())
        self.CtrManager._Init(self.m_LiveProject.GetUUIDStr())
    
    def __Initialize(self):
        self.m_Projects = self.Serializer.GetProjects()
        self.log.debug(f"Found {len(self.m_Projects)} project(s)")
        return True