# Project-Management.gui.menu.View - GUI View menu
# Copyright (C) 2021-2022  DAAV, LLC
# Language: Python 3.10

import dearpygui.dearpygui as dpg

class View:
    class ShowStatus:
        def __init__(self):
            self.ProjectExplorer = True
            self.ProjectContributions = True
            self.ProjectContributors = True
            self.ProjectProperty = True

            self.Menu_Debug = False

        def TogglePX(self):
            self.ProjectExplorer = not self.ProjectExplorer
            dpg.configure_item("ProjectExplorer", show=self.ProjectExplorer)

        def ToggleCtbX(self):
            self.ProjectContributions = not self.ProjectContributions
            dpg.configure_item("ContributionExplorer", show=self.ProjectContributions)

        def ToggleCtrX(self):
            self.ProjectContributors = not self.ProjectContributors
            dpg.configure_item("ContributorExplorer", show=self.ProjectContributors)

        def TogglePPX(self):
            self.ProjectProperty = not self.ProjectProperty
            dpg.configure_item("ProjectPropertyExplorer", show=self.ProjectProperty)

        def ToggleDebug(self):
            self.Menu_Debug = not self.Menu_Debug
            dpg.configure_item("Menu.Debug", show=self.Menu_Debug)

    def __init__(self, parent):
        self.parent = parent
        self.Status = self.ShowStatus()
        with dpg.menu(tag="Menu.View", label="View"):
            dpg.add_menu_item(tag="Menu.View.Refresh", label="Refresh", callback=self.parent.parent.Refresh)
            dpg.add_separator()
            with dpg.menu(tag="Menu.View.Appearence", label="Appearence"):
                dpg.add_menu_item(tag="Menu.View.Appearence.Fullscreen", label="Fullscreen")
                dpg.add_separator()
                with dpg.menu(tag="Menu.View.Appearence.Panels", label="Panels"):
                    dpg.add_checkbox(tag="Menu.View.Appearence.Panels.PX", label="Show Project Explorer", default_value=True, callback=self.Status.TogglePX)
                    dpg.add_checkbox(tag="Menu.View.Appearence.Panels.CtbX", label="Show Project Contributions",  default_value=True, callback=self.Status.ToggleCtbX)
                    dpg.add_checkbox(tag="Menu.View.Appearence.Panels.CtrX", label="Show Project Contributors",  default_value=True, callback=self.Status.ToggleCtrX)
                    dpg.add_checkbox(tag="Menu.View.Appearence.Panels.PPX", label="Show Project Property Explorer",  default_value=True, callback=self.Status.TogglePPX)
                with dpg.menu(tag="Menu.View.Appearence.Colors", label="Colors"):
                    dpg.add_menu_item(tag="Menu.View.Appearence.Colors.Default", label="Default")
                with dpg.menu(tag="Menu.View.Appearence.Text", label="Text"):
                    dpg.add_menu_item(tag="Menu.View.Appearence.Text.None", label="No options yet")
                with dpg.menu(tag="Menu.View.Appearence.Menus", label="Menus"):
                    dpg.add_checkbox(tag="Menu.View.Appearence.Menus.Debug", label="Show Debug Menu", default_value=False, callback=self.Status.ToggleDebug)
            with dpg.menu(tag="Menu.View.Appearence.Layout", label="Layout"):
                dpg.add_menu_item(tag="Menu.View.Appearence.Layout.Default", label="Default", callback=self.SetLayoutDefault)
                dpg.add_separator()
                dpg.add_menu_item(tag="Menu.View.Appearence.Layout.EasyDocking", label="Easy Docking (debug)", callback=self.SetLayoutEasyDocking)

    def SetLayoutDefault(self):
        dpg.configure_item("ProjectExplorer", pos=[0,0], width=250, height=720)
        dpg.configure_item("ContributionExplorer", pos=[250,0], width=250, height=350)
        dpg.configure_item("ContributorExplorer", pos=[250,370], width=250, height=350)
        dpg.configure_item("ProjectPropertyExplorer", pos=[500,0], width=780, height=720)
    def SetLayoutEasyDocking(self):
        dpg.configure_item("ProjectExplorer", pos=[900,50], width=200, height=100)
        dpg.configure_item("ContributionExplorer", pos=[900,200], width=200, height=100)
        dpg.configure_item("ContributorExplorer", pos=[900,400], width=200, height=100)
        dpg.configure_item("ProjectPropertyExplorer", pos=[900,600], width=200, height=100)
