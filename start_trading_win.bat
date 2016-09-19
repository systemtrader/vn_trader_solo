@echo off
set script_start_path=%cd%
set script_start_drive=%script_start_path:~0,2%
set script_located_path=%~dp0
set script_located_drive=%script_located_path:~0,2%

rem switch to the script_drive
%script_located_drive%
cd %script_located_path%

rem start trading without command line
start pythonw.exe vtMain.py

rem start trading with command line
rem start python.exe vtMain.py
