######################################################################################################
#  ____   _____   ________  ____  ______    _        ___   _     _ ___  _____   ____     ____ _____  #
# |  __ \|  __ \ /|_    __|/ __ \|__  __|  | \      / _ \ | \   | | _ \/  __ \ |  __|   /  __|_  __| #
# | |  \ \ |  \ \ / \ \|  | |  \ \  | |    |  \    / / \ \|  \  | |/ \ \ /  \_\| |\    /  | \  | |   #
# | |__/ / |__/ /|   | |  | |_  |_| | |    | \ \  / /___\ \ \ \ | |   | |  ____| |_\  / / |_ \ | |   #
# |  ___/|  _  / |   | |  |  _|  _  | |    | |\ \/ /______ \ \ \| |___| | |___ |  _|\/ /|  _| \| |   #
# | |    | | \ \_|   | |  | |   | | | |    | | \/ / | |   \ \ \ \ |___  |    | | | \__/ | |  \ \ |   #
# | |    | |  \ \ \_/ /   | |__/ /  | |    | | / /  | |   |\ \ \  |   | |___/ /| |__    | |__ \  |   #
# |_|    |_|   \_\___/    |\____/   |_|    |_|/_/   |_|   |_\ \ \_|   |_|____/ |____|   |____| \_|   #
#                                                                                                    #
######################################################################################################
# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python 3.10
# License: GPLv3
## Project-Management
# Easy to use graphical application for managing projects
##########################################################
# Project Lead: Anonoei (https://github.com/Anonoei)

import datetime

from common_types.contributor import Contributor
import config.config as config

def main():
    print(f"Project Management {config.VERSION}")

def does_not_work_now():
    c = Contributor()
    c.SetName('Anonoei')
    c.SetURL('https://github.com/Anonoei')
    c.Push(1.5, datetime.date(2021, 11, 8), "Initial commit")
    c.Push(1.5, datetime.date(2021, 11, 8), "Initial commit 2")
    c.Push(1.5, datetime.date(2021, 11, 8), "Initial commit 3")
    c.Push(1.5, datetime.date(2021, 11, 8), "Initial commit 4")
    c.Export("data")
    print(str(c))

    c = Contributor()
    c.Import("data", "Anonoei")
    print(str(c))

if __name__ == '__main__':
    main()
