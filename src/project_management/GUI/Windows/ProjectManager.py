import dearpygui.dearpygui as dpg

class ProjectManager:
    def __init__(self, parent):
        self.parent = parent
        with dpg.window(tag="ProjectManager", label="Project Manager", no_close=True):
            dpg.add_text(default_value="No project selected", tag="pmNoSelected")