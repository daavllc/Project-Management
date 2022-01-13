from manager.controller import ControllerInst, Sources
from manager.project.ProjectManager import ProjectManager
from manager.contribution.ContributionManager import ContributionManager
from manager.contributor.ContributorManager import ContributorManager

from manager.command import Command

import helpers as hp

class Manager:
    """
    Provides easy access to basic functions and quality of life features
    Just like a manager, it doesn't know what it's managing, but does manages it all anyway
    """
    log = hp.Logger("PM.Manager", "manager.log")

    def __init__(self):
        self.Controller = ControllerInst()
        self.Projects = ProjectManager(self)
        self.Contributions = ContributionManager(self)
        self.Contributorts = ContributorManager(self)

    # Controller abstractions
    def Execute(self, source: Sources, cmd: Command):
        self.Controller.Execute(source, cmd)

    def Undo(self):
        self.Controller.Undo()

    def Redo(self):
        self.Controller.Redo()

    def ClearHistory(self, source: Sources = None):
        self.Controller.Clear(source)

    def History(self, source = None):
        self.Controller.History()

    def Save(self):
        self.Projects.Save()

    # Project abstractions
    def GetSelectedProject(self):
        return self.Projects.GetSelected()

    def GetSelectedProjectUUID(self):
        return self.GetSelectedProject().GetUUIDStr()

