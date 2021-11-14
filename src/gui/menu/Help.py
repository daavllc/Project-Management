# Project-Management.gui.menu.Help - GUI Help menu
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

class Help:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="Welcome")
            dpg.add_menu_item(label="Do something")