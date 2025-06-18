"""
Windows Mouse Jiggler v1.1 - System Tray Edition
Runs headless in system tray with right-click menu controls

New Features in v1.1:
- System tray integration
- Right-click menu for start/stop/settings
- Headless operation (no console window)
- Visual status indicators
- Easy access to configuration
"""

import time
import threading
import sys
from datetime import datetime, timedelta
import json
import os

try:
    import pyautogui
    import pystray
    from PIL import Image, ImageDraw
except ImportError as e:
    print(f"Required packages not installed: {e}")
    print("Please install: pip install pyautogui pystray pillow")
    sys.exit(1)

class SystemTrayJiggler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 60  # seconds
        self.movement_distance = 1  # pixels
        self.total_jiggles = 0
        self.start_time = None
        self.config_file = "jiggler_config.json"
        
        # System tray
        self.icon = None
        self.status_text = "Stopped"
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        # Load configuration
        self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.interval = config.get('interval', 60)
                    self.movement_distance = config.get('movement_distance', 1)
        except Exception as e:
            pass  # Use defaults if config fails to load
            
    def save_config(self):
        """Save current configuration to file"""
        try:
            config = {
                'interval': self.interval,
                'movement_distance': self.movement_distance,
                'total_jiggles': self.total_jiggles
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            pass  # Silently fail if can't save
    
    def create_icon_image(self, color="red"):
        """Create a simple icon image"""
        # Create a 64x64 image
        image = Image.new('RGB', (64, 64), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        if color == "green":
            # Green circle for running
            draw.ellipse([8, 8, 56, 56], fill=(34, 139, 34), outline=(0, 100, 0))
        else:
            # Red circle for stopped
            draw.ellipse([8, 8, 56, 56], fill=(220, 20, 60), outline=(139, 0, 0))
          # Add a small mouse cursor symbol
        draw.polygon([(32, 20), (32, 44), (38, 38), (44, 44), (38, 32)], fill=(255, 255, 255))
        
        return image
    
    def jiggle_mouse(self):
        """Perform enhanced system activity simulation for Windows 11"""
        try:
            # Get current mouse position
            current_x, current_y = pyautogui.position()
            
            # Enhanced movement pattern for Windows 11 compatibility
            # Use multiple small movements in different directions
            movements = [
                (self.movement_distance, 0),
                (0, self.movement_distance), 
                (-self.movement_distance, 0),
                (0, -self.movement_distance)
            ]
            
            for dx, dy in movements:
                pyautogui.moveRel(dx, dy, duration=0.05)
                time.sleep(0.02)
            
            # Also simulate a very brief key press (Shift key) to ensure system activity
            # This is more reliable for preventing sleep on Windows 11
            try:
                pyautogui.keyDown('shift')
                time.sleep(0.01)
                pyautogui.keyUp('shift')
            except:
                pass  # Fallback to just mouse movement if key simulation fails
            
            self.total_jiggles += 1
            return True
        except Exception as e:
            return False
    
    def worker_thread(self):
        """Background thread that performs the jiggling"""
        self.start_time = datetime.now()
        
        while self.running:
            try:
                # Wait for the specified interval
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    self.jiggle_mouse()
                    # Update status
                    runtime = datetime.now() - self.start_time
                    self.status_text = f"Running - {self.total_jiggles} jiggles - {str(runtime).split('.')[0]}"
                    self.update_tray_icon()
                        
            except Exception as e:
                break
    
    def start_jiggling(self):
        """Start the mouse jiggler"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.worker_thread, daemon=True)
        self.thread.start()
        self.status_text = "Starting..."
        self.update_tray_icon()
    
    def stop_jiggling(self):
        """Stop the mouse jiggler"""
        if not self.running:
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        if self.start_time:
            runtime = datetime.now() - self.start_time
            self.status_text = f"Stopped - {self.total_jiggles} total jiggles"
        else:
            self.status_text = "Stopped"
        
        self.update_tray_icon()
        self.save_config()
    
    def toggle_jiggling(self, icon, item):
        """Toggle jiggling on/off"""
        if self.running:
            self.stop_jiggling()
        else:
            self.start_jiggling()
    
    def set_interval_30(self, icon, item):
        """Set interval to 30 seconds"""
        self.interval = 30
        self.save_config()
    
    def set_interval_60(self, icon, item):
        """Set interval to 60 seconds"""
        self.interval = 60
        self.save_config()
    
    def set_interval_120(self, icon, item):
        """Set interval to 120 seconds"""
        self.interval = 120
        self.save_config()
    
    def set_distance_1(self, icon, item):
        """Set movement distance to 1 pixel"""
        self.movement_distance = 1
        self.save_config()
    
    def set_distance_2(self, icon, item):
        """Set movement distance to 2 pixels"""
        self.movement_distance = 2
        self.save_config()
    
    def show_status(self, icon, item):
        """Show current status in a notification"""
        try:
            runtime = datetime.now() - self.start_time if self.start_time else "Not started"
            status = "Running" if self.running else "Stopped"
            
            message = f"Status: {status}\n"
            message += f"Interval: {self.interval}s\n"
            message += f"Distance: {self.movement_distance}px\n"
            message += f"Total jiggles: {self.total_jiggles}\n"
            if self.start_time:
                message += f"Runtime: {str(runtime).split('.')[0]}"
            
            icon.notify(message, "Mouse Jiggler Status")
        except Exception as e:
            pass
    
    def quit_app(self, icon, item):
        """Quit the application"""
        self.stop_jiggling()
        icon.stop()
    
    def update_tray_icon(self):
        """Update the tray icon based on current status"""
        if self.icon:
            color = "green" if self.running else "red"
            self.icon.icon = self.create_icon_image(color)
            self.icon.title = f"Mouse Jiggler - {self.status_text}"
    
    def create_menu(self):
        """Create the right-click context menu"""
        return pystray.Menu(
            pystray.MenuItem(
                "Start" if not self.running else "Stop",
                self.toggle_jiggling,
                default=True
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Interval",
                pystray.Menu(
                    pystray.MenuItem("30 seconds", self.set_interval_30),
                    pystray.MenuItem("60 seconds", self.set_interval_60),
                    pystray.MenuItem("120 seconds", self.set_interval_120)
                )
            ),
            pystray.MenuItem(
                "Movement",
                pystray.Menu(
                    pystray.MenuItem("1 pixel", self.set_distance_1),
                    pystray.MenuItem("2 pixels", self.set_distance_2)
                )
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Status", self.show_status),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        )
    
    def run(self):
        """Start the system tray application"""
        # Create the icon
        image = self.create_icon_image("red")  # Start with red (stopped)
        self.icon = pystray.Icon("mouse_jiggler", image, "Mouse Jiggler - Stopped", self.create_menu())
        
        # Show startup notification
        try:
            self.icon.notify("Mouse Jiggler started!\nRight-click for options.", "Mouse Jiggler v1.1")
        except:
            pass
        
        # Run the icon (this blocks until quit)
        self.icon.run()

def main():
    """Main entry point"""
    try:
        app = SystemTrayJiggler()
        app.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # If running from command line, show error
        if sys.stdout.isatty():
            print(f"Error starting Mouse Jiggler: {e}")
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
