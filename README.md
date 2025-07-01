# Windows Mouse Jiggler - Security Friendly

A lightweight, security-conscious mouse jiggler for Windows that prevents system sleep and screensaver activation without triggering security warnings.

## 🚀 Version 2.0 - Standalone Edition

**NEW:** No Python or Java required! Three standalone implementations using only built-in Windows components:

- **Batch Script** (`.bat`) - Just double-click to run
- **PowerShell Script** (`.ps1`) - Advanced configuration options  
- **VBScript** (`.vbs`) - Minimal resource usage

**Perfect for corporate environments** - no installations needed!

## Features

### 🎯 Standalone Versions (v2.0) - **RECOMMENDED**

- **Zero Dependencies**: No Python, Java, or any runtime required
- **Instant Use**: Just download and double-click
- **Corporate Friendly**: Uses only built-in Windows components
- **Three Options**: Batch, PowerShell, and VBScript versions
- **Full Documentation**: Complete usage guides included

### 🐍 Python Versions (Legacy)

- **System Tray Integration**: Runs in background with visual status indicators
- **Right-Click Menu**: Easy access to start/stop and configuration
- **Configurable**: Adjustable intervals and movement distance
- **Safe**: Uses PyAutoGUI library (well-established and trusted)
- **Standalone Executable**: No Python installation required for compiled versions

### Version Comparison

| Version | Dependencies | Best For | Ease of Use |
|---------|-------------|----------|-------------|
| **v2.0 Standalone** | None | Corporate/Restricted environments | ⭐⭐⭐⭐⭐ |
| v1.1 System Tray | Python | Advanced users with Python | ⭐⭐⭐ |
| v1.0 Console | Python | Command-line users | ⭐⭐ |

## Why This Approach is Security Friendly

1. **Transparent Operation**: Uses standard PyAutoGUI library, not low-level injection
2. **Minimal Movements**: Tiny 1-2 pixel movements that barely affect cursor position
3. **User Control**: Clear start/stop commands and visual feedback
4. **No Hidden Behavior**: All actions are logged to console
5. **Standard Library**: Uses well-known, legitimate automation library

## Quick Start

### 🚀 Standalone Versions (Recommended)

**No installation required!** Choose your preferred version:

1. **Batch Script** (Easiest)
   ```batch
   # Just double-click:
   standalone_mouse_jiggler.bat
   ```

2. **PowerShell Script** (Most Features)
   ```powershell
   # Right-click → "Run with PowerShell" or:
   .\standalone_mouse_jiggler.ps1
   
   # With custom settings:
   .\standalone_mouse_jiggler.ps1 -Interval 30 -Distance 2
   ```

3. **VBScript** (Lightest)
   ```batch
   # Double-click or:
   cscript standalone_mouse_jiggler.vbs
   ```

### 🐍 Python Versions (Legacy)

1. Make sure Python 3.6+ is installed
2. Run the batch file or install manually:

### Option 1: Use the batch file (Python)

```batch
run_jiggler.bat
```

### Option 2: Manual installation (Python)

```bash
pip install -r requirements.txt
python mouse_jiggler.py
```

## Standalone Usage

### Batch Script (`standalone_mouse_jiggler.bat`)

1. Double-click the file
2. Mouse will jiggle every 60 seconds
3. Press Ctrl+C to stop

### PowerShell Script (`standalone_mouse_jiggler.ps1`)

```powershell
# Basic usage
.\standalone_mouse_jiggler.ps1

# Custom interval (30 seconds)
.\standalone_mouse_jiggler.ps1 -Interval 30

# Silent mode
.\standalone_mouse_jiggler.ps1 -Silent

# Show help
.\standalone_mouse_jiggler.ps1 -Help
```

### VBScript (`standalone_mouse_jiggler.vbs`)

```batch
# Console output
cscript standalone_mouse_jiggler.vbs

# Background mode
wscript standalone_mouse_jiggler.vbs
```

## Python Usage (Legacy)

### Quick Start

1. Run `python mouse_jiggler.py`
2. Type `start` to begin
3. Type `stop` to pause
4. Type `quit` to exit

### Commands

- `start` - Start the mouse jiggler
- `stop` - Stop the mouse jiggler
- `interval X` - Set interval to X seconds (minimum 5)
- `distance X` - Set movement distance to X pixels (1-10)
- `status` - Show current status
- `help` - Show help information
- `quit` or `exit` - Exit the program

### Example Session

```
> interval 30        # Jiggle every 30 seconds
> distance 1         # Move 1 pixel
> start              # Begin jiggling
[14:30:15] Mouse jiggled - keeping system active
[14:30:45] Mouse jiggled - keeping system active
> stop               # Stop jiggling
> quit               # Exit
```

## Configuration Options

### Interval Settings

- **Default**: 60 seconds
- **Minimum**: 5 seconds
- **Recommended**: 30-120 seconds
- **Purpose**: How often to perform the jiggle

### Movement Distance

- **Default**: 1 pixel
- **Range**: 1-10 pixels
- **Recommended**: 1-2 pixels
- **Purpose**: How far to move the mouse

## Security Considerations

### Why This Won't Trigger Windows Security

1. **No DLL Injection**: Doesn't inject code into other processes
2. **No Low-Level Hooks**: Doesn't install global mouse hooks
3. **Standard API Usage**: Uses standard Windows mouse APIs through Python
4. **Transparent Process**: Runs as a normal user application
5. **No System Modification**: Doesn't modify system files or registry

### Antivirus Considerations

- Uses PyAutoGUI, a legitimate automation library
- No obfuscated code or suspicious patterns
- Open source and auditable
- Minimal system interaction
- Clear logging of all actions

### Corporate Environment Friendly

- No admin privileges required
- Doesn't bypass security policies
- Transparent operation with logging
- Can be easily monitored or disabled
- Uses standard automation approaches

## Technical Details

### How It Works

1. Gets current mouse position
2. Moves mouse 1-2 pixels right
3. Immediately moves back to original position
4. Waits for specified interval
5. Repeats

### Why This Prevents Sleep

- Windows monitors for user input activity
- Mouse movement counts as user activity
- Prevents system sleep and screensaver
- Keeps applications active

### Performance Impact

- Minimal CPU usage (mostly sleeping)
- No memory leaks (Python garbage collection)
- Small memory footprint
- No impact on system performance

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'pyautogui'**

   - Solution: Run `pip install pyautogui`

2. **Permission denied**

   - Solution: Run from a location you have write access to

3. **Mouse not moving**

   - Check if interval is too long
   - Verify pyautogui is working: `python -c "import pyautogui; print(pyautogui.position())"`

4. **Still going to sleep**
   - Decrease interval (try 30 seconds)
   - Increase movement distance (try 2-3 pixels)

### Known Limitations

#### Standalone Versions
- Fixed intervals (60 seconds for batch/VBS, configurable for PowerShell)
- Basic error handling
- Windows only (by design)

#### Python Versions  
- Requires Python to be installed
- Doesn't work if Python process is suspended
- Mouse movements may be visible (by design for transparency)
- Failsafe: Move mouse to top-left corner to stop PyAutoGUI

## Files Overview

### Standalone Files (v2.0) ⭐
- `standalone_mouse_jiggler.bat` - Batch script version
- `standalone_mouse_jiggler.ps1` - PowerShell version  
- `standalone_mouse_jiggler.vbs` - VBScript version
- `STANDALONE_OPTIONS.md` - Complete documentation

### Python Files (Legacy)
- `mouse_jiggler.py` - Console version
- `tray_jiggler.py` - System tray version
- `advanced_jiggler.py` - Feature-rich version
- Various build scripts and executables

## License

This project is open source. Use responsibly and in accordance with your organization's policies.

## Disclaimer

This tool is for legitimate use cases such as:

- Preventing system sleep during long processes
- Keeping presentations active
- Maintaining remote connections
- Development/testing scenarios

Use in accordance with your organization's IT policies and local laws.
