import datetime as dt
import uuid

from objects.contributor import Contributor
from manager.command import Command
from objects.base_types.time import Time

class SetName(Command):
    def __init__(self, ctr: Contributor, toName: str):
        self.fromName: str = ctr.GetName()
        self.toName: str = toName
        self.ctr: Contributor = ctr

    def Details(self) -> str:
        return f"set contributor [{self.ctr.GetUUIDStr()}] name from {self.fromName} to {self.toName}"

    def Execute(self) -> None:
        self.ctr.SetName(self.toName)

    def Undo(self) -> None:
        self.ctr.SetName(self.fromName)

    def Redo(self) -> None:
        self.ctr.SetName(self.toName)


class SetDate(Command):
    def __init__(self, ctr: Contributor, toDate: dt.datetime):
        self.fromDate: dt.datetime = ctr.GetDate()
        self.toDate: dt.datetime = toDate
        self.ctr: Contributor = ctr

    def Details(self) -> str:
        return f"set contributor [{self.ctr.GetUUIDStr()}] date from {str(self.fromDate)} to {str(self.toDate)}"

    def Execute(self) -> None:
        self.ctr.SetDate(self.toDate)

    def Undo(self) -> None:
        self.ctr.SetDate(self.fromDate)

    def Redo(self) -> None:
        self.ctr.SetDate(self.toDate)

class SetURL(Command):
    def __init__(self, ctr: Contributor, toURL: str):
        self.fromURL: str = ctr.GetLead()
        self.toURL: str = toURL
        self.ctr: Contributor = ctr

    def Details(self) -> str:
        return f"set contributor [{self.ctr.GetUUIDStr()}] url from {self.fromURL} to {self.toURL}"

    def Execute(self) -> None:
        self.ctr.SetURL(self.toURL)

    def Undo(self) -> None:
        self.ctr.SetLead(self.fromURL)

    def Redo(self) -> None:
        self.ctr.SetLead(self.toURL)

class AddAddition(Command):
    def __init__(self, ctr: Contributor, timeWorked: Time, description: str, ctbUUID: uuid.UUID, pushTime = dt.datetime.now()):
        self.timeWorked: Time = timeWorked
        self.description: str = description
        self.ContributionUUID: uuid.UUID = ctbUUID
        self.pushTime = pushTime
        self.ctr: Contributor = ctr

    def Details(self) -> str:
        return f"Pushed addition to contributor [{self.ctr.GetUUIDStr()}] {self.pushTime}: [{self.timeWorked}, {self.description}, {self.ContributionUUID}]"

    def Execute(self) -> None:
        self.ctr.Push(self.timeWorked, self.description, self.ContributionUUID, self.pushTime)

    def Undo(self) -> None:
        self.ctr.SetDescription(self.fromDesc)

    def Redo(self) -> None:
        self.ctr.Push(self.timeWorked, self.description, self.ContributionUUID, self.pushTime)
