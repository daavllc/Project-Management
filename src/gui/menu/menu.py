# Project-Management.gui.menu.menu - GUI menu start point/launcher
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

import helpers as hp
from .File import File
from .Edit import Edit
from .View import View
from .Help import Help
from .Debug import Debug

class Menu:
    def __init__(self, parent):
        self.parent = parent # gui.gui.Application
        self.manager = self.parent.manager # manager.manager
        self.log = hp.Logger("PM.GUI.Menu", "gui.log")

        with dpg.viewport_menu_bar():
            self.File = File(self)
            self.Edit = Edit(self)
            self.View = View(self)
            self.Help = Help(self)
            self.Debug = Debug(self)