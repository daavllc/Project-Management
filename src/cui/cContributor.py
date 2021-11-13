
import datetime

from common_types.base_types.version import Version
from common_types.contributor import Contributor
import config.config as config

import cui.utils as utils

class cContributor:
    def __init__(self, parent):
        self.ctr = None
        self.parent = parent

    def Menu(self):
        while True:
            utils.ClearScreen()
            print("\tMenu: CUI > Project > Contribution > Contributor > Menu")
            print(f"\Contributor: '{self.ctr.GetName()}'")
            print("\t===========================================================")
            self.ViewInfo()
            print("\t===========================================================")
            val = self.Command(input("\tEnter a command > "))
            match val:
                case -1:
                    return

    def Command(self, command: str) -> None:
        match command.split():
            case ['view']:
                self.mViewInfo()
            case ['edit'] | ['set']:
                self.mEditInfo()
            case ['push']:
                hours = ""
                date = ""
                desc = ""
                while True:
                    hours = input("Hours worked on addition > ")
                    date = input("Date worked on (YYYY-MM-DD|today) > ")
                    desc = input("Description of addition > ")
                    try:
                        hours = float(hours)
                        if date == "today":
                            date = datetime.datetime.now().date()
                        else:
                            date = date.split('-')
                            date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                        break
                    except ValueError:
                        print("invalid input")
                self.ctr.Push(hours, date, desc, self.parent.ctb.GetUUID())
            case ['load']:
                pass
            case ['export'] | ['save']:
                self.ctr.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}")
                print(f"Exported '{self.ctr.GetName()}'")
            case ["exit"] | ["close"]:
                exit(0)
            case ["reload"]:
                exit(-2)
            case ["return"] | ["menu"] | [".."]:
                return -1
            case ["help"]:
                print("\tCommands:")
                print("\t  help\n\t\tshow this menu")
                print("\t  view\n\t\tview contributor information")
                print("\t  edit\n\t\tedit contributor information")
                print("\t  push\n\t\tpush addition information")
                print("\t  export | save\n\t\texport contributor")
                print("\t  exit | close\n\t\texit Project-Management")
                print("\t  return | menu | ..\n\t\treturn to Contribution Menu")
                print("\t  reload\n\t\treload CUI")
                utils.Pause()
            case _:
                print("Unknown command! Type 'help' to view commands")
                utils.Pause()

    def ViewInfo(self):
        print(f"\tCreated on {self.ctr.GetDateStr()} ({(datetime.datetime.now().date() - self.ctr.GetDate()).days} days ago)")
        print(f"\tURL: {self.ctr.GetURL()}")

    def Set(self, name: str) -> None:
        self.ctr = Contributor()
        self.ctr.Import(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTORS}", name)

    def Create(self, name: str = None):
        if name == None:
            name = input("Enter contributor's name > ")
        self.ctr = Contributor()
        self.ctr.SetName(name=name)