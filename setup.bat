@echo off
title Setup

echo Checking python...
python --version >nul 2>&1
if errorlevel 1 (
	echo Python not found. Install from python.org
	pause
	exit /b 1
)
echo Python OK

echo Installing packages...
pip install -r requirements.txt
if errorlevel 1 (
	echo Failed to install packages
	echo Try running as admin
	pause
	exit /b 1
)

echo Testing imports...
pythonw -c "import customtkinter, pyautogui, pyperclip, pynput" 2>nul
if errorlevel 1 (
	echo Import test failed
	pause
	exit /b 1
)

echo Setup done. Starting app...
cscript //nologo run.vbs
timeout /t 1 /nobreak >nul