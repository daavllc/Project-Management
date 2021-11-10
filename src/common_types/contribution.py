# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python 3.10
# License: GPLv3
if __name__ == "__main__":
    exit(-1)

import datetime
import uuid

from .contributor import Contributor
class Contribution:
    def __init__(self, name: str = None, date: datetime.date = None, number: str = None, desc: str = None, lead: str = None, change: str = None, progress: str = None):
        self.Info = {
            'name' : name,         # Name of the contribution
            'date' : date,         # Contribution creation date
            'number' : number,     # Contribution number in relation to the project: 01, 02, 03...
            'desc' : desc,         # Description of the contribution
            'lead' : lead,         # Name of Contribution Lead
            'vChange' : change,    # Project version change because this contribution
            'progress' : progress, # Current contribution progress: 0.0-100.0
            'uuid' : uuid.uuid4()  # Contribution UUID -> don't touch
        }

        self.Contributors = {}

    # ---============================================================---
    #               self.Info get/set
    # ---============================================================---
    def SetName(self, name: str) -> None:
        self.Info['name'] = name

    def SetNumber(self, number: str) -> None:
        self.Info['number'] = number

    def SetDescription(self, desc: str) -> None:
        self.Info['desc'] = desc

    def SetLead(self, contributor: str) -> None:
        self.Info['lead'] = contributor

    def SetVersionChange(self, change: str) -> None:
        self.Info['vChange'] = change

    def SetCurrentProgress(self, progress: float) -> None:
        self.Info['progress'] = progress

    def AddContributor(self, name: str) -> None:
        self.Contributors[name] = Contributor(name)

    def GetContributor(self, name: str) -> Contributor:
        self.Contributors.get(name, None)

    # ---============================================================---
    #               Helpers
    # ---============================================================---