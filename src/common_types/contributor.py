# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python 3.10
# License: GPLv3
###########################
#
# Contributor:
#  Name, date, URL, UUID
#  Additions: [hours, date, what they added, contribution uuid]
import csv
import datetime
import os
import uuid

if __name__ == "__main__":
    exit(-1)

class Contributor:
    def __init__(self, name: str = None, date: datetime.date = None, url: str = None):
        self.Info = {
            'name' : name,        # Name of Contributor
            'date' : date,        # Contributor first added date
            'url' : url,          # Contributor URL
            'uuid' : uuid.uuid4() # Contributor UUID -> don't touch
        }
        self.Additions = {} # hours, dates, what was added, what contribution


    def __str__(self) -> str:
        return f"{self.GetName()} helped with {len(self.GetContributions())} contributions, with {self.__len__()} additions over {self.GetTotalHours()} hours"

    def __repr__(self) -> str:
        return f"{self.GetName()}: {self.GetUUID()}"

    def __len__(self) -> int:
        return int(len(self.Additions) / 4)

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
        val = self.__len__()
        self.Additions[f'hours{val}'] = hours
        self.Additions[f'date{val}'] = date
        self.Additions[f'desc{val}'] = description
        self.Additions[f'cont{val}'] = contribution

    def View(self) -> dict:
        return self.Additions

    def GetFirstDate(self) -> datetime.date:
        return self.Additions.get('date0', None)

    def GetLastDate(self) -> datetime.date:
        val = self.__len__() - 1
        return self.Additions.get(f'date{val}', None)

    def GetFirst(self) -> list[float, datetime.date, str]:
        return self.GetAddition(0)
    
    def GetLatest(self) -> list[float, datetime.date, str]:
        return self.GetAddition(self.__len__() - 1)

    def GetTotalHours(self) -> float:
        return sum(self.GetHours())

    def GetHours(self) -> list[float]:
        return [v for k, v in self.Additions.items() if k.startswith('hours')]

    def GetDates(self) -> list[datetime.date]:
        return [v for k, v in self.Additions.items() if k.startswith('date')]

    def GetDescriptions(self) -> list[str]:
        return [v for k, v in self.Additions.items() if k.startswith('desc')]

    def GetContributions(self) -> list[uuid.UUID]: # returns list of unique contribution uuids
        return list(set([v for k, v in self.Additions.items() if k.startswith('cont')]))

    def GetContributionInfo(self, cID: uuid.UUID) -> list[float, datetime.date, str]: # Returns list of data for the supplied contribution
        # if key starts with 'cont' and value == cID, append int('cont###'[4:])
        indexes = list([int(k[4:]) for k, v in self.Additions.items() if k.startswith('cont') and v == cID])
        info = [[],[],[]]
        for index in indexes:
            info[0].append(self.Additions.get(f'hours{index}', None))
            info[1].append(self.Additions.get(f'date{index}', None))
            info[2].append(self.Additions.get(f'desc{index}', None))
        if len(info[0]) == 0:
            return [ None, None, None ]
        return info

    def GetAddition(self, index: int) -> list[float, datetime.date, str, uuid.UUID]: # Returns list of data by addition 'index'
        return [ self.Additions.get(f'hours{index}', None), self.Additions.get(f'date{index}', None), self.Additions.get(f'desc{index}', None), self.Additions.get(f'cont{index}', None) ]

    # Serialization
    def Export(self, path: str) -> None:
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(path, self.GetName())
        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.path.join(path, "info.inf"), 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetDate() + "\n")
            f.write(self.GetUUIDStr() + "\n")
        with open(os.path.join(path, "data.csv"), "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for index in range(self.__len__()):
                writer.writerow(self.GetAddition(index))

    def Import(self, path: str, name: str) -> None:
        path = os.path.join(path, name)
        with open(os.path.join(path, "info.inf"), 'r') as f:
            lines = f.readlines()
            self.SetName(lines[0].strip())
            date = lines[1].split('-')
            self.SetDate(datetime.date(int(date[0]), int(date[1]), int(date[2])))
            self.SetURL( lines[2].strip())
            self.SetUUID(lines[3].strip())
        with open(os.path.join(path, "data.csv"), 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')
            rows = sum(1 for line in f)

            for index in range(rows):
                row = next(reader)
                self.Additions[f'hours{index}'] = float(row[0])
                date = row[1].split('-')
                self.Additions[f'date{index}'] = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                self.Additions[f'desc{index}'] = row[2]
                self.Additions[f'cont{index}'] = uuid.UUID(row[3])


