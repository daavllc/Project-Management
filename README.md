# Project Management v0.0.1
 Easy to use graphical application for managing projects

## Purpose:
In order to effectively manage projects within an organization, details about each project, hours and time invested, it’s contributions, and contributors must be kept. This will allow DAAV, LLC to function more efficiently, by ensuring details about all of our projects are well maintained. We hope to streamline and automate this process as much as possible, to spend more time developing, instead of describing what we’ve developed.

## Details:
 - Project lead: [Anonoei](https://github.com/Anonoei)
 - Language: Python 3.10
 - License: GPLv3

----

## Current status/roadmap:
 - [ ] External integrations?
 - [ ] Search for projects
 - [ ] Project Explorer
 - [ ] One-click start/end/pause timer for contributions
 - [ ] Project editor/viewer
 - [ ] Contribution editor/viewer
 - [ ] Contributor editor/viewer
 - [ ] DearPyGui implementation
 - [ ] Project import/export
 - [ ] Initial working implementation
 - [ ] Command line access
 - [ ] API for accessing each class and it’s data
 - [ ] Header class
 - [ ] Contribution class
 - [X] Contributor class

----

## Projects
 A project contains various information, and each item can be considered nested in the item above it:
 - Header
 - Contributions
 - Contributors
### Header
 - Name
 - Description/goal
 - Creation Date
 - Project lead/originator
 - Version - Release.Major.Minor Patch #.#.# #su
 - Time invested (total) - automatic from contribution data
 - Money Invested (total) - automatic from contribution data
 - Contributions:
### Contributions
 - Name
 - Description/goal
 - Contribution lead/originator
 - Version increase
 - Current progress %
 - Time invested (total)
 - Money invested (total)
 - Contributors:
### Contributors
 - Name
 - What was added
   - Date worked on
     - Time worked on
      
## Installation
Note: currently there are no releases, so it must be downloaded from source. Officially, only windows is supported, but there is no windows-only code.

## Download from source
 1. `git clone https://github.com/daavofficial/Project-Management.git`
   - If wanted, create python environment
 2. Install dependancies
   - `pip install dearpygui`
 3. Open 'Project-Management' folder.
 4. Run Win-Launch.bat
 5. Begin using