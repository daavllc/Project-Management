import logging

import dearpygui.dearpygui as dpg

from .GUI.ViewportMenu.ViewportMenu import ViewportMenu
from .GUI.Windows.Windows import Windows

from .project import Project

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s <%(name)s> %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Management:
    def __init__(self):
        self.Version = "v0.0.1"
        self.projects = []
        self.selected = None

        self.log = logger
        self.log.debug("Initalized Management")

    def SaveInit(self):
        dpg.save_init_file("dpg.ini")
        self.log.debug("Saved window configuration")

    def uiSetup(self):
        self.log.debug("Setting up UI")
        dpg.create_context()
        dpg.configure_app(docking=True, docking_space=True)
        dpg.configure_app(init_file="dpg.ini", load_init_file=True)
        dpg.create_viewport(title=f"Project Management {self.Version}", width=1280, height=720, vsync=True, clear_color=[0.8, 0.2, 0.8, 1.0])
        dpg.setup_dearpygui()

    def uiRuntime(self):
        self.log.debug("Running UI")
        def Run():
            dpg.show_viewport()
            dpg.set_primary_window("MainWindow", True)
            while dpg.is_dearpygui_running(): # Render loop
                dpg.render_dearpygui_frame()
        self.ViewportMenu = ViewportMenu(self)
        with dpg.window(id="MainWindow", width=1280, height=720):
            self.Windows = Windows(self)
        Run()

    def Reload(self):
        self.log.debug("Reloading application")
        exit(-1)

    def uiShutdown(self):
        self.log.debug("Shutting down UI")
        dpg.destroy_context()

    def _AddColumn(self, sender, app_data, user_data):
        self.log.debug(f"Adding column '{app_data}'")
        self.projects[self.selected].Push(app_data)
        dpg.delete_item("pmAddColumnInput")
        dpg.delete_item("pmAddColumnSepatator")
        dpg.add_input_text(parent="ProjectManager", tag="pmAddColumnInput", hint="Add Column", on_enter=True, callback=self._AddColumn)
        dpg.add_separator(parent="ProjectManager", tag="pmAddColumnSepatator")

        self._DrawSelected()

    def _AddEntry(self, sender, app_data, user_data):
        self.log.debug(f"Adding entry to column")
        col = int(sender.split('_')[1])
        self.projects[self.selected].columns[col].Push(app_data)

        dpg.delete_item(f"pmEntryInput_{col}")
        dpg.delete_item(f"pmGroupColumn_{col}")
        dpg.delete_item(f"pmGroup_{col}")
        self._DrawSelected()

    def _UpdateSelected(self):
        def ProjectManager(self):
            dpg.delete_item("pmNoSelected")
            dpg.add_text(parent="ProjectManager", tag="pmSelectedName", default_value=self.projects[self.selected].name)
            dpg.add_separator(parent="ProjectManager", tag="pmSelectedSepatator")
            dpg.add_input_text(parent="ProjectManager", tag="pmAddColumnInput", hint="Add Column", on_enter=True, callback=self._AddColumn)
            dpg.add_separator(parent="ProjectManager", tag="pmAddColumnSepatator")
        def ProjectViewer(self):
            dpg.delete_item("pvNoSelected")
            dpg.add_text(parent="ProjectViewer", tag="pvSelectedName", default_value=self.projects[self.selected].name)
            dpg.add_separator(parent="ProjectViewer", tag="pvSelectedSepatator")
        ProjectManager(self)
        ProjectViewer(self)

    def _DrawSelected(self):
        def ProjectManager(self):
            for index in range(len(self.projects[self.selected].columns) - 1):
                dpg.delete_item(f"pmEntryInput_{index}")
                dpg.delete_item(f"pmGroupColumn_{index}")
                dpg.delete_item(f"pmGroup_{index}")
            index = 0
            for column in self.projects[self.selected].columns:
                with dpg.group(parent="ProjectManager", tag=f"pmGroup_{index}", horizontal=True):
                    dpg.add_text(tag=f"pmGroupColumn_{index}", default_value=column.name)
                    dpg.add_input_text(tag=f"pmEntryInput_{index}", hint="Add Entry", on_enter=True, callback=self._AddEntry)
                index += 1
        def ProjectViewer(self):
            try:
                dpg.delete_item("pvTable") # First time, this doesnt exist, so it's excepted
            except Exception as e:
                self.log.debug(str(e))
            with dpg.table(parent="ProjectViewer", tag="pvTable", header_row=True, row_background=True, resizable=True,
                            borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                for column in self.projects[self.selected].columns:
                    dpg.add_table_column(label=column.name)
                for x in range(self.projects[self.selected].GetLargestColumn()):
                    with dpg.table_row():
                        for y in range(len(self.projects[self.selected])):
                            dpg.add_text(str(self.projects[self.selected].Get(y, x)))
        ProjectManager(self)
        ProjectViewer(self)

    def _SelectProject(self, sender):
        self.selected = int(sender.split('_')[1])
        self._UpdateSelected()

    def _UpdateProjects(self):
        index = 0
        for index in range(len(self.projects) - 1):
            dpg.delete_item(f"Project{index}")
        for project in self.projects:
            dpg.add_button(parent="ProjectHierarchy", tag=f"Project_{index}", label=project.name, callback=self._SelectProject)
            index += 1

    def _AddProject(self, sender, app_data, user_data):
        if len(self.projects) == 0:
            dpg.delete_item("NoProjects")
        self.log.debug(f"Adding project '{app_data}'")
        self.projects.append(Project(app_data))
        dpg.delete_item("AddProjectInput")
        self._UpdateProjects()
        self.selected = len(self.projects) - 1
        self._UpdateSelected()

    def NewProject(self):
        dpg.add_input_text(parent="ProjectHierarchy", hint="Project Name", tag="AddProjectInput", on_enter=True, callback=self._AddProject)