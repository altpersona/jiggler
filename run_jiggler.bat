@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Mouse Jiggler...
python mouse_jiggler.py

pause
