@echo off
REM Windows Standalone Mouse Jiggler - Simple Version
REM No Python or Java required - uses built-in Windows tools

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
    REM Get current time (simpler method)
    echo [%TIME:~0,8%] Moving mouse to keep system active...
    
    REM Call PowerShell to move mouse
    powershell -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms; $pos = [System.Windows.Forms.Cursor]::Position; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X + 1), $pos.Y); Start-Sleep -Milliseconds 50; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X), $pos.Y)"
    
    if %errorlevel% neq 0 (
        echo Error: PowerShell command failed
        pause
        exit /b 1
    )
    
    echo Mouse movement completed successfully
    
    REM Wait for 60 seconds
    echo Waiting 60 seconds... (Press Ctrl+C to stop)
    timeout /t 60 /nobreak >nul
    
    REM Check if user pressed Ctrl+C
    if errorlevel 1 goto END
    
goto LOOP

:END
echo.
echo Mouse jiggler stopped.
pause
