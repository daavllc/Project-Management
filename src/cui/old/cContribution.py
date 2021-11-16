# Project-Management.cui.cContribution - CUI interface for project contributions
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import datetime as dt

from objects.base_types.version import Version
from objects.contribution import Contribution
import config.config as config

from .cContributor import cContributor
import cui.utils as utils

class cContribution:
    def __init__(self, parent):
        self.ctb = None
        self.parent = parent
        self.cCtr = cContributor(self)

    def Menu(self):
        while True:
            utils.ClearScreen()
            print("\tMenu: CUI > Project > Contribution > Menu")
            print(f"\tContribution: '{self.ctb.GetName()}'")
            print("\t===========================================================")
            self.ViewInfo()
            print("\t===========================================================")
            val = self.Command(input("\tEnter a command > "))
            match val:
                case -1:
                    return

    def Command(self, command: str) -> int:
        match command.split():
            case ['view']:
                self.mViewInfo()
            case ['view', *args]:
                print("view ", end="")
                print(*args, sep=", ")
            case ['edit'] | ['set']:
                self.mEditInfo()
            case ['add']:
                self.cCtr.Create()
                self.cCtr.Menu()
                self.ctb.AddContributor(self.cCtr.ctr.GetName(), self.cCtr.ctr.GetUUID())
            case ['load']:
                contributors = self.ctb.GetContributors()
                ctrList = []

                if len(contributors) == 0:
                    print("No contributors found, please use the command 'add' instead.")
                    utils.Pause()
                    return
                print("\t---- Available contributors ----")
                print("\t", end="")
                num = 1
                for key in contributors.keys():
                    print(str(num) + ") " + key)
                    ctrList.append(key)
                print("\t--------------------------------")
                ctr = ""
                while True:
                    ctr = input("Please select a contributors > ")
                    if ctr == "exit":
                        return
                    try:
                        ctr = int(ctr)
                        if ctr > 0 and ctr <= len(contributors):
                            break
                    except ValueError as e:
                        print(f"Err: {e}")
                        print("Please input only integers")
                self.cCtr.Set(ctrList[ctr - 1])
                self.cCtr.Menu()
            case ['export'] | ['save']:
                self.ctb.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}")
                print(f"Exported '{self.ctb.GetName()}'")
            case ['import']:
                print("import")
            case ["exit"] | ["close"]:
                exit(0)
            case ['mainmenu'] | ['main', 'menu'] | ['main']:
                exit(-1)
            case ["reload"]:
                exit(-2)
            case ["return"] | ["project"] | [".."]:
                return - 1
            case ["help"]:
                print("\tCommands:")
                print("\t  help\n\t\tshow this menu")
                print("\t  view\n\t\tview contribution information")
                print("\t  edit\n\t\tedit contribution information")
                print("\t  add\n\t\tadd contribution")
                print("\t  export | save\n\t\texport contribution")
                print("\t  import\n\t\timport contribution")
                print("\t  exit | close\n\t\tview contribution information")
                print("\t  main menu | main\n\t\treturn to project menu")
                print("\t  return | project | ..\n\t\treturn to main CUI menu")
                print("\t  reload\n\t\treload CUI")
                utils.Pause()
            case _:
                print("Unknown command! Type 'help' to view commands")
                utils.Pause()

    def ViewInfo(self):
        print(f"\tCreated on {self.ctb.GetDateStr()} ({(dt.date.today() - self.ctb.GetDate()).days} days ago)")
        print(f"\tContribution Lead: {self.ctb.GetLead()}, Contribution #{self.ctb.GetNumber()}, Version change: {self.ctb.GetVersionChangeStr()}")
        print(f"\tDescription: {self.ctb.GetDescription()}")

    def mViewInfo(self):
        while True:
            utils.ClearScreen()
            print("\tMenu: CUI > Project > Contribution > Menu > View")
            print(f"\Contribution: '{self.ctb.GetName()}'")
            print("\t===========================================================")
            self.ViewInfo()
            print("\t===========================================================")

    def mEditInfo(self):
        bSaved = False
        while True:
            utils.ClearScreen()
            print("\tMenu: CUI > Project > Contribution > Menu > Edit")
            print(f"\Contribution: '{self.ctb.GetName()}'")
            print("\t===========================================================")
            self.ViewInfo()
            print("\t===========================================================")
            command = input("\tWhat do you want to edit? > ")
            match command.split():
                case ['created'] | ['date'] | ['created', 'on']:
                    while True:
                        uinput = input("Please enter a date (YYYY-MM-DD) > ")
                        if uinput == "exit":
                            break
                        try:
                            uinput = uinput.split('-')
                            uinput = dt.date(int(uinput[0]), int(uinput[1]), int(uinput[2]))
                            self.ctb.SetDate(uinput)
                            bSaved = False
                            break
                        except IndexError as e:
                            print("Err: " + str(e))
                            print("Please follow the supplied format")
                        except TypeError as e:
                            print("Err: " + str(e))
                            print("Only input integers separated by '-'")
                case ['lead']:
                    uinput = input("Enter the Project lead's name > ")
                    self.ctb.SetLead(uinput)
                    bSaved = False
                case ['version']:
                    while True:
                        uinput = input("Please enter a version (#.#.#) > ")
                        if uinput == "exit":
                            break
                        try:
                            uinput = Version(uinput)
                            self.ctb.SetVersionChange(uinput)
                            bSaved = False
                            break
                        except Version.Errors.InvalidInitializationArgs as e:
                            print("Err: " + str(e))
                            print("Please follow the supplied format")
                        except Version.Errors.InvalidVersionString as e:
                            print("Err: " + str(e))
                            print("Only input integers separated by '.'")
                case ['desc'] | ['description']:
                    uinput = input("Enter the Project's description > ")
                    self.ctb.SetDescription(uinput)
                    bSaved = False
                case ['export'] | ['save']:
                    print(f"Saving changes to '{self.ctb.GetName()}'...")
                    self.ctb.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}")
                    bSaved = True
                case ['done']:
                    print(f"Saving changes to '{self.ctb.GetName()}'...")
                    self.ctb.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}")
                    return
                case ['exit'] | ['return'] | ['..']:
                    if not bSaved:
                        if not 'y' in input("Exit without saving? (y/N) > "):
                            print(f"Saving changes to '{self.prj.GetName()}'...")
                            self.ctb.Export(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}")
                            return
                    return
                case ['reload']:
                    exit(-2)
                case ["help"]:
                    print("\tCommands:")
                    print("\t  help\n\t\tshow this menu")
                    print("\t  date | created\n\t\tset creation date")
                    print("\t  lead\n\t\tset contribution lead")
                    print("\t  version\n\t\tset contribution version change")
                    print("\t  desc\n\t\tset contribution description")
                    print("\t  export | save\n\t\tsave contribution changes")
                    print("\t  done\n\t\tsave contribution changes and return to Menu")
                    print("\t  exit | return | ..\n\t\treturn to Menu")
                    print("\t  reload\n\t\treload CUI")
                    utils.Pause()
                case _:
                    print("Unknown command!")
                    utils.Pause()

    def Set(self, name: str):
        self.ctb = Contribution()
        self.ctb.Import(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}", name)

    def Create(self, number: int, name: str = None):
        if name == None:
            name = input("Enter the contribution name: ")
        self.ctb = Contribution(name=name)
        self.ctb.SetName(name)
        number = input(f"Please enter contribution number (00{number}) > ")
        self.ctb.SetNumber(number)