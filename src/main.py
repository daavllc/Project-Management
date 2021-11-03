#
## Cost/Time Management
# Author: DAAV, LLC (https://github.com/daavofficial)
# Language: Python 3.10
# License: GPLv3
# Purpose: Create easy-to-use graphical program for managing cost/time of projects
# Contributors: 
"""
    Anonoei: https://github.com/Anonoei
"""

from project_management.management import Management

def main():
    app = Management()

    app.uiSetup()
    app.uiRuntime()
    app.uiShutdown()

if __name__ == "__main__":
    main()