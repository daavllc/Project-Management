# Project-Management.objects.contributor - Implementation of Project Contributor
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import datetime as dt
import csv
import os
import uuid

import helpers as hp
import config.config as config

if __name__ == "__main__":
    exit(-1)

class Contributor:
    def __init__(self, name: str = 'None', date: dt.date = dt.date.today(), url: str = 'None'):
        self.log = hp.Logger("PM.Contributor", "objects.log")
        self.Info = {
            'name' : name,        # Name of Contributor
            'date' : date,        # Date contributor was added to the project
            'url' : url,          # Contributor URL
            'uuid' : uuid.uuid4() # Contributor UUID -> don't touch
        }
        self.Additions: list[list[float, dt.date, str, uuid.UUID]] = []

        # Serialization
        self.Files = {
            'info' : 'info.inf',
            'additions' : 'additions.csv'
        }
        self.LoadedInfo = False
        self.LoadedAdditions = False
        self.SavedInfo = True
        self.SavedAdditions = True

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
    # Setters
    def SetName(self, name: str) -> None:
        self.SavedInfo = False
        self.Info['name'] = name

    def SetDate(self, date: dt.date) -> None:
        self.SavedInfo = False
        self.Info['date'] = date

    def SetURL(self, url: str) -> None:
        self.SavedInfo = False
        self.Info['url'] = url

    def SetUUID(self, uid: str) -> None:
        self.SavedInfo = False
        self.Info['uuid'] = uuid.UUID(uid)

    # Getters
    def GetName(self) -> str:
        return self.Info.get('name')

    def GetDate(self) -> dt.date:
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
    def GetInfoFile(self) -> str:
        return self.Files.get('info')
    def GetAdditionsFile(self) -> str:
        return self.Files.get('additions')

    def Push(self, hours: float, date: dt.date, description: str, contribution: uuid.UUID) -> None:
        self.SavedAdditions = False
        self.Additions.append([hours, date, description, contribution])

    def View(self) -> list[list[float, dt.date, str, uuid.UUID]]:
        return self.Additions

    def GetFirstDate(self) -> dt.date:
        return self.Additions[0][1]
    def GetFirstStr(self) -> str:
        return str(self.GetFirstDate())

    def GetLastDate(self) -> dt.date:
        return self.Additions[-1][1]
    def GetLastDateStr(self) -> str:
        return str(self.GetLastDate())

    def GetFirst(self) -> list[float, dt.date, str, uuid.UUID]:
        self.Additions[0]
    
    def GetLast(self) -> list[float, dt.date, str, uuid.UUID]:
        self.Additions[-1]

    def GetTotalHours(self) -> float:
        return sum(self.GetHours())

    def GetHours(self) -> list[float]:
        return [a[0] for a in self.Additions]

    def GetDates(self) -> list[dt.date]:
        return [a[1] for a in self.Additions]

    def GetDescriptions(self) -> list[str]:
        return [a[2] for a in self.Additions]

    def GetWorkedContributions(self) -> list[uuid.UUID]: # returns list of unique contribution uuids
        return list(set([a[3] for a in self.Additions]))

    def GetContributionInfo(self, cID: uuid.UUID) -> list[float, dt.date, str]: # Returns list of data for the supplied contribution from most recent to least recent
        return list([a[0:3] for a in self.Additions if a[3] == cID])

    def GetTotalContributionHours(self, cID: uuid.UUID) -> float:
        return sum(detail[0] for detail in self.GetContributionInfo(cID))

    def GetContributionFirstDate(self, cID: uuid.UUID) -> dt.date:
        return min(detail[1] for detail in self.GetContributionInfo(cID))

    def GetContributionLastDate(self, cID: uuid.UUID) -> dt.date:
        return max(detail[1] for detail in self.GetContributionInfo(cID))

    def GetTotalContributionAdditions(self, cID: uuid.UUID) -> int:
        return len(self.GetContributionInfo(cID))

    def GetAddition(self, index: int) -> list[float, dt.date, str, uuid.UUID]: # Returns list of data by index
        return self.Additions[index]

    def GetAdditions(self) -> list[list[float, dt.date, str, uuid.UUID]]:
        return self.Additions

    def GetTotalAdditions(self) -> int:
        return len(self.Additions)

    # ---============================================================---
    #               Serialization
    # ---============================================================---
    # Export
    def Export(self, force: bool = False) -> None:
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{self.GetUUIDStr()}"
        if not os.path.exists(path):
            os.mkdir(path) # Projects/<Project UUID>/Contributors/<Contributor UUID>

        self.SaveInfo(force)
        self.SaveAdditions(force)

    def SaveInfo(self, force: bool = False) -> None:
        file = self.GetInfoFile()
        if self.SavedInfo and not force:
            self.log.debug(f"Skipped saving {file}")
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{self.GetUUIDStr()}"
        with open(f"{path}/{file}", 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetURL() + "\n")
            f.write(self.GetUUIDStr() + "\n")
        self.log.debug(f"Saved {file}")
        self.SavedInfo = True

    def SaveAdditions(self, force: bool = False) -> None:
        file = self.GetAdditionsFile()
        if self.SavedAdditions and not force:
            self.log.debug(f"Skipped saving {file}")
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{self.GetUUIDStr()}"
        with open(f"{path}/{file}", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for index in range(self.__len__()):
                writer.writerow(self.Additions[index])
        self.log.debug(f"Saved {file}")
        self.SavedAdditions = True

    # Import
    def Import(self, filename: str, force: bool = False) -> None:
        self.LoadInfo(filename, force)
        self.LoadAdditions(filename, force)

    def LoadInfo(self, filename: str, force: bool = False) -> None:
        file = self.GetInfoFile()
        if self.LoadedInfo and not force:
            self.log.debug(f"Skipped loading {file}")
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{filename}"
        if not os.path.exists(f"{path}/{file}"):
            self.LoadedInfo = True
            self.log.debug(f"No {file} file to load")
            return
        with open(f"{path}/{file}", 'r') as f:
            lines = f.readlines()
            self.SetName(lines[0].strip())
            date = lines[1].split('-')
            self.SetDate(dt.date(int(date[0]), int(date[1]), int(date[2])))
            self.SetURL( lines[2].strip())
            self.SetUUID(lines[3].strip())
        self.log.debug(f"Loaded {file}")
        self.LoadedInfo = True

    def LoadAdditions(self, filename: str, force: bool = False) -> None:
        file = self.GetAdditionsFile()
        if self.LoadedAdditions and not force:
            self.log.debug(f"Skipped loading {file}")
            return
        path = f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}/{filename}"
        if not os.path.exists(f"{path}/{file}"):
            self.LoadedProgress = True
            self.log.debug(f"No {file} file to load")
            return
        with open(f"{path}/{file}", 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')

            for row in reader:
                hours = float(row[0])
                year, month, day = row[1].split('-')
                date = dt.date(int(year), int(month), int(day))
                desc = row[2]
                cUID = uuid.UUID(row[3])
                self.Push(hours, date, desc, cUID)
        self.log.debug(f"Loaded {file}")
        self.LoadedAdditions = True

