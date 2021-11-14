# Project-Management.cui.utils - CUI helpful functions
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

def ClearScreen():
    import os
    if 'nt' in os.name:
        os.system('cls')
    else:
        os.system('clear')

def Pause():
    input("Press enter to continue...")