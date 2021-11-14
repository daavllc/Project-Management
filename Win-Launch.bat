:: Project-Management.Win-Launch - Windows script to launch launch.ps1 by double-clicking
:: Copyright (C) 2021  DAAV, LLC
:: Language: Python 3.10
@echo off
cd src/launch
powershell -NoProfile -ExecutionPolicy RemoteSigned ".\launch.ps1"
PAUSE