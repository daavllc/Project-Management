
import logging

import dearpygui.dearpygui as dpg

from gui.logger import Logger
from gui.menu.menu import Menu
from gui.windows.windows import Windows

import config.config as config

class GUI:
    def __init__(self):
        self.parent = None

    def Launch(self, parent):
        self.parent = parent
        print("Launching GUI...")
        self._Start()

    def _Start(self):
        app = Application()

        app.uiSetup()
        app.uiRuntime()
        app.uiShutdown()

class Application:
    def __init__(self):
        self.Width = 1280
        self.Height = 720
        self.selected = None

        self.log = Logger("PM")

    def SaveInit(self):
        dpg.save_init_file("dpg.ini")
        self.log.debug("Saved window configuration")

    def Reload(self):
        self.log.debug("Reloading...")
        exit(-3)

    def uiSetup(self):
        self.log.debug("Setting up context...")
        dpg.create_context()
        dpg.configure_app(docking=True, docking_space=True)
        dpg.configure_app(init_file="dpg.ini", load_init_file=True)
        dpg.create_viewport(title=f"Project Management {config.VERSION}", width=self.Width, height=self.Height, vsync=True, clear_color=[1, 0, 1, 1.0])
        dpg.setup_dearpygui()

    def uiRuntime(self):
        self.log.debug("Starting Runloop...")
        def Run():
            dpg.show_viewport()
            dpg.set_primary_window("MainWindow", True)
            while dpg.is_dearpygui_running():
                dpg.render_dearpygui_frame()
        self.Menu = Menu(self)
        with dpg.window(id="MainWindow", width=1280, height=720):
            self.Window = Windows(self)
        Run()

    def uiShutdown(self):
        self.log.debug("Shutting down...")
        dpg.destroy_context()