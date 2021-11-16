# Project-Management.objects.project - Implementation of Project header
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

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
    def __init__(self, name: str = 'None', date: hp.Date = hp.Date.Today(), desc: str = 'None', lead: str = 'None', version: Version = 'None'):
        self.log = hp.Logger("PM.Project", "objects.log")
        self.Info = {
            'name' : name,
            'date' : date,
            'desc' : desc,
            'lead' : lead,
            'version' : version,
            'uuid' : uuid.uuid4()
        }
        # Serialization
        self.Files = {
            'info' : 'header.inf'
        }
        self.LoadedHeader = False
        self.SavedHeader = False

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
    #               self.Info get/Get
    # ---============================================================---
    # Setters
    def SetName(self, name: str) -> None:
        self.SavedHeader = False
        self.Info['name'] = name

    def SetDate(self, date: hp.Date) -> None:
        self.SavedHeader = False
        self.Info['date'] = date

    def SetDescription(self, desc: str) -> None:
        self.SavedHeader = False
        self.Info['desc'] = desc

    def SetLead(self, lead: str) -> None:
        self.SavedHeader = False
        self.Info['lead'] = lead

    def SetVersion(self, version: Version) -> None:
        self.SavedHeader = False
        self.Info['version'] = version

    def SetUUID(self, uid: str) -> None:
        self.SavedHeader = False
        self.Info['uuid'] = uuid.UUID(uid)

    # Getters
    def GetName(self) -> str:
        return self.Info.get('name')

    def GetDate(self) -> hp.Date:
        return self.Info.get('date')
    def GetDateStr(self) -> str:
        return str(self.GetDate())

    def GetDescription(self) -> str:
        return self.Info.get('desc')

    def GetLead(self) -> str:
        return self.Info.get('lead')

    def GetVersion(self) -> Version:
        return self.Info.get('version')
    def GetVersionStr(self) -> str:
        return str(self.GetVersion())

    def GetUUID(self) -> uuid.UUID:
        return self.Info.get('uuid')
    def GetUUIDStr(self) -> str:
        return str(self.GetUUID())

    # ---============================================================---
    #               Helpers
    # ---============================================================---
    def GetInfoFile(self) -> str:
        return self.Files.get('info')

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
        contributions = sorted(contributions, key=lambda ctb: ctb.GetNumber())
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

    def SaveHeader(self, force: bool = False) -> None:
        file = self.GetInfoFile()
        if self.SavedHeader and not force:
            self.log.debug(f"Skipped saving {file}")
            return
        path = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{self.GetUUIDStr()}"
        with open(f"{path}/{file}", 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetDescription() + "\n")
            f.write(self.GetLead() + "\n")
            f.write(self.GetVersionStr() + "\n")
            f.write(self.GetUUIDStr() + "\n")
        self.log.debug(f"Saved {file}")
        self.SavedHeader = True

    # Import
    def Import(self, filename: str, force: bool = False) -> None:
        self.LoadHeader(filename, force)

        config.PATH_CURRENT_PROJECT = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{filename}"
        self.log.debug(f"Set {config.PATH_CURRENT_PROJECT = }")

    def LoadHeader(self, filename: str, force: bool = False) -> None:
        file = self.GetInfoFile()
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
            self.SetDate( hp.Date.Set(int(year), int(month), int(day)) )
            self.SetDescription(lines[2].strip())
            self.SetLead(lines[3].strip())
            self.SetVersion(Version(lines[4].strip()))
            self.SetUUID(lines[5].strip())
        self.log.debug(f"Loaded {file}")
        self.LoadedHeader = True