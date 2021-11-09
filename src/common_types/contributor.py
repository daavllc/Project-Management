# Author: DAAV, LLC
# Language: Python 3.10
# License: GPLv3
import csv
import datetime
import os

if __name__ == "__main__":
    exit(-1)

class Contributor:
    def __init__(self):
        self.Info = {}
        self.Contributions = {}

    def __str__(self) -> str:
        return f"Contributor {self.GetName()} with {self.__len__()} contributions over {self.GetTotalHours()} hours"

    def __repr__(self) -> str:
        return f"Contributor {self.GetName()}"

    def __len__(self) -> int:
        return int(len(self.Contributions) / 3)

    # Info
    def SetName(self, name: str) -> None:
        self.Info['name'] = name

    def SetURL(self, url: str) -> None:
        self.Info['url'] = url

    def GetName(self) -> str:
        return self.Info.get('name', None)

    def GetURL(self) -> str:
        return self.Info.get('url', None)

    # Helpers
    def Push(self, hours: float, date: datetime.date, description: str) -> None:
        val = self.__len__()
        self.Contributions[f'hours{val}'] = hours
        self.Contributions[f'date{val}'] = date
        self.Contributions[f'desc{val}'] = description

    def View(self) -> dict:
        return self.Contributions

    # Getters
    def GetFirstDate(self) -> datetime.date:
        return self.Contributions['date0']

    def GetLastDate(self) -> datetime.date:
        val = self.__len__() - 1
        return self.Contributions[f'date{val}']

    def GetFirst(self) -> list[float, datetime.date, str]:
        if self.__len__() > 0:
            return [ self.Contributions['hours0'], self.Contributions['date0'], self.Contributions['desc0'] ]
        else:
            return None
    
    def GetLatest(self) -> list[float, datetime.date, str]:
        val = self.__len__() - 1
        return [ self.Contributions[f'hours{val}'], self.Contributions[f'date{val}'], self.Contributions[f'desc{val}'] ]

    def GetTotalHours(self) -> float:
        return sum(self.GetHours())

    def GetHours(self) -> list[float]:
        return [v for k, v in self.Contributions.items() if k.startswith('hours')]

    def GetDates(self) -> list[datetime.date]:
        return [v for k, v in self.Contributions.items() if k.startswith('date')]

    def GetDescriptions(self) -> list[str]:
        return [v for k, v in self.Contributions.items() if k.startswith('desc')]

    # Serialization
    def Export(self, path) -> None:
        if not os.path.exists(path):
            os.mkdir(path)

        path = os.path.join(path, self.GetName())
        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.path.join(path, "info.inf"), 'w') as f:
            f.write(self.GetURL())
        with open(os.path.join(path, "data.csv"), "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(self.GetHours())
            writer.writerow(self.GetDates())
            writer.writerow(self.GetDescriptions())

    def Import(self, path: str, name: str) -> None:
        self.SetName(name)
        path = os.path.join(path, name)
        with open(os.path.join(path, "info.inf"), 'r') as f:
            self.SetURL(f.readlines()[0].strip())
        with open(os.path.join(path, "data.csv"), 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')

            index = 0
            for item in next(reader):
                self.Contributions[f'hours{index}'] = float(item)
                index += 1
            index = 0
            for item in next(reader):
                item = item.split('-')
                self.Contributions[f'date{index}'] = datetime.date(int(item[0]), int(item[1]), int(item[2]))
                index += 1
            index = 0
            for item in next(reader):
                self.Contributions[f'desc{index}'] = item
                index += 1

