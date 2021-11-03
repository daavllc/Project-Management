import dearpygui.dearpygui as dpg

class Help:
    def __init__(self, parent):
        self.parent = parent
        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="Welcome")
            dpg.add_menu_item(label="Do something")