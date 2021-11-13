# Project Management
 Easy to use graphical application for managing projects

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
 - [ ] Project editor/viewer
 - [ ] Contribution editor/viewer
 - [ ] Contributor editor/viewer
 - [ ] DearPyGui implementation
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
     - header.inf
     - Contributions
       - Contribution Name
         - contributors.csv
         - info.inf
         - progress.csv
     - Contributors
       - Contributor Name
         - data.csv
         - info.inf

This allows contributors and contributions to co-exist, and 'see' eachother
### Projects
 A project contains various information:
 - Header
 - Contributions
 - Contributors
### Project Header
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
### Project Contributions
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
### Project Contributors
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
    - This launches `src/launch/launch.ps1` which performs various functions
      - Check environment variables for python/python3 to choose the best one
      - Launch `src/setup/Setup.py` to check python version and prompy for required packages
      - Allows reloading/handling
 4. `src/main.py` will ask for what UI to use
 5. Select `1` for CUI, as the GUI is not implemented yet
 6. (Optional) Enjoy