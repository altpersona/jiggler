# Windows Standalone Mouse Jiggler - PowerShell Version
# No Python or Java required - pure PowerShell script
# More advanced than batch with better error handling and configurability

param(
    [int]$Interval = 60, # Seconds between movements
    [int]$Distance = 1, # Pixels to move
    [switch]$Silent = $false    # Run without console output
)

# Load required assemblies for mouse control
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Function to move mouse
function Move-Mouse {
    param([int]$distance = 1)
    
    try {
        # Get current mouse position
        $currentPos = [System.Windows.Forms.Cursor]::Position
        
        # Move mouse slightly right and down
        $newX = $currentPos.X + $distance
        $newY = $currentPos.Y + $distance
        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($newX, $newY)
        
        # Brief pause
        Start-Sleep -Milliseconds 50
        
        # Move back to original position
        [System.Windows.Forms.Cursor]::Position = $currentPos
        
        return $true
    }
    catch {
        Write-Warning "Failed to move mouse: $($_.Exception.Message)"
        return $false
    }
}

# Function to simulate key press (alternative method)
function Send-KeyPress {
    try {
        # Send a harmless key combination (Shift key press/release)
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("{SHIFT}")
        return $true
    }
    catch {
        return $false
    }
}

# Main execution
function Start-MouseJiggler {
    if (-not $Silent) {
        Write-Host "============================================" -ForegroundColor Green
        Write-Host "Windows Standalone Mouse Jiggler" -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Green
        Write-Host "Interval: $Interval seconds" -ForegroundColor Yellow
        Write-Host "Distance: $Distance pixels" -ForegroundColor Yellow
        Write-Host "Press Ctrl+C to stop gracefully" -ForegroundColor Yellow
        Write-Host "============================================" -ForegroundColor Green
        Write-Host ""
    }
    
    $startTime = Get-Date
    $moveCount = 0
    
    try {
        while ($true) {
            # Wait for the specified interval
            Start-Sleep -Seconds $Interval
            
            # Attempt mouse movement
            $success = Move-Mouse -distance $Distance
            
            if ($success) {
                $moveCount++
                if (-not $Silent) {
                    $timestamp = Get-Date -Format "HH:mm:ss"
                    Write-Host "[$timestamp] Mouse jiggled (Move #$moveCount) - System kept active" -ForegroundColor Cyan
                }
            }
            else {
                # Fallback to key press if mouse movement fails
                $keySuccess = Send-KeyPress
                if ($keySuccess -and -not $Silent) {
                    $timestamp = Get-Date -Format "HH:mm:ss"
                    Write-Host "[$timestamp] Key press sent (fallback) - System kept active" -ForegroundColor Yellow
                }
            }
        }
    }
    catch [System.Management.Automation.PipelineStoppedException] {
        # Handle Ctrl+C gracefully
        if (-not $Silent) {
            Write-Host ""
            Write-Host "Mouse jiggler stopped gracefully." -ForegroundColor Green
            $runtime = (Get-Date) - $startTime
            Write-Host "Runtime: $($runtime.ToString('hh\:mm\:ss'))" -ForegroundColor Green
            Write-Host "Total moves: $moveCount" -ForegroundColor Green
        }
    }
    catch {
        Write-Error "Unexpected error: $($_.Exception.Message)"
    }
}

# Display help if requested
if ($args -contains "-help" -or $args -contains "--help" -or $args -contains "/?" -or $args -contains "-h") {
    Write-Host @"
Windows Standalone Mouse Jiggler - PowerShell Version

USAGE:
    .\standalone_mouse_jiggler.ps1 [OPTIONS]

OPTIONS:
    -Interval <seconds>    Time between mouse movements (default: 60)
    -Distance <pixels>     Distance to move mouse (default: 1)
    -Silent               Run without console output
    -Help                 Show this help message

EXAMPLES:
    .\standalone_mouse_jiggler.ps1
    .\standalone_mouse_jiggler.ps1 -Interval 30 -Distance 2
    .\standalone_mouse_jiggler.ps1 -Silent

NOTES:
    - No Python or Java required
    - Uses built-in Windows PowerShell
    - Press Ctrl+C to stop gracefully
    - Minimal system impact
    - Works on Windows 7/8/10/11
"@
    exit 0
}

# Validate parameters
if ($Interval -lt 5) {
    Write-Warning "Interval too low. Setting to minimum of 5 seconds."
    $Interval = 5
}

if ($Distance -lt 1 -or $Distance -gt 10) {
    Write-Warning "Distance should be 1-10 pixels. Setting to 1."
    $Distance = 1
}

# Start the jiggler
Start-MouseJiggler
