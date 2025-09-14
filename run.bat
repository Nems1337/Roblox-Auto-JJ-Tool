@echo off

if not exist "main.py" (
	echo main.py missing
	pause
	exit /b 1
)

cscript //nologo run.vbs
timeout /t 1 /nobreak >nul