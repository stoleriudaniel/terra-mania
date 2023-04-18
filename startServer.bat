@echo off

REM Check if the server process is already running
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq server.py" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    REM Server process is running, stop it
    echo Stopping server...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq server.py"
)

REM Start the server by calling the create() method with an argument
echo Starting server...
start "" python -c "import sys; from server import Server; s = Server(); s.create(sys.argv[1])" %1