# Project-Management.cui.cui - CUI start point/launcher
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import os

import cui.utils as utils
import helpers as hp
from cui.console.console import Console
import config.config as config

class CUI:
    def Launch(self):
        print("Launching CUI...")
        self._Start()

    def _Start(self):
        app = Application()
        app.Run()

class Application:
    def __init__(self):
        self.log = hp.Logger("PM.CUI", "cui.log", writeConsole=False)
        self.Width = 180
        self.Height = 45

    def Run(self):
        self.Setup()
        self.Runtime()
        self.Shutdown()

    def Setup(self):
        utils.SetConsoleSize(self.Width, self.Height)

    def Runtime(self):
        self.Console = Console(self)

        while True:
            self.Console.Refresh()

    def Shutdown(self):
        return

    def Reload(self):
        self.log.debug("Reloading...")
        exit(-1)

    def Old(self):
        cPrj = cProject()
        projects = []
        for file in os.listdir(config.PATH_ROOT):
            if os.path.isdir(config.PATH_ROOT + "/" + file):
                prj = Project()
                projects.append(file)

        while True:
            print("\t---- Available projects ----")
            print("\t", end="")
            if len(projects) > 0:
                print(*projects, sep=", ")
            else:
                print("No projects found")
            print("\t----------------------------")
            print("\tCommands: load (project), create, exit, return, reload, help")
            while True:

                command = input("\tEnter a command > ")
                match command.split():
                    case ["create"]:
                        cPrj.Create()
                        cPrj.Menu()
                        config.PATH_CURRENT_PROJECT = None
                    case ['load', *name]:
                        prj = ' '.join(name)
                        if prj in projects:
                            cPrj.Set(config.PATH_ROOT, prj)
                            cPrj.Menu()
                            config.PATH_CURRENT_PROJECT = None
                        else:
                            print("Invalid project")
                    case ["exit"] | ["close"]:
                        return
                    case ["return"] | ["menu"] | [".."]:
                        exit(-1)
                    case ["reload"]:
                        exit(-1)
                    case ["help"]:
                        print("\tCommands")
                        print("\t  help\n\t\tshows this menu")
                        print("\t  create\n\t\tcreate new project")
                        print("\t  load (project)\n\t\tload specified project")
                        print("\t  exit | close\n\t\texits Project-Management")
                        print("\t  return | menu | ..\n\t\treturn to main menu")
                        print("\t  reload\n\t\treload CUI")
                    case _:
                        print(" ERR: Unknown command, type 'help' to show commands")