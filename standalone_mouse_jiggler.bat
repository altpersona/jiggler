@echo off
REM Windows Standalone Mouse Jiggler
REM No Python or Java required - uses built-in Windows tools
REM This script moves the mouse cursor slightly every 60 seconds

setlocal enabledelayedexpansion

echo ========================================
echo Windows Standalone Mouse Jiggler
echo ========================================
echo This tool prevents your computer from
echo going to sleep by moving the mouse
echo cursor slightly every 60 seconds.
echo.
echo Press Ctrl+C to stop at any time.
echo ========================================
echo.

:LOOP
    REM Get current time for logging
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "timestamp=!dt:~8,2!:!dt:~10,2!:!dt:~12,2!"
    
    echo [!timestamp!] Moving mouse to keep system active...
    
    REM Call PowerShell to move mouse (more reliable than VBS)
    powershell -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms; $pos = [System.Windows.Forms.Cursor]::Position; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X + 1), $pos.Y); Start-Sleep -Milliseconds 50; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X), $pos.Y)"
    
    REM Wait for 60 seconds (adjust as needed)
    timeout /t 60 /nobreak >nul
    
    REM Check if user pressed Ctrl+C (this won't catch it perfectly, but timeout will)
    if errorlevel 1 goto END
    
goto LOOP

:END
echo.
echo Mouse jiggler stopped.
pause
