# Project-Management.base_types.contributor - Implementation of Project Contributor
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import csv
import datetime
import os
import uuid

import config.config as config

if __name__ == "__main__":
    exit(-1)

class Contributor:
    def __init__(self, name: str = 'None', date: datetime.date = datetime.datetime.now().date(), url: str = 'None'):
        self.Info = {
            'name' : name,        # Name of Contributor
            'date' : date,        # Date contributor was added to the project
            'url' : url,          # Contributor URL
            'uuid' : uuid.uuid4() # Contributor UUID -> don't touch
        }

        self.Additions = [] # hours, dates, what was added, what contribution

        self.LoadedInfo = False

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self) -> str:
        return f"{self.GetName()} helped with {len(self.GetWorkedContributions())} contributions, with {self.__len__()} additions over {self.GetTotalHours()} hours"

    def __repr__(self) -> str:
        retr = f"{self.GetName()}: {self.GetUUID()}\n"
        retr += f"Started on {self.GetDate()}, worked on {len(self.GetWorkedContributions())} contributions"
        return retr

    def __len__(self) -> int:
        return len(self.Additions)

    # ---============================================================---
    #               self.Info get/set
    # ---============================================================---
    def SetName(self, name: str) -> None:
        self.Info['name'] = name

    def SetDate(self, date: datetime.date) -> None:
        self.Info['date'] = date

    def SetURL(self, url: str) -> None:
        self.Info['url'] = url

    def SetUUID(self, uid: str) -> None:
        self.Info['uuid'] = uuid.UUID(uid)

    def GetName(self) -> str:
        return self.Info.get('name')

    def GetDate(self) -> datetime.date:
        return self.Info.get('date')
    def GetDateStr(self) -> str:
        return str(self.GetDate())

    def GetURL(self) -> str:
        return self.Info.get('url')

    def GetUUID(self) -> uuid.UUID:
        return self.Info.get('uuid')
    def GetUUIDStr(self) -> str:
        return str(self.GetUUID())

    # ---============================================================---
    #               Helpers
    # ---============================================================---
    def Push(self, hours: float, date: datetime.date, description: str, contribution: uuid.UUID) -> None:
        self.Additions.append([hours, date, description, contribution])

    def View(self) -> list[list[float, datetime.date, str, uuid.UUID]]:
        return self.Additions

    def GetFirstDate(self) -> datetime.date:
        return self.Additions[0][1]

    def GetLastDate(self) -> datetime.date:
        self.Additions[-1][1]

    def GetFirst(self) -> list[float, datetime.date, str, uuid.UUID]:
        self.Additions[0]
    
    def GetLatest(self) -> list[float, datetime.date, str, uuid.UUID]:
        self.Additions[-1]

    def GetTotalHours(self) -> float:
        return sum(self.GetHours())

    def GetHours(self) -> list[float]:
        return [a[0] for a in self.Additions]

    def GetDates(self) -> list[datetime.date]:
        return [a[1] for a in self.Additions]

    def GetDescriptions(self) -> list[str]:
        return [a[2] for a in self.Additions]

    def GetWorkedContributions(self) -> list[uuid.UUID]: # returns list of unique contribution uuids
        return list(set([a[3] for a in self.Additions]))

    def GetContributionInfo(self, cID: uuid.UUID) -> list[float, datetime.date, str]: # Returns list of data for the supplied contribution
        indexes = list([a[3] for a in self.Additions if a[3] == cID])
        return [self.Additions[index] for index in indexes]

    def GetTotalContributionHours(self, cID: uuid.UUID) -> float:
        info = self.GetContributionInfo(cID)
        return sum(info[0])

    def GetAddition(self, index: int) -> list[float, datetime.date, str, uuid.UUID]: # Returns list of data by index
        return self.Additions[index]

    # ---============================================================---
    #               Serialization
    # ---============================================================---
    def Export(self) -> None: # path expects contributors folder ex: projects/name/contributors
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{self.GetUUIDStr()}"
        if not os.path.exists(path):
            os.mkdir(path)

        with open(f"{path}/info.inf", 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetURL() + "\n")
            f.write(self.GetUUIDStr() + "\n")
        with open(f"{path}/data.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for index in range(self.__len__()):
                writer.writerow(self.Additions[index])

    def Import(self, filename: str) -> None:
        if not self.LoadedInfo:
            self.LoadInfo(filename)
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{filename}"
        with open(f"{path}/data.csv", 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')

            for row in reader:
                hours = float(row[0])
                date = row[1].split('-')
                date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                desc = row[2]
                cUID = uuid.UUID(row[3])
                self.Push(hours, date, desc, cUID)

    def LoadInfo(self, filename: str) -> None:
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{filename}"
        with open(f"{path}/info.inf", 'r') as f:
            lines = f.readlines()
            self.SetName(lines[0].strip())
            date = lines[1].split('-')
            self.SetDate(datetime.date(int(date[0]), int(date[1]), int(date[2])))
            self.SetURL( lines[2].strip())
            self.SetUUID(lines[3].strip())
        self.LoadedInfo = True


