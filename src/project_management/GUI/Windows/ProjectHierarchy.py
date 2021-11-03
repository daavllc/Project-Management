import dearpygui.dearpygui as dpg

class ProjectHierarchy:
    def __init__(self, parent):
        self.parent = parent
        with dpg.window(tag="ProjectHierarchy", label="Project Hierarchy", no_close=True):
            dpg.add_text(default_value="No projects found", tag="NoProjects")