import dearpygui.dearpygui as dpg

class Edit:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(label="Edit"):
            dpg.add_menu_item(label="Save Window Configuration", callback=lambda: self.parent.parent.SaveInit())
            dpg.add_separator()
            dpg.add_menu_item(label="Reload Application", callback=lambda: self.parent.parent.Reload())