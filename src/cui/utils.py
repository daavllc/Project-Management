# Project-Management.cui.utils - CUI helpful functions
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10
import os

def ClearScreen():
    if 'nt' in os.name:
        os.system('cls')
    else:
        os.system('clear')

def Pause():
    input("Press enter to continue...")

def LeftAlign(text: str, width: int, fill: str = ' ') -> str:
    if len(text) > width:
        text = text[:width - 3] + '...'
        return text
        return text
    while len(text) < width:
        text += fill
    return text

def RightAlign(text: str, width: int, fill: str = ' ') -> str:
    if len(text) > width:
        text = text[:width - 3] + '...'
        return text
    while len(text) < width:
        text = fill + text
    return text

def CenterAlign(text: str, width: int, fill: str = ' ') -> str:
    if len(text) > width:
        text = text[:width - 3] + '...'
        return text
    while len(text) < width:
        text = fill + text + fill
    if len(text) > width:
        text = text[:-1]
    return text


def SetConsoleSize(width: int, height: int):
    if 'nt' in os.name:
        pass
        #os.system(f'mode con: cols={width} lines={height}')
    else:
        print("Uh oh! failed to set console size") # TODO: support Linux

def GetConsoleSize() -> list[int, int]:
    from shutil import get_terminal_size
    size = get_terminal_size(fallback=(-1, -1))
    return [size[0], size[1]]