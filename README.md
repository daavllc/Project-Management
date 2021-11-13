# Project Management
 Easy to use GUI/CUI for managing projects

## Purpose:
In order to effectively manage projects within an organization, details about each project, hours and time invested, it’s contributions, and contributors must be kept. This will allow DAAV, LLC to function more efficiently, by ensuring details about all of our projects are well maintained. We hope to streamline and automate this process as much as possible, to spend more time developing, instead of describing what we’ve developed.

## Details:
 - Project lead: [Anonoei](https://github.com/Anonoei)
 - Language: Python 3.10
 - License: GPLv3
 - Dependancies: dearpygui

----

## Current status/roadmap:
 - [ ] External integrations?
 - [ ] Search for projects
 - [ ] Project Explorer
 - [ ] One-click start/end/pause timer for contributions
 - [ ] Get data by UUID instead of name
 - [ ] Graphical User Interface (dearpygui)
 - [ ] GUI Project editor
 - [ ] GUI Contribution editor
 - [ ] GUI Contributor editor
 - [X] GUI Project viewer
 - [X] GUI Contribution viewer
 - [X] GUI Contributor viewer
 - [X] Console User Inerface
 - [X] Project import/export
 - [X] Initial working implementation
 - [X] API for accessing each class and it’s data
 - [X] Project Header class
 - [X] Contribution class
 - [X] Contributor class

----
## Structure
The files are structured as follows:
 - Projects
   - Project Name
     - *header.inf*
     - Contributions
       - Contribution Name
         - *contributors.csv*
         - *info.inf*
         - *progress.csv*
     - Contributors
       - Contributor Name
         - *data.csv*
         - *info.inf*

This allows contributors and contributions to co-exist, and 'see' eachother
### Projects
 A project contains various information:
 - Header
 - Contributions
 - Contributors
### [Project Header](https://github.com/daavofficial/Project-Management/blob/main/src/common_types/project.py)
 - Name
 - Description/goal of project
 - Creation Date
 - Project lead/originator
 - Version - Release.Major.Minor - #.#.#
 - Generated:
   - Time invested (total) - automatic from contribution data
   - Money Invested (total) - automatic from contribution data
   - Number of contributions
   - Number of contributors
### [Project Contributions](https://github.com/daavofficial/Project-Management/blob/main/src/common_types/contribution.py)
 - Name
 - Creation Date
 - Contribution Number - 01, 02, 03...
 - Description/goal of contribution
 - Contribution lead/originator
 - Version increase - #.#.#
 - Current progress (%)
 - Contribution UUID
 - Contributors - list of contributors
 - Generated:
   - Time invested (total) - automatic from contributor data
   - Money invested (total) - automatic from contributor data
### [Project Contributors](https://github.com/daavofficial/Project-Management/blob/main/src/common_types/contributor.py)
 - Name
 - Date began project work
 - URL
 - Contributor UUID
 - Additions
   - Hours
   - Date
   - Description of addition
   - Contribution UUID
      
## Installation
Note: currently there are no releases, so it must be downloaded from source. Officially, only windows is supported, although there is no windows-only code.

## Download from source
 1. `git clone https://github.com/daavofficial/Project-Management.git`
 3. Open 'Project-Management' folder.
 4. Run [Win-Launch.bat](https://github.com/daavofficial/Project-Management/blob/main/Win-Launch.bat)
    - This launches [launch.ps1](https://github.com/daavofficial/Project-Management/blob/main/src/launch/launch.ps1) which performs various functions
      - Check environment variables for python/python3 to choose the best one
      - Launch [Setup.py](https://github.com/daavofficial/Project-Management/blob/main/src/setup/Setup.py) to [check python version](https://github.com/daavofficial/Project-Management/blob/main/src/setup/SetupPython.py) and prompt for required packages
      - Launch [main.py](https://github.com/daavofficial/Project-Management/blob/main/src/main.py)
        - Prompt for what UI to use 
      - Allows reloading/error handling
 5. Type `1` or `2` to select [CUI](https://github.com/daavofficial/Project-Management/blob/main/src/cui/cui.py), or the [GUI](https://github.com/daavofficial/Project-Management/blob/main/src/gui/gui.py) respectively
 6. (Optional) Enjoy
