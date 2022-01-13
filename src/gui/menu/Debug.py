import dearpygui.dearpygui as dpg
import sys

class Debug:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(tag="Menu.Debug", label="Debug", show=True):
            dpg.add_menu_item(label="Log Undo/Redo History", callback=lambda: self.parent.manager.History())
            dpg.add_separator()
            dpg.add_menu_item(label="Reload GUI", callback=lambda: self.parent.parent.ReloadGUI())
            dpg.add_menu_item(label="Reload CUI", callback=lambda: self.parent.parent.ReloadCUI())
            dpg.add_menu_item(label="Reload Project-Management", callback=lambda: self.parent.parent.Reload())