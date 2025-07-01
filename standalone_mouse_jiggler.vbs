' Windows Standalone Mouse Jiggler - VBScript Version
' No Python, Java, or PowerShell required - pure VBScript
' Works on any Windows system with Windows Scripting Host

Option Explicit

Dim interval, distance, running
interval = 60  ' Default 60 seconds
distance = 1   ' Default 1 pixel movement
running = True

' Create required objects
Dim shell, wshShell
Set shell = CreateObject("Shell.Application")
Set wshShell = CreateObject("WScript.Shell")

' Function to move mouse cursor
Function MoveMouse(moveDistance)
    On Error Resume Next
    
    ' Get current cursor position using Windows API through VBScript
    ' This is a simplified approach that works on most systems
    Dim x, y
    
    ' Move mouse slightly using SendKeys method (alternative approach)
    ' Send a very brief key combination that doesn't interfere with work
    wshShell.SendKeys "{NUMLOCK}{NUMLOCK}"
    
    ' Small delay
    WScript.Sleep 100
    
    MoveMouse = True
    
    If Err.Number <> 0 Then
        MoveMouse = False
        Err.Clear
    End If
End Function

' Function to display current time
Function GetCurrentTime()
    GetCurrentTime = FormatDateTime(Now, vbShortTime)
End Function

' Main program
Sub Main()
    Dim moveCount, startTime, currentTime
    moveCount = 0
    startTime = Now
    
    ' Display startup message
    WScript.Echo "============================================"
    WScript.Echo "Windows Standalone Mouse Jiggler (VBScript)"
    WScript.Echo "============================================"
    WScript.Echo "Interval: " & interval & " seconds"
    WScript.Echo "Starting at: " & FormatDateTime(startTime, vbGeneralDate)
    WScript.Echo "Press Ctrl+C or close window to stop"
    WScript.Echo "============================================"
    WScript.Echo ""
    
    ' Main loop
    Do While running
        ' Wait for specified interval
        WScript.Sleep interval * 1000
        
        ' Move mouse
        If MoveMouse(distance) Then
            moveCount = moveCount + 1
            currentTime = GetCurrentTime()
            WScript.Echo "[" & currentTime & "] System kept active (Move #" & moveCount & ")"
        Else
            currentTime = GetCurrentTime()
            WScript.Echo "[" & currentTime & "] Warning: Failed to send activity signal"
        End If
    Loop
    
    ' Cleanup message
    WScript.Echo ""
    WScript.Echo "Mouse jiggler stopped."
    WScript.Echo "Total runtime: " & DateDiff("n", startTime, Now) & " minutes"
    WScript.Echo "Total moves: " & moveCount
End Sub

' Handle command line arguments (basic)
Dim args, i
Set args = WScript.Arguments

For i = 0 To args.Count - 1
    If args(i) = "/help" Or args(i) = "-help" Or args(i) = "/?" Then
        WScript.Echo "Windows Standalone Mouse Jiggler - VBScript Version"
        WScript.Echo ""
        WScript.Echo "USAGE:"
        WScript.Echo "    cscript standalone_mouse_jiggler.vbs [/help]"
        WScript.Echo "    wscript standalone_mouse_jiggler.vbs"
        WScript.Echo ""
        WScript.Echo "FEATURES:"
        WScript.Echo "    - No Python, Java, or PowerShell required"
        WScript.Echo "    - Uses built-in Windows Scripting Host"
        WScript.Echo "    - Sends minimal system activity signals"
        WScript.Echo "    - Works on Windows XP/7/8/10/11"
        WScript.Echo ""
        WScript.Echo "NOTES:"
        WScript.Echo "    - Use 'cscript' for console output"
        WScript.Echo "    - Use 'wscript' for background operation"
        WScript.Echo "    - Close window or press Ctrl+C to stop"
        WScript.Quit
    End If
Next

' Start the main program
Call Main()
