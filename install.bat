@echo off
REM Batch script to install Python and Node.js dependencies only

REM Install Python dependencies
pip install -r requirements.txt

REM Install Node.js dependencies (if package.json exists)
IF EXIST package.json (
    echo Installing Node.js dependencies...
    npm install
)

echo.
echo All dependencies installed. Press any key to exit.
pause >nul
