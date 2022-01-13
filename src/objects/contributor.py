# Project-Management.objects.contributor - Implementation of Project Contributor
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import datetime as dt
import csv
import os
import uuid

import helpers as hp
import config.config as config

from objects.base_types.time import Time

if __name__ == "__main__":
    exit(-1)

class Contributor:
    def __init__(self, name: str = 'Default Contributor', date: dt.date = dt.date.today(), url: str = 'None'):
        self.log = hp.Logger("PM.Contributor", "objects.log")
        self.Info = {
            'name' : name,        # Name of Contributor
            'date' : date,        # Date contributor was added to the project
            'url' : url,          # Contributor URL
            'uuid' : uuid.uuid4() # Contributor UUID -> don't touch
        }
        self.Additions: dict = dict(
            # dt.datetime.now() = dict(
            # timeWorked: Time = timeWorked
            # description: str = description
            # ctbUUID: uuid.UUID = ctbUUID
            # ), ...
        )

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
        self.Info['name'] = name

    def SetDate(self, date: dt.date) -> None:
        self.Info['date'] = date

    def SetURL(self, url: str) -> None:
        self.Info['url'] = url

    def SetUUID(self, uid: str) -> None:
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
    def Push(self, timeWorked: Time, description: str, contribution: uuid.UUID, pushTime = dt.datetime.now()) -> None:
        self.Additions[pushTime] = dict(
            timeWorked = timeWorked,
            description = description,
            ctbUUID = contribution
        )

    def View(self) -> dict[dict[Time, dt.date, str, uuid.UUID]]:
        return self.Additions

    def GetFirstDate(self) -> dt.datetime:
        return (self.Additions.keys())[0]
    def GetFirstDateStr(self) -> str:
        return str(self.GetFirstDate())

    def GetLastDate(self) -> dt.datetime:
        return (self.Additions.keys())[-1]
    def GetLastDateStr(self) -> str:
        return str(self.GetLastDate())

    def GetFirst(self) -> list[dt.datetime, dict[Time, str, uuid.UUID]]:
        return [self.additions.keys[0], self.additions.values[0]]
    
    def GetLast(self) -> list[dt.datetime, dict[Time, str, uuid.UUID]]:
        return [self.additions.keys[-1], self.additions.values[-1]]

    def GetTotalHours(self) -> Time:
        return sum(self.GetHours())

    def GetHours(self) -> list[Time]:
        return [val[0] for val in self.Additions.values()]

    def GetDates(self) -> list[dt.date]:
        return [val for val in self.Additions.keys()]

    def GetDescriptions(self) -> list[str]:
        return [val[1] for val in self.Additions.values()]

    def GetWorkedContributions(self) -> list[uuid.UUID]: # returns list of unique contribution uuids
        return list(set([val[2] for val in self.Additions.values()]))

    def GetContributionInfo(self, cID: uuid.UUID) -> list[dt.datetime, Time, str]: # Returns list of data for the supplied contribution from most recent to least recent
        info = []
        for key, value in self.Additions.items():
            if value['ctbUUID'] == cID:
                info.append[key, value[0], value[1]]
        return info

    def GetTotalContributionHours(self, cID: uuid.UUID) -> Time:
        return sum(detail[1] for detail in self.GetContributionInfo(cID))

    def GetContributionFirstDate(self, cID: uuid.UUID) -> dt.date:
        return min(detail[0] for detail in self.GetContributionInfo(cID))

    def GetContributionLastDate(self, cID: uuid.UUID) -> dt.date:
        return max(detail[0] for detail in self.GetContributionInfo(cID))

    def GetTotalContributionAdditions(self, cID: uuid.UUID) -> int:
        return len(self.GetContributionInfo(cID))

    def GetAdditionByIndex(self, index: int) -> list[Time, str, uuid.UUID]: # Returns list of data by index
        return self.Additions[index]

    def GetAdditionByDate(self, date: dt.date) -> list[Time, str, uuid.UUID]:
        return [key for key in self.addititions.keys() if key.date() == date]

    def GetAdditions(self) -> dict[dict[Time, dt.date, str, uuid.UUID]]:
        return self.Additions

    def GetTotalAdditions(self) -> int:
        return len(self.Additions)

