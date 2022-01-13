import datetime as dt
from enum import Enum, auto

import helpers as hp

from manager.command import Command

class Sources(Enum):
    PROJECT = auto()
    CONTRIBUTION = auto()
    CONTRIBUTOR = auto()

class ControllerInst:
    __instance = None
    
    @staticmethod
    def Get():
        if ControllerInst.__instance is None:
            ControllerInst()
        return ControllerInst.__instance

    def __init__(self):
        if ControllerInst.__instance is not None:
            return ControllerInst.__instance
        else:
            ControllerInst.__instance = self
            self.log = hp.Logger("PM.Manager.Controller", "manager.log")
            self.Timeline = dict(
                Project = Controller("PM.Manager.Controller.Projects"),
                Contribution = Controller("PM.Manager.Controller.Contributions"),
                Contributor = Controller("PM.Manager.Controller.Contributors"),
                Sources = [],
                Position = -1
            )
            self.MaxTimelines = 5

    def Execute(self, source: Sources, command: Command):
        if source == Sources.PROJECT:
            self.Timeline['Project'].Execute(command)
        elif source == Sources.CONTRIBUTION:
            self.Timeline['Contribution'].Execute(command)
        elif source == Sources.CONTRIBUTOR:
            self.Timeline['Contributor'].Execute(command)
        self.Timeline['Sources'].append(source)
        self.Timeline['Position'] += 1

    def Undo(self):
        if self.Timeline['Position'] < 0:
            return
        source = self.Timeline['Sources'][self.Timeline['Position']]
        if source == Sources.PROJECT:
            self.Timeline['Project'].Undo()
        elif source == Sources.CONTRIBUTION:
            self.Timeline['Contribution'].Undo()
        elif source == Sources.CONTRIBUTOR:
            self.Timeline['Contributor'].Undo()
        self.Timeline['Position'] -= 1

    def Redo(self):
        if self.Timeline['Position'] == len(self.Timeline['Sources']) - 1:
            return
        source = self.Timeline['Sources'][self.Timeline['Position']]
        if source == Sources.PROJECT:
            self.Timeline['Project'].Redo()
        elif source == Sources.CONTRIBUTION:
            self.Timeline['Contribution'].Redo()
        elif source == Sources.CONTRIBUTOR:
            self.Timeline['Contributor'].Redo()
        self.Timeline['Position'] += 1

    def Clear(self, source: Sources = None):
        if source is None or source == Sources.PROJECT:
            self.Timeline['Project'].Clear()
            self.Timeline['Contribution'].Clear()
            self.Timeline['Contributor'].Clear()
            self.Timeline['Sources'] = []
            self.Timeline['Position'] = -1
        elif source == Sources.CONTRIBUTION:
            self.Timeline['Contribution'].Clear()
            for idx, source in enumerate(self.Timeline['Sources']):
                if source == Sources.CONTRIBUTION:
                    self.Timeline['Sources'].pop(idx)
                    self.Timeline['Position'] -= 1
        elif source == Sources.CONTRIBUTOR:
            self.Timeline['Contributor'].Clear()
            for idx, source in enumerate(self.Timeline['Sources']):
                if source == Sources.CONTRIBUTOR:
                    self.Timeline['Sources'].pop(idx)
                    self.Timeline['Position'] -= 1
        else:
            self.log.warn("Something went wrong")

    def GetTimeline(self) -> list[dt.datetime, str]:
        history: list[dt.datetime, str] = []
        PrjIdx = 0
        CtbIdx = 0
        CtrIdx = 0
        for source in self.Timeline['Sources'][:self.Timeline['Position'] + 1]:
            if  source == Sources.PROJECT:
                history.append(self.Timeline['Project'].GetHistory(PrjIdx))
                PrjIdx += 1
            elif source == Sources.CONTRIBUTION:
                history.append(self.Timeline['Contribution'].GetHistory(CtbIdx))
                CtbIdx += 1
            elif source == Sources.CONTRIBUTOR:
                history.append(self.Timeline['Contributor'].GetHistory(CtrIdx))
                CtrIdx += 1
        return history

    def History(self):
        for item in self.GetTimeline():
            self.log.info(f"{item[1]} at {item[0]}")


class Controller:
    class Type(Enum):
        EXECUTE = "Executed: "
        REDO = "Undid: "
        UNDO = "Redid: "

    def __init__(self, logName: str):
        self.log = hp.Logger(logName, "manager.log")
        self.m_History: list[list[self.Type, Command, dt.datetime]] = []
        self.m_Position: int = -1
        self.m_MaxHistory: int = 50

    def Execute(self, cmd: Command) -> None:
        cmd.Execute()
        self.m_History = self.m_History[:self.m_Position]
        self.m_History.append([self.Type.EXECUTE, cmd, dt.datetime.now()])
        self.m_Position += 1

    def Undo(self) -> None:
        if self.m_Position < 1:
            return
        command: Command = self.m_History[self.m_Position][1]
        self.m_History[self.m_Position][0] = self.Type.UNDO
        self.m_Position -= 1
        command.Undo()

    def Redo(self) -> None:
        if len(self.m_History) == 0 or self.m_Position == len(self.m_History) - 1:
            return
        command: Command = self.m_History[self.m_Position][1]
        self.m_History[self.m_Position][0] = self.Type.REDO
        self.m_Position += 1
        command.Redo()

    def Get(self, index: int):
        return self.m_History[index]

    def Clear(self) -> None:
        self.m_History.clear()
        self.m_Position = -1

    def GetStatement(self, index: int) -> str:
        if self.m_History:
            item = self.m_History[index]
            return f"{item[0].value}{item[1].Details()} at {item[2]}"
        else:
            return "No history to show"

    def GetHistory(self, index: int) -> list[dt.datetime, str]:
        item = self.m_History[index]
        return [item[2], f"{item[0].value}{item[1].Details()}"]

    def GetFullHistory(self) -> list[dt.datetime, str]:
        history = []
        if self.m_History:
            for item in self.m_History[:self.m_Position + 1]:
                history.append([item[2], f"{item[0].value}{item[1].Details()}"])
        return history