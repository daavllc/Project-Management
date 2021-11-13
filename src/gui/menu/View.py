import dearpygui.dearpygui as dpg

class View:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(label="View"):
            with dpg.menu(label="Appearence"):
                dpg.add_checkbox(label="Show Project Hierarchy",    default_value=True)
                dpg.add_checkbox(label="Show/Hide Project Manager", default_value=True)
                dpg.add_checkbox(label="Show/Hide Project Viewer",  default_value=True)