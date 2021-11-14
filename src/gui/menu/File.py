# Project-Management.gui.menu.File - GUI File menu
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

class File:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="New Project")
            dpg.add_separator()
            dpg.add_menu_item(label="Open Project")
            dpg.add_separator()
            dpg.add_menu_item(label="Save Project")
            dpg.add_menu_item(label="Save Project As")