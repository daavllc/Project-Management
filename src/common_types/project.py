# Project-Management.base_types.project - Implementation of Project header
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import csv
import os
import datetime
import uuid

from .base_types.version import Version
from .contribution import Contribution
from .contributor import Contributor
import config.config as config

if __name__ == "__main__":
    exit(-1)

class Project:
    def __init__(self, name: str = 'None', date: datetime.date = datetime.datetime.now().date(), desc: str = 'None', lead: str = 'None', version: Version = 'None'):
        self.Info = {
            'name' : name,
            'date' : date,
            'desc' : desc,
            'lead' : lead,
            'version' : version,
            'uuid' : uuid.uuid4()
        }
        self.LoadedHeader = False

    # ---============================================================---
    #               Operation overloads
    # ---============================================================---
    def __str__(self) -> str:
        return f"'{self.GetName()}' created on {self.GetDateStr()}"

    def __repr__(self) -> str:
        retr = f"'{self.GetName()}' : {self.GetUUIDStr()}\n"
        retr += f"Created on {self.GetDateStr()}, Version {self.GetVersionStr()}\n"
        retr += f"Lead by {self.GetLead()}\n"

    # ---============================================================---
    #               self.Info get/Get
    # ---============================================================---
    # Setters
    def SetName(self, name: str) -> None:
        self.Info['name'] = name

    def SetDate(self, date: datetime.date) -> None:
        self.Info['date'] = date

    def SetDescription(self, desc: str) -> None:
        self.Info['desc'] = desc

    def SetLead(self, lead: str) -> None:
        self.Info['lead'] = lead

    def SetVersion(self, version: Version) -> None:
        self.Info['version'] = version

    def SetUUID(self, uid: str) -> None:
        self.Info['uuid'] = uuid.UUID(uid)

    # Getters
    def GetName(self) -> str:
        return self.Info.get('name')

    def GetDate(self) -> datetime.date:
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
    def AddContribution(self) -> Contribution:
        ctb = Contribution()
        ctb.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}")
    def GetContributions(self) -> list[str]:
        path = config.PATH_CURRENT_PROJECT + "/" + config.FOLDER_CONTRIBUTIONS

        contributions = []
        for file in os.listdir(path):
            if os.path.isdir(path + "/" + file):
                contributions.append(file)
        return contributions

    def InitContribution(self, name: str) -> Contribution:
        path = config.PATH_CURRENT_PROJECT + "/" + config.FOLDER_CONTRIBUTIONS
        if os.path.exists(path + "/" + name):
            ctb = Contribution()
            ctb.Import(path, name)
            return ctb
        else: # This means the contribution does not exist, what?
            print(f"Creating new contribution '{name}'")
            ctb = Contribution()
            ctb.SetName(name)
            ctb.SetDate(datetime.datetime.now().date())
            return ctb

    def GetContributionInfo(self, name: str) -> Contribution:
        path = config.PATH_CURRENT_PROJECT + "/" + config.FOLDER_CONTRIBUTIONS
        ctb = Contribution()
        ctb.Import(path, name)
        return ctb

    # ---============================================================---
    #               Serialization
    # ---============================================================---
    def Export(self) -> None:
        path = config.PATH_ROOT
        if not os.path.exists(path):
            os.mkdir(path)

        path = f"{path}/{self.GetUUIDStr()}"
        if not os.path.exists(path):
            os.mkdir(path)

        with open(f"{path}/header.inf", 'w') as f:
            f.write(self.GetName() + "\n")
            f.write(self.GetDateStr() + "\n")
            f.write(self.GetDescription() + "\n")
            f.write(self.GetLead() + "\n")
            f.write(self.GetVersionStr() + "\n")
            f.write(self.GetUUIDStr() + "\n")

        if not os.path.exists(f"{path}/{config.FOLDER_CONTRIBUTIONS}"):
            os.mkdir(f"{path}/{config.FOLDER_CONTRIBUTIONS}")
        if not os.path.exists(f"{path}/{config.FOLDER_CONTRIBUTORS}"):
            os.mkdir(f"{path}/{config.FOLDER_CONTRIBUTORS}")

    def Import(self, filename: str) -> None:
        path = config.PATH_ROOT
        if not self.LoadedHeader:
            self.LoadHeader(filename)
        config.PATH_CURRENT_PROJECT = f"{path}/filename"

    def LoadHeader(self, filename: str) -> None:
        path = f"{config.PATH_ROOT}/{filename}"
        with open(f"{path}/header.inf", 'r') as f:
            lines = f.readlines()
            self.SetName(lines[0].strip())
            date = lines[1].strip().split('-')
            self.SetDate(datetime.date(int(date[0]), int(date[1]), int(date[2])))
            self.SetDescription(lines[2].strip())
            self.SetLead(lines[3].strip())
            self.SetVersion(Version(lines[4].strip()))
            self.SetUUID(lines[5].strip())
        self.LoadedHeader = True