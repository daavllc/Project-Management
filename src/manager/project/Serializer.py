import datetime as dt
import os
import csv
import uuid
import config.config as config
import helpers as hp

from objects.project import Project
from objects.base_types.version import Version

class Serializer:
    log = hp.Logger("PM.Manager.Projects.Serializer", "manager.log")
    HeaderFile = "header.inf"
    VersionFile = "versions.csv"

    def GetProjects(self) -> list[Project]:
        projects: list[Project] = []
        for file in os.listdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}"):
            if os.path.isdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{file}"):
                projects.append(self.Import(file))
        return projects

    def Export(self, prj: Project) -> bool:
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}"
        if not os.path.exists(path):
            os.mkdir(path) # Projects/

        path = f"{path}/{prj.GetUUIDStr()}"
        if not os.path.exists(path):
            os.mkdir(path) # Projects/<Project UUID>

        if not os.path.exists(f"{path}/{config.FOLDER_CONTRIBUTIONS}"):
            os.mkdir(f"{path}/{config.FOLDER_CONTRIBUTIONS}") # Projects/<Project UUID>/Contributions
        if not os.path.exists(f"{path}/{config.FOLDER_CONTRIBUTORS}"):
            os.mkdir(f"{path}/{config.FOLDER_CONTRIBUTORS}") # Projects/<Project UUID>/Contributors

        # Header
        with open(f"{path}/{self.HeaderFile}", 'w') as f:
            f.write(prj.GetName() + "\n")
            f.write(prj.GetDateStr() + "\n")
            f.write(prj.GetDescription() + "\n")
            if type(prj.GetLead()) == list:
                f.write(prj.GetLeadName() + "|" + str(prj.GetLeadUUID()) + "\n")
            else:
                f.write(prj.GetLead() + "\n")
            f.write(prj.GetUUIDStr() + "\n")
        SavedHeader = True

        # Versions
        with open(f"{path}/{self.VersionFile}", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for ver in prj.GetVersions():
                writer.writerow(ver)
        return True

    def Import(self, ProjectUUID: str) -> Project:
        prj = Project()
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{ProjectUUID}"
        # Header
        if not os.path.exists(f"{path}/{self.HeaderFile}"):
            return None
        with open(f"{path}/{self.HeaderFile}", 'r') as f:
            lines = f.readlines()
            prj.SetName(lines[0].strip())
            year, month, day = lines[1].strip().split('-')
            prj.SetDate( dt.date(int(year), int(month), int(day)) )
            prj.SetDescription(lines[2].strip())
            if "|" in lines[3]:
                lines[3] = lines[3].strip().split("|")
                prj.SetLead(lines[3][0], lines[3][1])
            else:
                prj.Header['lead'] = lines[3].strip() # TODO: make better
            prj.SetUUID(lines[4].strip())

        # Versions
        if os.path.exists(f"{path}/{self.VersionFile}"):
            with open(f"{path}/{self.VersionFile}", 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|')
                for row in reader:
                    version = Version(row[0])
                    cID = uuid.UUID(row[1])
                    prj.UpdateVersion(version, cID)
        return prj