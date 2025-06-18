@echo off
echo Building Mouse Jiggler v1.1 - System Tray Edition
echo This creates a standalone executable that runs in the system tray
echo.

REM Build the system tray version
"C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m PyInstaller --onefile --windowed --name "MouseJiggler_v1.1_SystemTray" --distpath "dist" tray_jiggler.py

echo.
echo Build complete!
echo.
echo Executable created: dist\MouseJiggler_v1.1_SystemTray.exe
echo.
echo Features:
echo - Runs in system tray (no console window)
echo - Right-click menu for controls
echo - Visual status indicators (red=stopped, green=running)
echo - Configurable intervals and movement distance
echo - Status notifications
echo.
echo Double-click the .exe file to start!
echo.
pause
