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
 - [ ] One-click start/end/pause timer for contributions
 - [ ] Polished Graphical User Interface (dearpygui)
 - [X] GUI Project editor
 - [X] GUI Contribution editor
 - [X] GUI Contributor editor
 - [X] GUI Project viewer
 - [X] GUI Contribution viewer
 - [X] GUI Contributor viewer
 - [X] Get data by UUID instead of name
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
   - Project UUID
     - *header.inf*
     - Contributions
       - Contribution UUID
         - *contributors.csv*
         - *info.inf*
         - *progress.csv*
     - Contributors
       - Contributor UUID
         - *data.csv*
         - *info.inf*

This allows contributors and contributions to co-exist, and 'see' eachother, and using UUIDs enables changing names without creating issues
### Projects
 A project contains various information:
 - [Header](https://github.com/daavofficial/Project-Management/blob/main/src/common_types/project.py)
 - [Contributions](https://github.com/daavofficial/Project-Management/blob/main/src/common_types/contribution.py)
 - [Contributors](https://github.com/daavofficial/Project-Management/blob/main/src/common_types/contributor.py)
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
 - Description/goal of contribution
 - Contribution lead/originator
 - Version increase - #.#.#
 - Contributors - list of contributors
 - Progress - list of progress increase and date
 - Generated:
   - Creation Date (modifiable)
   - Contribution UUID
   - Current progress (%)
   - Contribution Number(1, 2, ...) - from project contributions (modifiable)
   - Time invested (total) - from contributor data
   - Money invested (total) - from contributor data
### [Project Contributors](https://github.com/daavofficial/Project-Management/blob/main/src/common_types/contributor.py)
 - Name
 - URL
 - Additions
   - Hours
   - Date
   - Description of addition
   - Contribution UUID
 - Generated
   - Date began working on project (modifiable)
   - Contributor UUID
      
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

## License
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
