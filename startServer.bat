@echo off

tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq server.py" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Stopping server...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq server.py"
)

echo Starting server...
start "" python -c "import sys; from server import Server; s = Server(); s.create(sys.argv[1], sys.argv[2], sys.argv[3])" %1 %2 %3