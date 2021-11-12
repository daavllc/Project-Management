@echo off

:SETUP
cd src/setup
python3 Setup.py
cd ..

:MAINLOOP
python3 main.py
if %errorlevel% == -1 GOTO :MAINLOOP
PAUSE
exit