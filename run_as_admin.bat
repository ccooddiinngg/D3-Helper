@echo off
:: Batch file to run main.py as administrator
:: Right-click this file and select "Run as administrator"

cd /d "%~dp0"
c:/Downloads/222/.venv/Scripts/python.exe c:/Downloads/222/main.py
pause

