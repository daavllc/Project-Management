# Project-Management.gui.gui - Initialize dearpygui and launch the gui
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

import helpers as hp
from gui.menu.menu import Menu
from gui.windows.windows import Windows

import config.config as config

class GUI:
    def Launch(self):
        print("Launching GUI...")
        self._Start()

    def _Start(self):
        app = Application()
        app.Run()

class Application:
    def __init__(self):
        self.Width = 1280
        self.Height = 720

        self.log = hp.Logger("PM.GUI", "gui.log")

    def Run(self):
        self.Setup()
        self.Runtime()
        self.Shutdown()

    def SaveInit(self):
        dpg.save_init_file(f"{config.PATH_ROOT}/dpg.ini")
        self.log.debug("Saved window configuration")

    def Reload(self):
        self.log.debug("Reloading...")
        exit(-3)

    def Setup(self):
        self.log.debug("Setting up context...")
        dpg.create_context()
        dpg.configure_app(docking=True, docking_space=True)
        dpg.configure_app(init_file=f"{config.PATH_ROOT}/dpg.ini", load_init_file=True)
        dpg.create_viewport(title=f"Project Management {config.VERSION}", width=self.Width, height=self.Height, vsync=True, clear_color=[1, 0, 1, 1.0])
        dpg.setup_dearpygui()

    def Runtime(self):
        self.log.debug("Starting Runloop...")
        self.Menu = Menu(self)
        self.Windows = Windows(self)
        self.Windows.Refresh()

        #dpg.set_primary_window("MainWindow", True)
        dpg.show_viewport()
        dpg.start_dearpygui()
        
        #while dpg.is_dearpygui_running(): # Runloop
        #    dpg.render_dearpygui_frame()

    def Shutdown(self):
        self.log.debug("Shutting down...")
        dpg.destroy_context()