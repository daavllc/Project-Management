# Project-Management.gui.menu.menu - GUI menu start point/launcher
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

from .File import File
from .Edit import Edit
from .View import View
from .Help import Help

class Menu:
    def __init__(self, parent):
        self.parent = parent # gui.gui.Application
        with dpg.viewport_menu_bar():
            self.File = File(self)
            self.Edit = Edit(self)
            self.View = View(self)
            self.Help = Help(self)