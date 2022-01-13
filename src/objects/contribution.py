# Project-Management.objects.contribution - Implementation of Project Contribution
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import datetime as dt
import os
import uuid

import helpers as hp
from .base_types.version import Version
from .contributor import Contributor
import config.config as config

if __name__ == "__main__":
    exit(-1)
class Contribution:
    def __init__(self, name: str = 'Default Contribution', date: dt.date = dt.date.today(), number: int = 'None', desc: str = 'None', lead: Contributor = 'None', change: Version = Version("0.0.0")):
        self.log = hp.Logger("PM.Contribution", "objects.log")
        self.Info = dict(
            name = name,         # Name of the contribution
            date = date,         # Contribution creation date
            number = number,     # Contribution number in relation to the project: 01, 02, 03...
            desc = desc,         # Description of the contribution
            lead = lead,         # Contributor that is contribution lead
            vChange = change,    # Project version change because this contribution
            uuid = uuid.uuid4()  # Contribution UUID -> don't touch
        )

        self.Contributors = []
        self.Progress: list[list[float, dt.date]] = [ 0.0 ] # index 0 is total progress

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self) -> str:
        return f"'{self.GetName()}' created on {self.GetDateStr()}"

    def __repr__(self) -> str:
        retr = f"'{self.GetName()}': {self.GetUUIDStr()}\n"
        retr += f"Created on {self.GetDate()}, vChange {self.GetVersionChangeStr()}\n"
        retr += f"Lead by '{self.GetLead()}', {self.GetTotalProgressStr()()}% complete\t"
        retr += f"{self.__len__()} progress changes and {len(self.Contributors)} contributors\n"
        num = 1
        for prog in self.GetProgress():
            retr += f"\t{num}. On {prog[1]} progress changed by {prog[0]}%\n"
            num += 1
        for key, value in self.Contributors.items():
            retr += key + " : " + str(value) + "\n"
        return retr

    def __len__(self) -> int:
        return len(self.Progress) - 1

    # ---============================================================---
    #               self.Info get/Get
    # ---============================================================---
    # Setters
    def SetName(self, name: str) -> None:
        self.Info['name'] = name

    def SetDate(self, date: dt.date) -> None:
        self.log.debug(f"Set date to {str(date)}")
        self.Info['date'] = date

    def SetNumber(self, number: int) -> None:
        self.Info['number'] = number
    def CalcNumber(self, ProjectUUID: str) -> None:
        self.Info['number'] = len([f for f in os.listdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTIONS}") 
                                    if os.path.isdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTIONS}/{f}")]) + 1

    def SetDescription(self, desc: str) -> None:
        self.Info['desc'] = desc

    def SetLead(self, cID: uuid.UUID) -> None:
        if cID == 'None':
            self.Info['lead'] = 'None'
        else:
            ctr = Contributor()
            ctr.Import(cID)
            self.Info['lead'] = ctr

    def SetVersionChange(self, change: Version) -> None:
        self.Info['vChange'] = change

    def SetUUID(self, uid: str) -> None:
        self.Info['uuid'] = uuid.UUID(uid)

    # Getters
    def GetName(self) -> str:
        return self.Info.get('name')
    def GetTitle(self) -> str:
        return f"{self.GetNumberStr()}) {self.GetName()}"

    def GetDate(self) -> dt.date:
        return self.Info.get('date')
    def GetDateStr(self) -> str:
        return str(self.GetDate())

    def GetNumber(self) -> int:
        return self.Info.get('number')
    def GetNumberStr(self) -> str:
        return str(self.GetNumber())

    def GetDescription(self) -> str:
        return self.Info.get('desc')

    def GetLead(self) -> Contributor:
        return self.Info.get('lead')
    def GetLeadName(self) -> str:
        lead = self.GetLead()
        if isinstance(lead, Contributor):
            return self.GetLead().GetName()
        return lead
    def GetLeadUUID(self) -> uuid.UUID:
        lead = self.GetLead()
        if isinstance(lead, Contributor):
            return lead.GetUUID()
        return lead

    def GetVersionChange(self) -> Version:
        return self.Info.get('vChange')
    def GetVersionChangeStr(self) -> str:
        return str(self.GetVersionChange())

    def GetUUID(self) -> uuid.UUID:
        return self.Info.get('uuid')
    def GetUUIDStr(self) -> str:
        return str(self.GetUUID())

    # ---============================================================---
    #               Helpers
    # ---============================================================---
    def GetContributor(self, id: uuid.UUID) -> Contributor:
        ctr = Contributor()
        ctr.Import(str(id))

    def GetContributors(self) -> list[Contributor]:
        ctrs = []
        for cID in self.Contributors:
            ctr = Contributor()
            ctr.Import(str(cID))
            ctrs.append(ctr)
        return ctrs

    def GetTotalContributors(self) -> int:
        return len(self.Contributors)

    def GetTotalAdditions(self) -> int:
        total = 0
        for cID in self.Contributors:
            ctr = Contributor()
            ctr.LoadAdditions(str(cID))
            total += ctr.GetTotalContributionAdditions(self.GetUUID())
        return total

    def GetTotalHours(self) -> float:
        total = 0
        for cID in self.Contributors:
            ctr = Contributor()
            ctr.LoadAdditions(str(cID))
            total += ctr.GetTotalContributionHours(self.GetUUID())
        return total

    def GetTotalProgress(self) -> float:
        return self.Progress[0]

    def GetTotalProgressStr(self) -> str:
        return str(self.GetTotalProgress)

    def GetProgress(self) -> list[list[float, dt.date]]:
        return self.Progress[1:]

    def UpdateProgress(self, increase: float, date: dt.date) -> float:
        self.Progress.append([increase, date])
        self.Progress[0] += increase

    def InitContributor(self, filename: str = None) -> Contributor:
        ctr = Contributor()
        if filename is None:
            self.log.debug(f"Creating new contributor '{ctr.GetUUIDStr()}'")
        else:
            ctr.Import(filename)
            self.log.debug(f"Imported contributor '{filename}'")
        ctr.SaveInfo()
        return ctr

    def Push(self, ctrUUID: uuid.UUID, hours: float, date: dt.date, description: str) -> None:
        ctr = self.InitContributor(ctrUUID)
        ctr.Push(hours, date, description, self.GetUUID())
        if not ctrUUID in self.Contributors:
            self.Contributors.append(ctrUUID)
        ctr.Export()