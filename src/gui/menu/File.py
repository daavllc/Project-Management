# Project-Management.gui.menu.File - GUI File menu
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg
import sys
class File:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save", shortcut="CTRL + S", callback=lambda: self.parent.manager.Save())
            dpg.add_separator()
            with dpg.menu(label="Preferences"):
                dpg.add_menu_item(label="Settings")
                dpg.add_menu_item(label="Keyboard Shortcuts")
                dpg.add_menu_item(label="Color Theme")
            dpg.add_separator()
            dpg.add_menu_item(label="Exit", callback=lambda: sys.exit(0))