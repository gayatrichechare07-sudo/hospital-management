@echo off
title MediCare Hospital Management System
echo.
echo  ========================================
echo    MediCare Hospital Management System
echo  ========================================
echo.
echo  Starting server... please wait.
echo.
cd /d "%~dp0"
python app.py
echo.
echo  Server stopped. Press any key to exit.
pause
