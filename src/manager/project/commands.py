import datetime as dt
import uuid

from objects.project import Project
from manager.command import Command

class SetName(Command):
    def __init__(self, prj: Project, toName: str):
        self.fromName: str = prj.GetName()
        self.toName: str = toName
        self.prj: Project = prj

    def Details(self) -> str:
        return f"set project [{self.prj.GetUUIDStr()}] name from '{self.fromName}' to '{self.toName}'"

    def Execute(self) -> None:
        self.prj.SetName(self.toName)

    def Undo(self) -> None:
        self.prj.SetName(self.fromName)

    def Redo(self) -> None:
        self.prj.SetName(self.toName)


class SetDate(Command):
    def __init__(self, prj: Project, toDate: dt.datetime):
        self.fromDate: dt.datetime = prj.GetDate()
        self.toDate: dt.datetime = toDate
        self.prj: Project = prj

    def Details(self) -> str:
        return f"set project [{self.prj.GetUUIDStr()}] date from '{str(self.fromDate)}' to '{str(self.toDate)}'"

    def Execute(self) -> None:
        self.prj.SetDate(self.toDate)

    def Undo(self) -> None:
        self.prj.SetDate(self.fromDate)

    def Redo(self) -> None:
        self.prj.SetDate(self.toDate)

class SetLead(Command):
    def __init__(self, prj: Project, toLeadName: str, toLeadUUID: uuid.UUID):
        self.fromLead: list[str, uuid.UUID] = prj.GetLead()
        self.toLead: list[str, uuid.UUID] = [toLeadName, toLeadUUID]
        self.prj: Project = prj

    def Details(self) -> str:
        return f"set project [{self.prj.GetUUIDStr()}] lead from '{self.fromLead[0]}' to '{self.toLead[0]}'"

    def Execute(self) -> None:
        self.prj.SetLead(self.toLead[0], self.toLead[1])

    def Undo(self) -> None:
        self.prj.SetLead(self.fromLead[0], self.fromLead[1])

    def Redo(self) -> None:
        self.prj.SetLead(self.toLead[0], self.toLead[1])

class SetDescription(Command):
    def __init__(self, prj: Project, toDesc: str):
        self.fromDesc: str = prj.GetDescription()
        self.toDesc: str = toDesc
        self.prj: Project = prj

    def Details(self) -> str:
        return f"set project [{self.prj.GetUUIDStr()}] description from '{self.fromDesc}' to '{self.toDesc}'"

    def Execute(self) -> None:
        self.prj.SetDescription(self.toDesc)

    def Undo(self) -> None:
        self.prj.SetDescription(self.fromDesc)

    def Redo(self) -> None:
        self.prj.SetDescription(self.toDesc)
