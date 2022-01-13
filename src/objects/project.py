# Project-Management.objects.project - Implementation of Project header
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import datetime as dt
import os
import uuid

import helpers as hp
from .base_types.version import Version
from .contribution import Contribution
from .contributor import Contributor
import config.config as config

if __name__ == "__main__":
    exit()

class Project:
    def __init__(self, name: str = 'Default Project', date: dt.date = dt.date.today(), desc: str = 'None', lead: list[str, uuid.UUID] = 'None'):
        self.log = hp.Logger("PM.Project", "objects.log")
        self.Header = dict(
            name = name, # str
            date = date, # dt.date
            desc = desc, # str
            lead = lead, # Contributor
            uuid = uuid.uuid4()
        )
        self.Version: list[list[Version, uuid.UUID]] = [Version(0, 0, 0)] # index 0 is total version

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
        self.Header['name'] = name

    def SetDate(self, date: dt.date) -> None:
        self.Header['date'] = date

    def SetDescription(self, desc: str) -> None:
        self.Header['desc'] = desc

    def SetLead(self, ctrName: str, ctrUUID: uuid.UUID) -> None:
        self.Header['lead'] = [ctrName, ctrUUID]

    def SetUUID(self, uid: str) -> None:
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

    def GetLead(self) -> list[str, uuid.UUID]:
        return self.Header.get('lead')
    def GetLeadName(self) -> str:
        return self.GetLead()[0]
    def GetLeadUUID(self) -> uuid.UUID:
        return self.GetLead()[1]

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
    def SetCurrent(self) -> None:
        config.PATH_CURRENT_PROJECT = f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{self.GetUUIDStr()}"
        self.log.debug(f"Set {config.PATH_CURRENT_PROJECT = }")

    def UpdateVersion(self, ver: Version, cID: uuid.UUID) -> None:
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