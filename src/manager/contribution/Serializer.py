import os
import csv
import datetime as dt
import uuid

import config.config as config

from objects.contribution import Contribution
from objects.base_types.version import Version

class Serializer:
    
    InfoFile: str = "info.inf"
    ContributorsFile: str = "contributors.csv"
    ProgressFile: str = "progress.csv"

    def GetContributions(self, ProjectUUID: str) -> list[Contribution]:
        ctbs = []
        if not os.path.exists(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}"):
            return ctbs
        
        for file in os.listdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTIONS}"):
            if os.path.isdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTIONS}/{file}"):
                ctbs.append(self.Import(file))
        return ctbs

    def Export(self, ProjectUUID: str, ctb: Contribution) -> bool:
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTIONS}/{ctb.GetUUIDStr()}"

        if not os.path.exists(path):
            os.mkdir(path) # Projects/<Project UUID>/Contributions/<Contribution UUID>

        # Info
        with open(f"{path}/{self.InfoFile}", 'w') as f:
            f.write(ctb.GetName() + "\n")
            f.write(ctb.GetDateStr() + "\n")
            f.write(ctb.GetNumberStr() + "\n")
            f.write(ctb.GetDescription() + "\n")
            f.write(str(ctb.GetLeadUUID()) + "\n")
            f.write(ctb.GetVersionChangeStr() + "\n")
            f.write(ctb.GetUUIDStr() + "\n")

        # Contributors
        with open(f"{path}/{self.ContributorsFile}", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for cID in ctb.Contributors:
                writer.writerow([str(cID)])

        # Progress
        with open(f"{path}/{self.ProgressFile}", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for prog in ctb.GetProgress():
                writer.writerow(prog)
        return True

    def Import(self, ProjectUUID: str, ContributionUUID: str) -> Contribution:
        ctb = Contribution()
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}/{config.FOLDER_CONTRIBUTIONS}/{ContributionUUID}"

        # Info
        if not os.path.exists(f"{path}/{self.InfoFile}"):
            return None
        with open(f"{path}/{self.InfoFile}", 'r') as f:
            lines = f.readlines()
            ctb.SetName(lines[0].strip())
            date = lines[1].strip().split('-')
            ctb.SetDate(dt.date(int(date[0]), int(date[1]), int(date[2])))
            ctb.SetNumber(int(lines[2].strip()))
            ctb.SetDescription(lines[3].strip())
            ctb.SetLead(lines[4].strip())
            ctb.SetVersionChange(Version(lines[5].strip()))
            ctb.SetUUID(lines[6].strip())

        # Contributors
        if os.path.exists(f"{path}/{self.ContributorsFile}"):
            with open(f"{path}/{self.ContributorsFile}", 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|')
                for row in reader:
                    ctb.Contributors.append(uuid.UUID(row[0]))

        # Progress
        if os.path.exists(f"{path}/{self.ProgressFile}"):
            with open(f"{path}/{self.ProgressFile}", 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|')
                for row in reader:
                    progress = float(row[0])
                    year, month, day = row[1].split('-')
                    date = dt.date(int(year), int(month), int(day))
                    ctb.UpdateProgress(progress, date)
        return ctb