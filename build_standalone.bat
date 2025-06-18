@echo off
title Building Standalone Mouse Jiggler Executables

echo ============================================================
echo Building Standalone Windows Mouse Jiggler Executables
echo ============================================================
echo.
echo This will create .exe files that don't require Python!
echo.

REM Create build directory
if not exist "dist" mkdir dist
if not exist "build" mkdir build

echo Building Basic Mouse Jiggler (single file executable)...
"C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m PyInstaller --onefile --windowed --name "MouseJiggler" --distpath "dist" --workpath "build" mouse_jiggler.py

echo.
echo Building Advanced Mouse Jiggler (single file executable)...
"C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m PyInstaller --onefile --windowed --name "MouseJigglerAdvanced" --distpath "dist" --workpath "build" advanced_jiggler.py

echo.
echo Building Console Version (with visible output)...
"C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m PyInstaller --onefile --console --name "MouseJigglerConsole" --distpath "dist" --workpath "build" mouse_jiggler.py

echo.
echo ============================================================
echo Build Complete!
echo ============================================================
echo.
echo Standalone executables created in 'dist' folder:
echo - MouseJiggler.exe (basic version, no console)
echo - MouseJigglerAdvanced.exe (advanced version, no console)  
echo - MouseJigglerConsole.exe (basic version, with console)
echo.
echo These .exe files can run on any Windows machine without Python!
echo.
echo File sizes will be larger (~15-30 MB) because they include Python runtime.
echo.

REM Clean up build artifacts
echo Cleaning up build artifacts...
rmdir /s /q build 2>nul
del *.spec 2>nul

echo.
echo Press any key to exit...
pause >nul
