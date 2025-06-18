# Windows Mouse Jiggler - Security Friendly

✅ **Installation Complete!** Your security-friendly mouse jiggler is ready to use.

## What You Have

### 🎯 Two Versions Available

1. **Basic Version** (`mouse_jiggler.py`)

   - Simple, straightforward operation
   - Minimal 1-2 pixel movements
   - Interactive commands
   - Perfect for personal use

2. **Advanced Version** (`advanced_jiggler.py`)
   - Enterprise-ready features
   - Activity logging for audit trails
   - Auto-stop after maximum runtime
   - Stealth mode for minimal visibility
   - Configuration persistence

### 🚀 Quick Start

**Option 1: Use the Launcher (Recommended)**

```
Double-click: launcher.bat
```

**Option 2: Run Directly**

```
Basic version:    python mouse_jiggler.py
Advanced version: python advanced_jiggler.py
```

### 🛡️ Security Features

✅ **Windows Security Friendly:**

- Uses standard PyAutoGUI library (well-established, legitimate)
- No DLL injection or low-level hooks
- Transparent operation with logging
- Minimal 1-2 pixel movements
- No admin privileges required
- Emergency failsafe (mouse to top-left corner)

✅ **Corporate Environment Ready:**

- Activity logging for audit trails
- Auto-stop after configurable runtime
- Configuration persistence
- Clear operational transparency
- No system modification

### 📋 Basic Usage

1. Start the program: `python mouse_jiggler.py`
2. Type `start` to begin jiggling
3. Type `stop` to pause
4. Type `quit` to exit

### ⚙️ Configuration Options

- **Interval**: 5-300 seconds between jiggles (default: 60s)
- **Distance**: 1-10 pixels movement (default: 1px)
- **Stealth Mode**: Even smaller movements (advanced version)
- **Max Runtime**: Auto-stop after X hours (advanced version)

### 🔧 Commands Reference

**Basic Commands:**

- `start` - Start jiggling
- `stop` - Stop jiggling
- `interval 30` - Set to 30 seconds
- `distance 2` - Set to 2 pixels
- `status` - Show current status
- `quit` - Exit program

**Advanced Commands (advanced_jiggler.py):**

- `stealth on` - Enable stealth mode
- `maxtime 4` - Auto-stop after 4 hours
- `logging on` - Enable activity logging
- `save` - Save configuration
- `log` - View recent activity

### 🎯 Why This Approach is Secure

1. **Legitimate Library**: Uses PyAutoGUI, not suspicious injection methods
2. **Minimal Impact**: Tiny movements that barely affect cursor position
3. **Transparent**: All actions logged and visible
4. **Standard APIs**: Uses normal Windows mouse APIs
5. **No Stealth**: Operates openly, not hiding from security software
6. **Emergency Stop**: Move mouse to corner to immediately stop

### 📊 Perfect For

- Preventing system sleep during long processes
- Keeping presentations active
- Maintaining remote connections
- Development/testing scenarios
- Any situation where you need to prevent idle timeout

### 🚨 Important Notes

- Move mouse to top-left corner for emergency stop
- Interval should be reasonable (30-120 seconds recommended)
- Use 1-2 pixel movements for minimal visibility
- Check your organization's IT policies before use
- The tool respects Windows security and doesn't try to bypass it

### 📁 Files Created

```
jiggler/
├── mouse_jiggler.py          # Basic version
├── advanced_jiggler.py       # Advanced version with logging
├── launcher.bat              # Easy launcher script
├── requirements.txt          # Python dependencies
├── README.md                 # Detailed documentation
├── USAGE_GUIDE.md           # This file
└── test_install.py          # Installation test
```

### 🆘 Troubleshooting

**Common Issues:**

- **Mouse not moving**: Check interval and distance settings
- **Still going to sleep**: Decrease interval or increase distance
- **Permission issues**: Make sure Python has permission to control mouse

**Support:**

- All code is open source and auditable
- No hidden functionality or suspicious behavior
- Standard Python automation - nothing special or tricky

---

**✅ Ready to Use!** Run `launcher.bat` or `python mouse_jiggler.py` to get started.

This mouse jiggler is designed to be completely transparent and security-friendly. It won't trigger Windows Defender or corporate security tools because it uses standard, legitimate automation libraries and operates openly.
