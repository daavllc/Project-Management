import os
import csv
import datetime as dt
import uuid

import config.config as config

from objects.contributor import Contributor
from objects.base_types.version import Version

class Serializer:
    InfoFile = "info.inf"
    AdditionsFile = "additions.csv"

    def GetContributors(self, ProjectUUID: str) -> list[Contributor]:
        ctrs = []
        if not os.path.exists(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}"):
            return ctrs
    
        for file in os.listdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTORS}"):
            if os.path.isdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTORS}/{file}"):
                ctrs.append(self.Import(file))
        return ctrs

    def Export(self, ProjectUUID: str, ctr: Contributor) -> bool:
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTORS}/{ctr.GetUUIDStr()}"

        if not os.path.exists(path):
            os.mkdir(path) # Projects/<Project UUID>/Contributors/<Contributor UUID>

        # Info
        with open(f"{path}/{self.InfoFile}", 'w') as f:
            f.write(ctr.GetName() + "\n")
            f.write(ctr.GetDateStr() + "\n")
            f.write(ctr.GetURL() + "\n")
            f.write(ctr.GetUUIDStr() + "\n")

        # Additions
        with open(f"{path}/{self.AdditionsFile}", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for index in range(ctr.__len__()):
                writer.writerow(ctr.Additions[index])
        return True

    def Import(self, ProjectUUID: str, ContributorUUID: str) -> Contributor:
        ctr = Contributor()
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTORS}/{ContributorUUID}"

        # Info
        if os.path.exists(f"{path}/{self.InfoFile}"):
            with open(f"{path}/{self.InfoFile}", 'r') as f:
                lines = f.readlines()
                ctr.SetName(lines[0].strip())
                date = lines[1].split('-')
                ctr.SetDate(dt.date(int(date[0]), int(date[1]), int(date[2])))
                ctr.SetURL( lines[2].strip())
                ctr.SetUUID(lines[3].strip())

        # Additions
        if os.path.exists(f"{path}/{self.AdditionsFile}"):
            with open(f"{path}/{self.AdditionsFile}", 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|')
                for row in reader:
                    hours = float(row[0])
                    year, month, day = row[1].split('-')
                    date = dt.date(int(year), int(month), int(day))
                    desc = row[2]
                    cUID = uuid.UUID(row[3])
                    ctr.Push(hours, date, desc, cUID)
        return ctr