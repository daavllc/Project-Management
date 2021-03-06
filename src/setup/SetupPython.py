# Project-Management.setup.SetupPython - Checks python version and prompts for package install
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import sys
import subprocess
import importlib.util as importlib_util

class PythonConfiguration:
    @classmethod
    def Validate(cls):
        if not cls.__ValidatePython():
            return # cannot validate further

        for packageName in ["dearpygui"]:
            if not cls.__ValidatePackage(packageName):
                return # cannot validate further

    @classmethod
    def __ValidatePython(cls, versionMajor = 3, versionMinor = 10):
        if sys.version is not None:
            if sys.version_info.major < versionMajor or (sys.version_info.major == versionMajor and sys.version_info.minor < versionMinor):
                print("Python version too low, expected version {0:d}.{1:d} or higher. You have version {3:d}.{4:d}.{5:d}".format( \
                    versionMajor, versionMinor, sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
                if not 'y' in input("Do you want to proceed anyway? (y/N) ").lower():
                    return False
            return True

    @classmethod
    def __ValidatePackage(cls, packageName):
        if importlib_util.find_spec(packageName) is None:
            return cls.__InstallPackage(packageName)
        return True

    @classmethod
    def __InstallPackage(cls, packageName):
        reply = input(f"Would you like to install Python package '{packageName:s}'? (Y/n) ").lower()
        if 'n' in reply or 'N' in reply:
            return False

        print(f"Installing {packageName} module...")
        subprocess.check_call(['python', '-m', 'pip', 'install', packageName])

        return cls.__ValidatePackage(packageName)

if __name__ == "__main__":
    PythonConfiguration.Validate()