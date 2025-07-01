# Changelog

## Version 1.1.0 - System Tray Edition (2025-06-18)

### 🎉 Major New Features

- **System Tray Integration**: Runs headless in system tray with visual status indicators
- **Right-Click Menu**: Easy access to all controls without command line
- **Visual Status**: Color-coded icons (red=stopped, green=running)
- **Background Operation**: No console window, runs silently in background
- **Smart Notifications**: Status updates and startup notifications

### ✨ Enhanced User Experience

- **One-Click Start/Stop**: Toggle jiggling with single menu click
- **Quick Settings**: Change interval (30/60/120s) and distance (1/2px) from menu
- **Status Information**: View runtime, jiggle count, and settings via menu
- **Persistent Configuration**: Settings automatically saved and restored
- **Easy Deployment**: Single executable file for distribution

### 🛠️ Technical Improvements

- **New Dependencies**: Added pystray and pillow for system tray functionality
- **Enhanced Error Handling**: Graceful fallbacks for system tray operations
- **Improved Threading**: Better background task management
- **Dynamic Icons**: Programmatically generated status icons
- **Memory Efficiency**: Optimized for long-running background operation

### 📦 Distribution

- **Standalone Executable**: `MouseJiggler_v1.1_SystemTray.exe` (~17MB)
- **No Installation Required**: Copy and run on any Windows machine
- **Python Source**: Available for customization and development

### 🔧 Menu Options

- **Start/Stop**: Toggle jiggling operation
- **Interval Settings**: 30, 60, or 120 seconds
- **Movement Distance**: 1 or 2 pixels
- **Status Display**: Show current configuration and statistics
- **Quit**: Clean shutdown with settings preservation

---

## Version 1.0.0 - Initial Release (2025-06-17)

### 🎯 Core Features

- **Basic Mouse Jiggler**: Command-line interface with interactive controls
- **Advanced Version**: Enterprise features with activity logging
- **Security-Friendly Design**: Minimal movements using standard Windows APIs
- **Standalone Support**: PyInstaller builds for distribution
- **Multiple Interfaces**: Console and windowed versions

### 🛡️ Security Focus

- **Transparent Operation**: Uses legitimate PyAutoGUI library
- **Minimal Movements**: 1-2 pixel movements that return to origin
- **Standard APIs**: No low-level injection or suspicious techniques
- **Emergency Stop**: Failsafe mouse-to-corner termination
- **Activity Logging**: Full audit trail for enterprise environments

### 📋 Initial Commands

- `start/stop` - Control jiggling operation
- `interval X` - Set time between jiggles (5-300 seconds)
- `distance X` - Set movement distance (1-10 pixels)
- `status` - Show current configuration
- `help` - Display available commands

### 🚀 Distribution Options

- **Python Scripts**: For development and customization
- **Standalone Executables**: For easy deployment
- **Build Scripts**: Automated compilation with PyInstaller
- **Documentation**: Comprehensive usage guides and security information

---

## Roadmap

### Potential Future Features

- **Custom Intervals**: User-defined timing beyond preset options
- **Movement Patterns**: Different jiggle patterns (circle, figure-8, etc.)
- **Scheduled Operation**: Time-based automatic start/stop
- **Multiple Monitor Support**: Awareness of multi-display setups
- **Hotkey Support**: Global keyboard shortcuts for quick control
- **Statistics Dashboard**: Detailed usage analytics and reporting
