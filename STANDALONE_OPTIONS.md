# Standalone Mouse Jiggler Options

This folder contains three standalone mouse jiggler implementations that don't require Python or Java:

## 1. Batch Script Version (`standalone_mouse_jiggler.bat`)

- **Most Compatible**: Works on any Windows system
- **Simplest**: Just double-click to run
- **Technology**: Windows Batch + PowerShell (built-in)
- **Best for**: Quick use, maximum compatibility

### Usage:

```
double-click standalone_mouse_jiggler.bat
```

## 2. PowerShell Version (`standalone_mouse_jiggler.ps1`)

- **Most Advanced**: Full configurability and error handling
- **Flexible**: Command-line options available
- **Technology**: Pure PowerShell (built-in on Windows 7+)
- **Best for**: Power users, customization needed

### Usage:

```powershell
# Basic usage
.\standalone_mouse_jiggler.ps1

# Custom interval (30 seconds)
.\standalone_mouse_jiggler.ps1 -Interval 30

# Custom distance and silent mode
.\standalone_mouse_jiggler.ps1 -Interval 45 -Distance 2 -Silent

# Show help
.\standalone_mouse_jiggler.ps1 -Help
```

## 3. VBScript Version (`standalone_mouse_jiggler.vbs`)

- **Lightest**: Minimal resource usage
- **Universal**: Works on very old Windows systems (XP+)
- **Technology**: Windows Scripting Host (always present)
- **Best for**: Older systems, minimal impact

### Usage:

```
# With console output
cscript standalone_mouse_jiggler.vbs

# Background mode (no console)
wscript standalone_mouse_jiggler.vbs

# Show help
cscript standalone_mouse_jiggler.vbs /help
```

## Comparison

| Feature        | Batch       | PowerShell | VBScript    |
| -------------- | ----------- | ---------- | ----------- |
| Compatibility  | All Windows | Win 7+     | All Windows |
| Configuration  | Fixed       | Full       | Limited     |
| Resource Usage | Low         | Medium     | Lowest      |
| Error Handling | Basic       | Advanced   | Basic       |
| Ease of Use    | Highest     | Medium     | Medium      |

## Security Notes

All versions:

- Use minimal mouse movements (1-2 pixels)
- Don't install anything on the system
- Use only built-in Windows components
- Can be easily stopped with Ctrl+C
- Leave no traces when stopped

## Recommendations

- **For most users**: Use the **Batch version** - just double-click and go
- **For customization**: Use the **PowerShell version** with your preferred settings
- **For old systems**: Use the **VBScript version** if PowerShell isn't available

All versions prevent your computer from going to sleep without requiring any external dependencies!
