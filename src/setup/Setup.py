# Project-Management.setup.Setup - Launches checking python verison and installing packages
# Copyright (C) 2021  DAAV, LLC
# Language: Python 3.10

import os
import subprocess
import platform

from SetupPython import PythonConfiguration as PythonRequirements

# Make sure everything we need for the setup is installed
PythonRequirements.Validate()