import datetime as dt
from collections import namedtuple
import os

from objects.project import Project

import helpers as hp
import config.config as config

import cui.utils as utils
from cui.commands import CommandParse

class Console:
    class Size:
        def __init__(self):
            con = utils.GetConsoleSize()
            Size = namedtuple('Size', 'x y')
            self.console = Size(con[0], con[1] - 2) # one for horizontal sep, one for input line
            self.projects = Size(int(self.console.x / 4) - 3, self.console.y)
            self.header = Size(self.console.x - self.projects.x - 4, 2)
    def __init__(self, parent):
        self.parent = parent
        self.log = hp.Logger("PM.CUI.console", "cui.log", writeConsole=False)
        self.projects = []
        self.project = None

        self.size = self.Size()

    def Refresh(self):
        self.GetProjects()
        self.Draw()
        
    def SetProject(self, prj):
        if prj is None:
            config.PATH_CURRENT_PROJECT = None
            self.log.debug(f"Set self.project = None")
        else:
            self.project = prj
            self.log.debug(f"Set self.project = {self.project.GetUUIDStr()}")
    
    def Resize(self):
        self.size = self.Size()

    def Draw(self):
        cmd = CommandParse(name="Project-Management CUI", description="main cui interface", fallback="Unknown command")
        main = cmd.AddGroup(name="Window", description="commands that modifiy the cui, or reload")
        main.Add([['h'], ['help']], help="shows this message", callback=cmd.PrintHelp)
        main.Add([['reload']], help="reloads CUI", callback=lambda: exit(-2))
        main.Add([['resize']], help="resizes elements based on console size", callback=self.Resize)
        prj = cmd.AddGroup(name="Project Manager", description="select, edit and view projects")
        prj.Add([['c'], ['create']], help="create new project", callback=self.CreateProject)
        prj.Add([['l', '*'], ['load', '*']], help="loads specified project", callback=self.LoadProject)
        prj.Add([['set', 'prj', 'name', '*']], help="set project name to specified value", callback=self.SetProjectName)
        prj.Add([['set', 'prj', 'lead', '*']], help="set project lead to specified value", callback=self.SetProjectLead)
        prj.Add([['set', 'prj', 'date', '*']], help="set project date to specified value", callback=self.SetProjectDate)
        prj.Add([['set', 'prj', 'desc', '**']], help="set project description to specified value", callback=self.SetProjectDescription)
        while True:
            utils.ClearScreen()
            lines = []
            # Project Viewer (left side)
            lines.append(self.DrawProjects())
            lines.append(self.DrawVerticalSep(self.size.console.y))

            # Project Header (top)
            lines.append(self.DrawHeader())
            lines.append(self.DrawHorizontalSep(self.size.header.x, self.size.header.y + 1))

            for y in range(self.size.console.y - 1):
                line = ""
                for x in range(len(lines)):
                    if len(lines[x]) > y:
                        line += lines[x][y]
                print(line)
            print(utils.LeftAlign('-', self.size.console.x, '-'))
            cmd.Check()

    def DrawProjects(self) -> list[str]:
        retr = []
        width = self.size.projects.x
        retr.append(utils.CenterAlign('Projects', width))
        retr.append(utils.CenterAlign('--', width, fill='-'))
        if len(self.projects) == 0:
                retr.append(utils.LeftAlign(" No projects found", width))
        else:
            index = 0
            for prj in self.projects:
                line = f"{index + 1}) {prj.GetName()}"
                retr .append(" " + utils.LeftAlign(line, width - 1))
        if len(retr) > self.size.console.y:
            while len(retr) > self.size.console.y - 1:
                retr.pop()
            retr.append('...')
            return retr
        while len(retr) < self.size.console.y:
            retr.append(' ' * width)
        return retr

    def DrawHeader(self) -> list[str]:
        retr = []
        width = self.size.header.x
        if self.project is None:
            retr.append(utils.LeftAlign('No project selected', width))
            while len(retr) < self.size.header.y:
                retr.append(' ' * width)
            return retr

        retr.append(utils.LeftAlign(f"Project: '{self.project.GetName()}', Version: {self.project.GetVersionStr()}", width))
        retr.append(utils.LeftAlign(f"Lead: {self.project.GetLead()}, Created on: {self.project.GetDateStr()}", width))
        retr.append(utils.LeftAlign(f"Description: {self.project.GetDescription()}", width))
        return retr

    def DrawVerticalSep(self, height: int, sep: str = ' | ') -> list[str]:
        retr = []
        while len(retr) < height:
            retr.append(sep)
        return retr

    def DrawHorizontalSep(self, width: int, posY: int, sep: str = '-') -> list[str]:
        retr = []
        y = 0
        while len(retr) < self.size.console.y:
            if y == posY:
                retr.append(utils.LeftAlign(sep, width, sep))
            else:
                retr.append('')
            y += 1
        return retr

    def CreateProject(self):
        prj = Project()
        prj.SetName("New Project")
        prj.Export()
        self.projects.append(prj)

    def LoadProject(self, args):
        for prj in self.projects:
            if prj.GetName() == args[0]:
                self.SetProject(prj)

    def GetProjects(self):
        self.projects = []
        for file in os.listdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}"):
            if os.path.isdir(f"{config.PATH_ROOT}/{config.FOLDER_PROJECTS}/{file}"):
                prj = Project()
                prj.LoadHeader(file)
                self.projects.append(prj)
        for prj in self.projects:
            print(f"Got project {prj.GetName()} : {prj.GetUUIDStr()}")
        utils.Pause()

    def SetProjectName(self, args):
        self.project.SetName(args[0])
        self.project.SaveHeader()

    def SetProjectLead(self, args):
        self.project.SetLead(args[0])
        self.project.SaveHeader()

    def SetProjectDate(self, args):
        date = None
        try:
            date = args[0].split('-')
            date = dt.date(int(date[0]), int(date[1]), int(date[2]))
            self.parent.project.SetDate(date)
            self.parent.project.Export()
            self.parent.Refresh()
        except IndexError:
            pass
        except ValueError:
            pass

    def SetProjectDescription(self, args):
        desc = ""
        for idx, arg in args:
            desc += arg
            if not idx == len(args) - 1:
                desc += " "
        self.project.SetDescription(desc)
        self.project.SaveHeader()


