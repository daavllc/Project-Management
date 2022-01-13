# Project-Management.gui.gui - Initialize dearpygui and launch the gui
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10
import sys
import dearpygui.dearpygui as dpg

import helpers as hp
from gui.events.events import Events
from gui.menu.menu import Menu
from gui.windows.windows import Windows

import config.config as config

class GUI:
    def Launch(self, manager):
        print("Launching GUI...")
        self._Start(manager)

    def _Start(self, manager):
        app = Application(manager)
        app.Run()

class Application:
    def __init__(self, manager):
        self.Width = 1280
        self.Height = 720

        self.log = hp.Logger("PM.GUI", "gui.log")
        self.manager = manager

    def Run(self):
        self.Setup()
        self.Runtime()
        self.Shutdown()

    def SaveInit(self):
        dpg.save_init_file(f"{config.PATH_ROOT}/settings/dpg.ini")
        self.log.debug("Saved window configuration")

    def ReloadGUI(self):
        self.log.debug("Reloading...")
        exit(-3)

    def ReloadCUI(self):
        self.log.debug("Reloading...")
        exit(-2)

    def Reload(self):
        self.log.debug("Reloading...")
        exit(-1)

    def Refresh(self):
        self.log.debug("Refreshing GUI...")
        self.Windows.Refresh()

    def Undo(self):
        self.manager.Undo()
        self.Refresh() # TODO: check performance

    def Redo(self):
        self.manager.Redo()
        self.Refresh() # TODO: check performance

    def Save(self):
        self.manager.Save()
        self.log.info("Saved!")
        self.Windows.Refresh()  # TODO: check performance

    def Setup(self):
        self.log.debug("Setting up context...")
        dpg.create_context()
        dpg.configure_app(docking=True, docking_space=True)
        dpg.configure_app(init_file=f"{config.PATH_ROOT}/settings/dpg.ini", load_init_file=True)
        dpg.create_viewport(title=f"Project Management {config.VERSION}", width=self.Width, height=self.Height, vsync=True, clear_color=[1, 0, 1, 1.0])
        dpg.setup_dearpygui()

    def Runtime(self):
        self.log.debug("Starting Runloop...")
        self.Events = Events(self)
        self.Menu = Menu(self)
        self.Windows = Windows(self)
        self.Windows.Refresh()

        dpg.set_primary_window("PrimaryWindow", True)
        dpg.show_viewport()
        dpg.start_dearpygui()

    def Shutdown(self):
        self.log.debug("Shutting down...")
        dpg.destroy_context()