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

from common_types.base_types.version import Version as Version
from common_types.contributor import Contributor
from common_types.contribution import Contribution
import config.config as config

def main():
    print(f"Project Management {config.VERSION}")

    config.PATH_CURRENT_PROJECT = config.PATH_ROOT + "/Name"

    ctb = Contribution()
    ctb.SetName("Initial commit")
    ctb.SetDate(datetime.datetime.now().date())
    ctb.SetNumber("001")
    ctb.SetDescription("Initial commit")
    ctb.SetLead("Anonoei")
    ctb.SetVersionChange(Version("0.0.1"))
    ctb.UpdateProgress(10.0, datetime.datetime.now().date())

    ctb.Push("Anonoei", 1.5, datetime.datetime.now().date(), "Updated README")

    print(repr(ctb))
    print("-----------------------------------")

    ctb.Export(config.PATH_CURRENT_PROJECT + "/Contributions")

    ctb = Contribution()
    ctb.Import(config.PATH_CURRENT_PROJECT + "/Contributions", "001. Initial commit")
    print(repr(ctb))

if __name__ == '__main__':
    main()
