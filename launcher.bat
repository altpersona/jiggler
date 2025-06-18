@echo off
title Windows Mouse Jiggler - Security Friendly

echo ============================================================
echo Windows Mouse Jiggler - Security Friendly Version
echo ============================================================
echo.
echo Choose version to run:
echo 1. Basic Version (simple and straightforward)
echo 2. Advanced Version (enterprise features)
echo 3. Install/Update dependencies
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Starting Basic Mouse Jiggler...
    echo.
    "C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" mouse_jiggler.py
) else if "%choice%"=="2" (
    echo Starting Advanced Mouse Jiggler...
    echo.
    "C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" advanced_jiggler.py
) else if "%choice%"=="3" (
    echo Installing/Updating dependencies...
    "C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m pip install --upgrade pip
    "C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m pip install -r requirements.txt
    echo.
    echo Dependencies updated successfully!
    pause
) else if "%choice%"=="4" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please run the script again.
    pause
)

echo.
echo Press any key to exit...
pause >nul
