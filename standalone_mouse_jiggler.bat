@echo off
REM Universal Windows Keep-Alive Tool
REM No Python or Java required - uses multiple fallback methods
REM Works with or without physical mouse/keyboard connected

setlocal enabledelayedexpansion

echo ========================================
echo Universal Windows Keep-Alive Tool v2.1
echo ========================================
echo This tool prevents your computer from
echo going to sleep using multiple methods.
echo.
echo Testing available methods...
echo ========================================

REM Test what methods are available
set "METHOD=NONE"
set "METHOD_NAME=Unknown"

REM Test 1: Try key press method
echo Testing keyboard input...
powershell -WindowStyle Hidden -Command "try { Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{SCROLLLOCK}'); exit 0 } catch { exit 1 }" 2>nul
if %errorlevel% equ 0 (
    set "METHOD=KEYPRESS"
    set "METHOD_NAME=Scroll Lock Key Press"
    echo ✓ Keyboard method available
    goto START_LOOP
)

REM Test 2: Try mouse movement method  
echo Testing mouse input...
powershell -WindowStyle Hidden -Command "try { Add-Type -AssemblyName System.Windows.Forms; $pos = [System.Windows.Forms.Cursor]::Position; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X + 1), $pos.Y); [System.Windows.Forms.Cursor]::Position = $pos; exit 0 } catch { exit 1 }" 2>nul
if %errorlevel% equ 0 (
    set "METHOD=MOUSE"
    set "METHOD_NAME=Mouse Movement"
    echo ✓ Mouse method available
    goto START_LOOP
)

REM Test 3: Try SetThreadExecutionState (most reliable for headless)
echo Testing system execution state...
powershell -WindowStyle Hidden -Command "try { Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Win32 { [DllImport(\"kernel32.dll\")] public static extern uint SetThreadExecutionState(uint esFlags); }'; [Win32]::SetThreadExecutionState(0x80000000 -bor 0x00000001); exit 0 } catch { exit 1 }" 2>nul
if %errorlevel% equ 0 (
    set "METHOD=EXECUTION_STATE"
    set "METHOD_NAME=System Execution State"
    echo ✓ System execution state method available
    goto START_LOOP
)

REM Fallback: Use simple file activity
set "METHOD=FILE_ACTIVITY"
set "METHOD_NAME=File System Activity"
echo ✓ Using file system activity method (universal fallback)

:START_LOOP
echo.
echo Using method: %METHOD_NAME%
echo Press Ctrl+C to stop at any time.
echo ========================================
echo.

:LOOP
    REM Get current time for logging
    echo [%TIME:~0,8%] Sending keep-alive signal (%METHOD_NAME%)...
    
    if "%METHOD%"=="KEYPRESS" (
        REM Method 1: Key press (invisible Scroll Lock toggle)
        powershell -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{SCROLLLOCK}'); Start-Sleep -Milliseconds 50; [System.Windows.Forms.SendKeys]::SendWait('{SCROLLLOCK}')"
    ) else if "%METHOD%"=="MOUSE" (
        REM Method 2: Mouse movement (1 pixel and back)
        powershell -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms; $pos = [System.Windows.Forms.Cursor]::Position; [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($pos.X + 1), $pos.Y); Start-Sleep -Milliseconds 50; [System.Windows.Forms.Cursor]::Position = $pos"
    ) else if "%METHOD%"=="EXECUTION_STATE" (
        REM Method 3: System execution state (prevents sleep directly)
        powershell -WindowStyle Hidden -Command "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class Win32 { [DllImport(\"kernel32.dll\")] public static extern uint SetThreadExecutionState(uint esFlags); }'; [Win32]::SetThreadExecutionState(0x80000000 -bor 0x00000001)"
    ) else (
        REM Method 4: File activity fallback (works on any system)
        echo %date% %time% > "%temp%\keepalive.tmp"
        del "%temp%\keepalive.tmp" 2>nul
    )
    
    REM Wait for 60 seconds (adjust as needed)
    timeout /t 60 /nobreak >nul
    
    REM Check if user pressed Ctrl+C (this won't catch it perfectly, but timeout will)
    if errorlevel 1 goto END
    
goto LOOP

:END
echo.
echo Keep-alive tool stopped.
echo Method used: %METHOD_NAME%
pause
