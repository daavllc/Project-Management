import dearpygui.dearpygui as dpg

class ProjectViewer:
    def __init__(self, parent):
        self.parent = parent
        with dpg.window(tag="ProjectViewer", label="Project Viewer", no_close=True):
            dpg.add_text(default_value="No project selected", tag="pvNoSelected")