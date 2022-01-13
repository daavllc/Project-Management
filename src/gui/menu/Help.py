# Project-Management.gui.menu.Help - GUI Help menu
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg
import webbrowser

import config.config as config

class Help:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(label="Help"):
            dpg.add_menu_item(tag="Menu.Help.Documentation", label="Documentation", callback=lambda: dpg.configure_item("Menu.Help.Documentation.Popup", show=True))
            with dpg.window(tag="Menu.Help.Documentation.Popup", label="Documentation", modal=True, show=False):
                dpg.add_button(label="https://github.com/daavofficial/Project-Management/wiki", callback=lambda: webbrowser.open('https://github.com/daavofficial/Project-Management/wiki'))

            dpg.add_menu_item(tag="Menu.Help.Report", label="Report", callback=lambda: dpg.configure_item("Menu.Help.Report.Popup", show=True))
            with dpg.window(tag="Menu.Help.Report.Popup", label="About", modal=True, show=False):
                dpg.add_text(default_value=f"A menu should go here eventually.")

                dpg.add_button(label="https://github.com/daavofficial/Project-Management/issues", callback=lambda: webbrowser.open('https://github.com/daavofficial/Project-Management/issues'))
                
            dpg.add_separator()
            dpg.add_menu_item(tag="Menu.Help.About", label="About", callback=lambda: dpg.configure_item("Menu.Help.About.Popup", show=True))
            with dpg.window(tag="Menu.Help.About.Popup", label="About", modal=True, show=False):
                dpg.add_text(default_value=f"Project Mangement v{config.VERSION} by DAAV, LLC")
                with dpg.group(horizontal = True):
                    dpg.add_text(default_value=f"Source:")
                    dpg.add_button(label="https://github.com/daavofficial/Project-Management", callback=lambda: webbrowser.open('https://github.com/daavofficial/Project-Management'))
                dpg.add_separator()
                dpg.add_text(default_value=f"Manager v{config.VERSION_MANAGER}")
                dpg.add_text(default_value=f"GUI v{config.VERSION_GUI}")
