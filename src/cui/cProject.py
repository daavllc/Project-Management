# Project-Management.cui.cProject - CUI implementation of projects
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import datetime
import os

from common_types.base_types.version import Version
from common_types.project import Project
import config.config as config

from cui.cContribution import cContribution
import cui.utils as utils

class cProject:
    def __init__(self):
        self.prj = None
        self.cCtb = cContribution(self)

    def Menu(self):
        while True:
            utils.ClearScreen()
            print("\tMenu: CUI > Project > Menu")
            print(f"\tProject: '{self.prj.GetName()}'")
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
            case ['add']:
                contributions = []
                for file in os.listdir(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"):
                    if os.path.isdir(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"):
                        contributions.append(file)
                self.cCtb.Create(len(contributions))
                self.cCtb.Menu()
            case ['load']:
                contributions = []
                fNames = []
                for file in os.listdir(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"):
                    if os.path.isdir(f"{config.PATH_CURRENT_PROJECT}/{config.FOLDER_CONTRIBUTIONS}"):
                        contributions.append(file.split('. ')[1])
                        fNames.append(file)

                if len(contributions) == 0:
                    print("No contributions found, please use the command 'add' instead.")
                    utils.Pause()
                    return
                print("\t---- Available contributions ----")
                print("\t", end="")
                for index in range(len(contributions)):
                    print(str(index + 1) + ") " + contributions[index])
                print("\t---------------------------------")
                ctb = ""
                while True:
                    ctb = input("Please select a contribution > ")
                    if ctb == "exit":
                        return
                    try:
                        ctb = int(ctb)
                        if ctb > 0 and ctb <= len(contributions):
                            break
                    except ValueError as e:
                        print(f"Err: {e}")
                        print("Please input only integers")
                self.cCtb.Set(fNames[ctb - 1])
                self.cCtb.Menu()
            case ['export'] | ['save']:
                self.prj.Export(config.PATH_CURRENT_PROJECT)
                print(f"Exported '{self.prj.GetName()}'")
            case ['import']:
                projects = []
                for file in os.listdir(config.PATH_ROOT):
                    if os.path.isdir(config.PATH_ROOT + "/" + file):
                        projects.append(file)

                if len(projects) == 0:
                    print("No projects found, please export, or create new projects instead.")
                    utils.Pause()
                    return
                print("\t---- Available projects ----")
                print("\t", end="")
                print(*projects, sep=", ")
                print("\t----------------------------")
                prj = ""
                while True:
                    prj = input("Please select a project > ")
                    if prj == "exit":
                        return
                    if prj in projects:
                        break
                self.Set(config.PATH_ROOT, prj)
                return
            case ["exit"] | ["close"]:
                exit(0)
            case ['mainmenu'] | ['main', 'menu'] | ['main']:
                exit(-1)
            case ["reload"]:
                exit(-2)
            case ["return"] | ["menu"] | [".."]:
                return -1
            case ["help"]:
                print("\tCommands:")
                print("\t  help\n\t\tshow this menu")
                print("\t  view\n\t\tview project information")
                print("\t  edit\n\t\tedit project information")
                print("\t  add\n\t\tadd contribution")
                print("\t  load\n\t\tload contribution")
                print("\t  export | save\n\t\texport project")
                print("\t  import\n\t\timport project")
                print("\t  exit | close\n\t\tview project information")
                print("\t  main menu | main\n\t\treturn to CUI/GUI selection")
                print("\t  return | menu | ..\n\t\treturn to main CUI menu")
                print("\t  reload\n\t\treload CUI")
                utils.Pause()
            case _:
                print("Unknown command! Type 'help' to view commands")
                utils.Pause()

    def ViewInfo(self):
        print(f"\tCreated on {self.prj.GetDateStr()} ({(datetime.datetime.now().date() - self.prj.GetDate()).days} days ago)")
        print(f"\tProject Lead: {self.prj.GetLead()}, Version: {self.prj.GetVersionStr()}")
        print(f"\tDescription: {self.prj.GetDescription()}")

    def mViewInfo(self):
        while True:
            utils.ClearScreen()
            print("\tMenu: CUI > Project > Menu > View")
            print(f"\tProject: '{self.prj.GetName()}'")
            print("\t===========================================================")
            self.ViewInfo()
            print("\t===========================================================")
            command = input("\tWhat do you want to view? > ")
            match command.split():
                case ['return'] | [".."]:
                    return

    def mEditInfo(self):
        bSaved = False
        while True:
            utils.ClearScreen()
            print("\tMenu: CUI > Project > Menu > Edit")
            print(f"\tProject: '{self.prj.GetName()}'")
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
                            uinput = datetime.date(int(uinput[0]), int(uinput[1]), int(uinput[2]))
                            self.prj.SetDate(uinput)
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
                    self.prj.SetLead(uinput)
                    bSaved = False
                case ['version']:
                    while True:
                        uinput = input("Please enter a version (#.#.#) > ")
                        if uinput == "exit":
                            break
                        try:
                            uinput = Version(uinput)
                            self.prj.SetVersion(uinput)
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
                    self.prj.SetDescription(uinput)
                    bSaved = False
                case ['export'] | ['save']:
                    print(f"Saving changes to '{self.prj.GetName()}'...")
                    self.prj.Export(config.PATH_CURRENT_PROJECT)
                    bSaved = True
                case ['done']:
                    print(f"Saving changes to '{self.prj.GetName()}'...")
                    self.prj.Export(config.PATH_CURRENT_PROJECT)
                    return
                case ['exit'] | ['return'] | ['..']:
                    if not bSaved:
                        if not 'y' in input("Exit without saving? (y/N) > "):
                            print(f"Saving changes to '{self.prj.GetName()}'...")
                            self.prj.Export(config.PATH_CURRENT_PROJECT)
                            return
                    return
                case ['reload']:
                    exit(-2)
                case ["help"]:
                    print("\tCommands:")
                    print("\t  help\n\t\tshow this menu")
                    print("\t  date | created\n\t\tset creation date")
                    print("\t  lead\n\t\tset project lead")
                    print("\t  version\n\t\tset project version")
                    print("\t  desc\n\t\tset project description")
                    print("\t  export | save\n\t\tsave project changes")
                    print("\t  done\n\t\tsave project changes and return to Menu")
                    print("\t  exit | return | ..\n\t\treturn to Menu")
                    print("\t  reload\n\t\treload CUI")
                    utils.Pause()
                case _:
                    print("Unknown command!")
                    utils.Pause()

    def Set(self, path: str, name: str):
        self.prj = Project()
        self.prj.Import(path, name)

    def Create(self, name: str = None):
        if name == None:
            name = input("Enter the project name: ")
        self.prj = Project(name=name)
        config.PATH_CURRENT_PROJECT = f"{config.PATH_ROOT}/{name}"