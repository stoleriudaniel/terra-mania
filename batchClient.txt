@echo off

REM Check if the server process is already running
tasklist /FI "IMAGENAME eq client.exe" /FI "WINDOWTITLE eq client.py" 2>NUL | find /I /N "client.exe">NUL
if "%ERRORLEVEL%"=="0" (
    REM Server process is running, stop it
    echo Stopping server...
    taskkill /F /IM client.exe /FI "WINDOWTITLE eq client.py"
)

REM Start the server by calling the create() method with an argument
echo Starting server...
start "" python -c "import sys; from client import Client; client = Client(sys.argv[1]); client.play()" %1