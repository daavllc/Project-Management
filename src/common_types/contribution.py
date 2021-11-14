# Project-Management.base_types.contribution - Implementation of Project Contribution
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import csv
import os
import datetime
import uuid

from .base_types.version import Version
from .contributor import Contributor
import config.config as config

if __name__ == "__main__":
    exit(-1)
class Contribution:
    def __init__(self, name: str = 'None', date: datetime.date = datetime.datetime.now().date(), number: int = 'None', desc: str = 'None', lead: str = 'None', change: Version = 'None'):
        self.Info = {
            'name' : name,         # Name of the contribution
            'date' : date,         # Contribution creation date
            'number' : number,     # Contribution number in relation to the project: 01, 02, 03...
            'desc' : desc,         # Description of the contribution
            'lead' : lead,         # Name of Contribution Lead
            'vChange' : change,    # Project version change because this contribution
            'uuid' : uuid.uuid4()  # Contribution UUID -> don't touch
        }
        if self.Info['number'] == 'None':
            self.CalcNumber()

        self.Contributors = []
        self.Progress = [ 0.0 ] # list of [float, datetime.date], index 0 is total progress

        self.LoadedInfo = False
        self.LoadedCtrs = False
        self.LoadedProgress = False

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

    def SetDate(self, date: datetime.date) -> None:
        self.Info['date'] = date

    def SetNumber(self, number: int) -> None:
        self.Info['number'] = number
    def CalcNumber(self) -> None:
        self.Info['number'] = len([f for f in os.listdir(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}") 
                                    if os.path.isdir(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}/{f}")]) + 1

    def SetDescription(self, desc: str) -> None:
        self.Info['desc'] = desc

    def SetLead(self, contributor: str) -> None:
        self.Info['lead'] = contributor

    def SetVersionChange(self, change: Version) -> None:
        self.Info['vChange'] = change

    def SetUUID(self, uid: str) -> None:
        self.Info['uuid'] = uuid.UUID(uid)

    # Getters
    def GetName(self) -> str:
        return self.Info.get('name')

    def GetDate(self) -> datetime.date:
        return self.Info.get('date')
    def GetDateStr(self) -> str:
        return str(self.GetDate())

    def GetNumber(self) -> int:
        return self.Info.get('number')
    def GetNumberStr(self) -> str:
        return str(self.GetNumber())

    def GetDescription(self) -> str:
        return self.Info.get('desc')

    def GetLead(self) -> str:
        return self.Info.get('lead')

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

    def GetContributors(self) -> list:
        return self.Contributors

    def GetTotalProgress(self) -> float:
        return self.Progress[0]

    def GetTotalProgressStr(self) -> str:
        return str(self.GetTotalProgress)

    def GetProgress(self) -> list[list[float, datetime.date]]:
        return self.Progress[1:]

    def UpdateProgress(self, increase: float, date: datetime.date) -> float:
        self.Progress.append([increase, date])
        self.Progress[0] += increase

    def InitContributor(self, filename: str) -> Contributor:
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}"
        if os.path.exists(f"{path}/{filename}"):
            ctr = Contributor()
            ctr.Import(filename)
        else: # This means the contributor does not exist, new contributor?
            print(f"Creating new contributor")
            ctr = Contributor()
        return ctr

    def Push(self, ctrUUID: uuid.UUID, hours: float, date: datetime.date, description: str) -> None:
        ctr = self.InitContributor(ctrUUID)
        ctr.Push(hours, date, description, self.GetUUID())
        if not ctrUUID in self.Contributors:
            self.Contributors.append(ctrUUID)
        ctr.Export()

    # ---============================================================---
    #               Serialization
    # ---============================================================---
    def Export(self) -> None: # path expects contributions folder ex: projects/name/contributions
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"

        path = f"{path}/{self.GetUUIDStr()}"
        if not os.path.exists(path):
            os.mkdir(path)

        with open(f"{path}/info.inf", 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetNumberStr() + "\n")
            f.write(self.GetDescription() + "\n")
            f.write(self.GetLead() + "\n")
            f.write(self.GetVersionChangeStr() + "\n")
            f.write(self.GetUUIDStr() + "\n")

        with open(f"{path}/contributors.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for contributor in self.Contributors:
                writer.writerow(contributor)

        with open(f"{path}/progress.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for prog in self.GetProgress():
                writer.writerow(prog)

    def Import(self, filename: str) -> None:
        if not self.LoadedInfo:
            self.LoadInfo(filename)
        if not self.LoadedCtrs:
            self.LoadContributors(filename)
        if not self.LoadedProgress:
            self.LoadProgress(filename)

    def LoadInfo(self, filename: str) -> None:
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}/{filename}"
        with open(f"{path}/info.inf", 'r') as f:
            lines = f.readlines()
            self.SetName(lines[0].strip())
            date = lines[1].strip().split('-')
            self.SetDate(datetime.date(int(date[0]), int(date[1]), int(date[2])))
            self.SetNumber(int(lines[2].strip()))
            self.SetDescription(lines[3].strip())
            self.SetLead(lines[4].strip())
            self.SetVersionChange(Version(lines[5].strip()))
            self.SetUUID(lines[6].strip())
        self.LoadedInfo = True

    def LoadContributors(self, filename: str) -> None:
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}/{filename}"
        with open(f"{path}/contributors.csv", 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')
            for row in reader:
                self.AddContributor(row[0], row[1])
        self.LoadedCtrs = True

    def LoadProgress(self, filename: str) -> None:
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}/{filename}"
        with open(f"{path}/progress.csv", 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')
            for row in reader:
                progress = float(row[0])
                date = row[1].split('-')
                date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                self.UpdateProgress(progress, date)
        self.LoadedProgress = True
