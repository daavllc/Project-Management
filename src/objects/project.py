# Project-Management.objects.project - Implementation of Project header
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import datetime as dt
import csv
import os
import uuid

import helpers as hp
from .base_types.version import Version
from .contribution import Contribution
from .contributor import Contributor
import config.config as config

if __name__ == "__main__":
    exit(-1)

class Project:
    def __init__(self, name: str = 'None', date: dt.date = dt.date.today(), desc: str = 'None', lead: Contributor = 'None'):
        self.log = hp.Logger("PM.Project", "objects.log")
        self.Header = {
            'name' : name, # str
            'date' : date, # dt.date
            'desc' : desc, # str
            'lead' : lead, # Contributor
            'uuid' : uuid.uuid4()
        }
        self.Version: list[list[Version, uuid.UUID]] = [Version(0, 0, 0)] # index 0 is total version
        # Serialization
        self.Files = {
            'header' : 'header.inf',
            'version' : 'versions.csv'
        }
        self.LoadedHeader = False
        self.LoadedVersion = False
        self.SavedHeader = True
        self.SavedVersion = True

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self) -> str:
        return f"'{self.GetName()}' created on {self.GetDateStr()}"

    def __repr__(self) -> str:
        retr = f"'{self.GetName()}' : {self.GetUUIDStr()}\n"
        retr += f"Created on {self.GetDateStr()}, Version {self.GetVersionStr()}\n"
        retr += f"Lead by {self.GetLead()}\n"
        return retr

    # ---============================================================---
    #               self.Header get/Get
    # ---============================================================---
    # Setters
    def SetName(self, name: str) -> None:
        self.SavedHeader = False
        self.Header['name'] = name

    def SetDate(self, date: dt.date) -> None:
        self.SavedHeader = False
        self.Header['date'] = date

    def SetDescription(self, desc: str) -> None:
        self.SavedHeader = False
        self.Header['desc'] = desc

    def SetLead(self, cID: uuid.UUID) -> None:
        self.SavedHeader = False
        if cID == 'None':
            self.Header['lead'] = 'None'
        else:
            ctr = Contributor()
            ctr.Import(cID)
            self.Header['lead'] = ctr

    def SetUUID(self, uid: str) -> None:
        self.SavedHeader = False
        self.Header['uuid'] = uuid.UUID(uid)

    # Getters
    def GetName(self) -> str:
        return self.Header.get('name')

    def GetDate(self) -> dt.date:
        return self.Header.get('date')
    def GetDateStr(self) -> str:
        return str(self.GetDate())

    def GetDescription(self) -> str:
        return self.Header.get('desc')

    def GetLead(self) -> uuid.UUID:
        return self.Header.get('lead')
    def GetLeadName(self) -> str:
        lead = self.GetLead()
        if isinstance(lead, Contributor):
            return self.GetLead().GetName()
        return lead
    def GetLeadUUID(self) -> uuid.UUID:
        lead = self.GetLead()
        if isinstance(lead, Contributor):
            return lead.GetUUID()
        return lead

    def GetVersion(self) -> Version:
        return self.Version[0]
    def GetVersionStr(self) -> str:
        return str(self.GetVersion())

    def GetUUID(self) -> uuid.UUID:
        return self.Header.get('uuid')
    def GetUUIDStr(self) -> str:
        return str(self.GetUUID())

    # ---============================================================---
    #               Helpers
    # ---============================================================---
    def GetHeaderFile(self) -> str:
        return self.Files.get('header')
    def GetVersionFile(self) -> str:
        return self.Files.get('version')

    def SetCurrent(self) -> None:
        config.PATH_CURRENT_PROJECT = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{self.GetUUIDStr()}"
        self.log.debug(f"Set {config.PATH_CURRENT_PROJECT = }")

    def UpdateVersion(self, ver: Version, cID: uuid.UUID) -> None:
        self.SavedVersion = False
        for idx, data in enumerate(self.GetVersions()):
            if data[1] == cID:
                self.Version[idx + 1] = [ver, cID]
                break
        else:
            self.Version.append([ver, cID])
        self.CalcVersion()

    def CalcVersion(self):
        tVer = Version(0, 0, 0)
        for data in self.GetVersions():
            tVer += data[0]
        self.log.debug(f"Updated version to {str(tVer)}")
        self.Version[0] = tVer

    def GetVersions(self) -> list[Version, uuid.UUID]:
        return self.Version[1:]

    # Contributions
    def AddContribution(self) -> Contribution:
        return self.InitContribution()

    def GetContribution(self, filename: str) -> Contribution:
        return self.InitContribution(filename)

    def GetContributions(self) -> list[Contribution]: # Returns sorted list of contributions
        path = config.PATH_CURRENT_PROJECT + "/" + config.FOLDER_CONTRIBUTIONS
        contributions = []
        for file in os.listdir(path):
            if os.path.isdir(path + "/" + file):
                contributions.append(self.InitContribution(file))
        contributions = sorted(contributions, key=lambda ctb: ctb.GetNumber(), reverse=True)
        return contributions

    def InitContribution(self, filename: str = None) -> Contribution:
        path = config.PATH_CURRENT_PROJECT + "/" + config.FOLDER_CONTRIBUTIONS
        ctb = Contribution()
        if filename is None:
            self.log.debug(f"Created new contribution '{ctb.GetUUIDStr()}'")
            ctb.Export()
            return ctb
        else:
            ctb.LoadInfo(filename)
            self.log.debug(f"Imported contribution '{ctb.GetUUIDStr()}'")
            return ctb

    # Contributors
    def AddContributor(self) -> Contributor:
        ctr = Contributor()
        ctr.Export()
        return ctr

    def GetContributor(self, cID: uuid.UUID) -> Contributor:
        ctr = Contributor()
        ctr.LoadInfo(cID)
        return ctr

    def GetContributors(self) -> list[Contributor]: # Returns list of contributors
        path = config.PATH_CURRENT_PROJECT + "/" + config.FOLDER_CONTRIBUTORS
        contributors = []
        for file in os.listdir(path):
            if os.path.isdir(path + "/" + file):
                ctr = Contributor()
                ctr.LoadInfo(file)
                contributors.append(ctr)
        return contributors

    # ---============================================================---
    #               Serialization
    # ---============================================================---
    # Export
    def Export(self, force: bool = False) -> None:
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}"
        if not os.path.exists(path):
            os.mkdir(path) # Projects/

        path = f"{path}/{self.GetUUIDStr()}"
        if not os.path.exists(path):
            os.mkdir(path) # Projects/<Project UUID>

        if not os.path.exists(f"{path}/{config.FOLDER_CONTRIBUTIONS}"):
            os.mkdir(f"{path}/{config.FOLDER_CONTRIBUTIONS}") # Projects/<Project UUID>/Contributions
        if not os.path.exists(f"{path}/{config.FOLDER_CONTRIBUTORS}"):
            os.mkdir(f"{path}/{config.FOLDER_CONTRIBUTORS}") # Projects/<Project UUID>/Contributors

        self.SaveHeader(force)
        self.SaveVersion(force)

    def SaveHeader(self, force: bool = False) -> None:
        file = self.GetHeaderFile()
        if self.SavedHeader and not force:
            self.log.debug(f"Skipped saving {file}")
            return
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{self.GetUUIDStr()}"
        with open(f"{path}/{file}", 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetDescription() + "\n")
            f.write(str(self.GetLeadUUID()) + "\n")
            f.write(self.GetUUIDStr() + "\n")
        self.log.debug(f"Saved {file}")
        self.SavedHeader = True

    def SaveVersion(self, force: bool = False) -> None:
        file = self.GetVersionFile()
        if self.SavedVersion and not force:
            self.log.debug(f"Skipped saving {file}")
            return
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{self.GetUUIDStr()}"
        with open(f"{path}/{file}", "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for ver in self.GetVersions():
                writer.writerow(ver)
        self.log.debug(f"Saved {file}")
        self.SavedVersion = True

    # Import
    def Import(self, filename: str, force: bool = False) -> None:
        self.LoadHeader(filename, force)
        self.LoadVersion(filename, force)

    def LoadHeader(self, filename: str, force: bool = False) -> None:
        file = self.GetHeaderFile()
        if self.LoadedHeader and not force:
            self.log.debug(f"Skipped loading {file}")
            return
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{filename}"
        if not os.path.exists(f"{path}/{file}"):
            self.LoadedHeader = True
            self.log.debug(f"No {file} file to load")
            return
        with open(f"{path}/{file}", 'r') as f:
            lines = f.readlines()
            self.SetName(lines[0].strip())
            year, month, day = lines[1].strip().split('-')
            self.SetDate( dt.date(int(year), int(month), int(day)) )
            self.SetDescription(lines[2].strip())
            self.SetLead(lines[3].strip())
            self.SetUUID(lines[4].strip())
        self.log.debug(f"Loaded {file}")
        self.LoadedHeader = True

    def LoadVersion(self, filename: str, force: bool = False) -> None:
        file = self.GetVersionFile()
        if self.LoadedVersion and not force:
            self.log.debug(f"Skipped loading {file}")
            return
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{filename}"
        if not os.path.exists(f"{path}/{file}"):
            self.LoadedVersion = True
            self.log.debug(f"No {file} file to load")
            return
        with open(f"{path}/{file}", 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=' ', quotechar='|')
            for row in reader:
                version = Version(row[0])
                cID = uuid.UUID(row[1])
                self.UpdateVersion(version, cID)
        self.log.debug(f"Loaded {file}")
        self.LoadedVersion = True