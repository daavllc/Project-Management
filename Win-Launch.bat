@echo off

cd src
:loop
python3 main.py
if %errorlevel% == -1 GOTO :loop
PAUSE
exit