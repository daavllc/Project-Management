# Project-Management.setup.CheckPython - Check for requirements and install if not found
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import subprocess
import pkg_resources

def install(package):
    print(f"Installing {package} module...")
    subprocess.check_call(['python', '-m', 'pip', 'install', package])

def ValidatePackage(package):
    required = { package }
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        install(package)

def ValidatePackages():
    ValidatePackage('dearpygui')