# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python 3.10
# License: MIT
## Project-Management
# Easy to use GUI/CUI for managing projects
# Copyright (C) 2021-2022 DAAV, LLC
##########################################################
# Project Lead: Anonoei (https://github.com/Anonoei)

import argparse
import sys

import interface
import config.config as config

def main():
    parser = argparse.ArgumentParser(add_help=True, description="Easy to use GUI/CUI for managing projects")
    parser.add_argument("-UI", help="specify user interface to use", choices=['CUI', 'GUI'])
    print("    ____               _           __     __  ___                                                  __ ")
    print("   / __ \_________    (_)__  _____/ /_   /  |/  /___ _____  ____ _____ ____  ____ ___  ___  ____  / /_")
    print("  / /_/ / ___/ __ \  / / _ \/ ___/ __/  / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ __ `__ \/ _ \/ __ \/ __/")
    print(" / ____/ /  / /_/ / / /  __/ /__/ /_   / /  / / /_/ / / / / /_/ / /_/ /  __/ / / / / /  __/ / / / /_  ")
    print("/_/   /_/   \____/_/ /\___/\___/\__/  /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/ /_/ /_/\___/_/ /_/\__/  ")
    print("                /___/                                          /____/                                 ")
    print(f" Copyright (C) 2021-2022 DAAV, LLC - {config.VERSION}")
    print(f" Licensed under the MIT license. See LICENSE for details\n")
    args = parser.parse_args()
    config.PATH_ROOT = __file__[:-12].replace('\\', '/') # set ROOT to repo folder (removes src/main.py from path)

    # Begin
    if args.UI == "CUI":
        LaunchCUI(args)
    elif args.UI == "GUI":
        LaunchGUI(args)
    else:
        LaunchMenu(args)
    exit(0)

def LaunchCUI(args):
    args.UI = interface.Type.CUI
    LaunchUI(args)

def LaunchGUI(args):
    args.UI = interface.Type.GUI
    LaunchUI(args)

def LaunchUI(args):
    ui = interface.UI(args)
    ui.Start()

def LaunchMenu(args):
    print("\tNote: UI is still developmental")
    print("\tPlease specify which interface you want to use:")
    print("\t    1) CUI       2) GUI")
    UsrInput = ""
    while True:
        UsrInput = input("\tSelect an option > ")
        try:
            UsrInput = int(UsrInput)
            if UsrInput == 1:
                LaunchCUI(args)
                break
            elif UsrInput == 2:
                LaunchGUI(args)
                break
            else:
                print(" ERR: Invalid option")
                continue
        except ValueError:
            UsrInput = UsrInput.lower()
            if "exit" in UsrInput:
                print("Goodbye!")
                exit(0)
            elif "reload" in UsrInput:
                print("Reloading...")
                sys.exit(-1)
            elif 'cui' in UsrInput:
                LaunchCUI(args)
                break
            elif 'gui' in UsrInput:
                LaunchGUI(args)
                break
            elif 'help' in UsrInput:
                print("\tCommands:")
                print("\t  help\n\t\tshow this menu")
                print("\t  1 | cui\n\t\tlaunch cui")
                print("\t  2 | gui\n\t\tlaunch gui")
                print("\t  reload\n\t\treload Project-Management")
            else:
                print(" ERR: Invalid option, type 'help' to view commands")
                continue
        except KeyboardInterrupt:
            print("Goodbye!")
            exit()

if __name__ == '__main__':
    main()
