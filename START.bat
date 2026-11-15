@echo off
title MediCare HMS - Setup & Run
color 0A
echo.
echo  =========================================
echo    MediCare Hospital Management System
echo  =========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Python not found!
    echo  [!] Opening Python download page...
    start https://www.python.org/downloads
    echo  [!] Install Python then run this file again.
    pause
    exit
)

echo  [+] Python found!

:: Install dependencies
echo  [+] Installing required packages...
pip install -r requirements.txt -q

echo  [+] Starting MediCare HMS...
echo.
echo  =========================================
echo   App is running!
echo   Open your browser and go to:
echo   >>> http://127.0.0.1:5000 <<<
echo  =========================================
echo.

:: Open browser automatically
start http://127.0.0.1:5000

:: Run the app
python app.py

pause
