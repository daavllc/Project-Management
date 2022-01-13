import dearpygui.dearpygui as dpg
from enum import Enum

import helpers as hp

class KeyStatus(Enum):
    NONE = 0
    DOWN = 1
    PRESSED = 2
    RELEASE = 3

class Events:
    # i looooooove dpg :))))))))))))))
    def __init__(self, parent):
        self.parent = parent # gui.gui
        self.log = hp.Logger("PM.GUI.Events", "gui.log")
        self.status: dict = {}

        with dpg.handler_registry():
            dpg.add_key_down_handler(callback=self.CheckKeys)
            dpg.add_key_press_handler(callback=self.CheckKeys)
            dpg.add_key_release_handler(callback=self.CheckKeys)

    def CheckKeys(self, sender, app_data):
        
        if sender == 22:
            self.status[str(app_data[0])] = self.GetStatus(sender)
        elif sender in {23, 24}:
            self.status[str(app_data)] = self.GetStatus(sender)

        if self.status.get(str(dpg.mvKey_Control)) == KeyStatus.DOWN:
            if self.status.get(str(dpg.mvKey_S)) == KeyStatus.PRESSED:
                self.parent.Save()



 
    def GetStatus(self, status: int):
        if status == 22:
            return KeyStatus.DOWN
        elif status == 23:
            return KeyStatus.PRESSED
        elif status == 24:
            return KeyStatus.RELEASE
