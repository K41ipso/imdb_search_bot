@echo off

call %~dp0omdb_dot\venv\Scripts\activate

cd %~dp0omdb_dot

set TOKEN=6240611798:AAEOMB4WUANSNCKbsVl8yjh4bnOorHYnSKk

python bot_telegram.py

pause