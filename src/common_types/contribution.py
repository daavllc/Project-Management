# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python 3.10
# License: GPLv3
if __name__ == "__main__":
    exit(-1)

import csv
import os
import datetime
import uuid

from .base_types.version import Version
from .contributor import Contributor
import config.config as config

class Contribution:
    def __init__(self, name: str = 'None', date: datetime.date = 'None', number: str = 'None', desc: str = 'None', lead: str = 'None', change: Version = 'None'):
        self.Info = {
            'name' : name,         # Name of the contribution
            'date' : date,         # Contribution creation date
            'number' : number,     # Contribution number in relation to the project: 01, 02, 03...
            'desc' : desc,         # Description of the contribution
            'lead' : lead,         # Name of Contribution Lead
            'vChange' : change,    # Project version change because this contribution
            'uuid' : uuid.uuid4()  # Contribution UUID -> don't touch
        }

        self.Contributors = {}
        self.Progress = [ 0.0 ] # list of [float, datetime.date], index 0 is total progress

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self) -> str:
        return f"'{self.GetName()}' created on {self.GetDate()}"

    def __repr__(self) -> str:
        retr = f"'{self.GetName()}': {self.GetUUID()}\n"
        retr += f"Created on {self.GetDate()}, vChange {self.GetVersionChange()}\n"
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
    def SetName(self, name: str) -> None:
        self.Info['name'] = name

    def SetDate(self, date: datetime.date) -> None:
        self.Info['date'] = date

    def SetNumber(self, number: str) -> None:
        self.Info['number'] = number

    def SetDescription(self, desc: str) -> None:
        self.Info['desc'] = desc

    def SetLead(self, contributor: str) -> None:
        self.Info['lead'] = contributor

    def SetVersionChange(self, change: Version) -> None:
        self.Info['vChange'] = change

    def SetUUID(self, uid: str) -> None:
        self.Info['uuid'] = uuid.UUID(uid)

    def GetName(self) -> str:
        return self.Info.get('name', None)

    def GetDate(self) -> datetime.date:
        return self.Info.get('date', None)
    def GetDateStr(self) -> str:
        return str(self.GetDate())

    def GetNumber(self) -> str:
        return self.Info.get('number', None)

    def GetDescription(self) -> str:
        return self.Info.get('desc', None)

    def GetLead(self) -> str:
        return self.Info.get('lead', None)

    def GetVersionChange(self) -> Version:
        return self.Info.get('vChange', None)
    def GetVersionChangeStr(self) -> str:
        return str(self.GetVersionChange())

    def GetUUID(self) -> uuid.UUID:
        return self.Info.get('uuid', None)
    def GetUUIDStr(self) -> str:
        return str(self.GetUUID())

    # ---============================================================---
    #               Helpers
    # ---============================================================---
    def GetContributor(self, name: str) -> uuid.UUID:
        return self.Contributors.get(name, None)

    def GetContributorInfo(self, name: str) -> list[str, uuid.UUID]:
        return [name, self.GetContributor(name)]

    def GetContributors(self) -> dict:
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

    def AddContributor(self, name: str, cid: uuid.UUID) -> None:
        self.Contributors[name] = cid

    def InitContributor(self, name: str) -> Contributor:
        if os.path.exists(config.PATH_CURRENT_PROJECT + "/Contributors/" + name):
            ctr = Contributor()
            ctr.Import(config.PATH_CURRENT_PROJECT + "/Contributors", name)
            return ctr
        else: # This means the contributor does not exist, new contributor?
            print("Creating new contributor " + name)
            ctr = Contributor()
            ctr.SetName(name)
            ctr.SetDate(datetime.datetime.now().date())
            return ctr

    def Push(self, contributorName: str, hours: float, date: datetime.date, description: str) -> None:
        ctr = self.InitContributor(contributorName)
        ctr.Push(hours, date, description, self.GetUUID())
        if not contributorName in self.Contributors.keys():
            self.AddContributor(ctr.GetName(), ctr.GetUUID())
        ctr.Export(config.PATH_CURRENT_PROJECT + "/Contributors")

    # ---============================================================---
    #               Serialization
    # ---============================================================---
    def Export(self, path: str) -> None:
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(path, f"{self.GetNumber()}. {self.GetName()}")
        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.path.join(path, "info.inf"), 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetNumber() + "\n")
            f.write(self.GetDescription() + "\n")
            f.write(self.GetLead() + "\n")
            f.write(self.GetVersionChangeStr() + "\n")
            f.write(self.GetUUIDStr() + "\n")

        with open(os.path.join(path, "contributors.csv"), "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for key, value in self.Contributors.items():
                writer.writerow([key, value])

        with open(os.path.join(path, "progress.csv"), "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for prog in self.GetProgress():
                writer.writerow(prog)

    def Import(self, path: str, name: str) -> None:
        path = os.path.join(path, name)
        with open(os.path.join(path, "info.inf"), 'r') as f:
            lines = f.readlines()
            self.SetName(lines[0].strip())
            date = lines[1].strip().split('-')
            self.SetDate(datetime.date(int(date[0]), int(date[1]), int(date[2])))
            self.SetNumber(lines[2].strip())
            self.SetDescription(lines[3].strip())
            self.SetLead(lines[4].strip())
            self.SetVersionChange(Version(lines[5].strip()))
            self.SetUUID(lines[6].strip())
        with open(os.path.join(path, "contributors.csv"), 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')

            for row in reader:
                self.AddContributor(row[0], row[1])

        with open(os.path.join(path, "progress.csv"), 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')

            for row in reader:
                progress = float(row[0])
                date = row[1].split('-')
                date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                self.UpdateProgress(progress, date)
