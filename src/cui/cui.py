# Project-Management.cui.cui - CUI start point/launcher
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import logging
import os

import cui.utils as utils
from cui.cProject import cProject
import config.config as config

class CUI:
    def __init__(self):
        self.parent = None

    def Launch(self, parent):
        self.parent = parent
        print("Launching CUI...")
        self._Start()

    def _Start(self):
        cPrj = cProject()
        projects = []
        for file in os.listdir(config.PATH_ROOT):
            if os.path.isdir(config.PATH_ROOT + "/" + file):
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
                        exit(-2)
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
