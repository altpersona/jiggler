@echo off
echo Building standalone mouse jiggler executable...
echo This will create a .exe file that doesn't require Python!
echo.

"C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m PyInstaller --onefile --windowed --name "MouseJiggler" standalone_jiggler.py

echo.
echo Build complete!
echo.
echo Executable created: dist\MouseJiggler.exe
echo.
echo This .exe file can run on any Windows machine without Python!
echo Copy MouseJiggler.exe to any computer and double-click to run.
echo.
pause
