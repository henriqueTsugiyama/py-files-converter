@echo off
REM Windows launcher script for File Converter GUI
REM Double-click this file to run the application

echo Starting File Converter GUI...
python file_converter_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error: Could not start the application.
    echo Please make sure Python is installed and requirements are installed.
    echo Run: pip install -r requirements.txt
    pause
)
