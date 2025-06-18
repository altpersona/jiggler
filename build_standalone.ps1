# Build Standalone Executables
# This script creates .exe files that don't require Python installation

# Build basic version
Write-Host "Building basic standalone mouse jiggler..."
& "C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m PyInstaller --onefile --noconsole --name "MouseJiggler" standalone_jiggler.py

# Build advanced version (if needed)
# Write-Host "Building advanced version..."
# & "C:/Users/micro/AppData/Local/Programs/Python/Python310/python.exe" -m PyInstaller --onefile --noconsole --name "MouseJiggler_Advanced" advanced_jiggler.py

Write-Host ""
Write-Host "Build complete! Executable files:"
Write-Host "- dist/MouseJiggler.exe (Standalone - No Python Required)"
Write-Host ""
Write-Host "You can copy MouseJiggler.exe to any Windows machine and it will work"
Write-Host "without requiring Python installation!"
