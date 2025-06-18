"""
KVM-Safe System Tray Jiggler - Version 1.2
Works even when mouse is disconnected via KVM switch

This version runs in the system tray and uses Windows system calls
instead of mouse movements to prevent sleep.
"""

import time
import threading
import sys
from datetime import datetime
import ctypes
from ctypes import wintypes

try:
    import pystray
    from pystray import MenuItem as item
    from PIL import Image, ImageDraw
except ImportError:
    print("Required packages not installed. Please run:")
    print("pip install pystray pillow")
    sys.exit(1)

# Windows constants for SetThreadExecutionState
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

class KVMSafeTrayJiggler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 60  # seconds
        self.total_jiggles = 0
        self.start_time = None
        self.use_display_required = True
        self.icon = None
        
    def create_icon_image(self, color="green"):
        """Create a simple icon image"""
        image = Image.new('RGB', (64, 64), color="white")
        draw = ImageDraw.Draw(image)
        
        if color == "green":
            # Green circle for running
            draw.ellipse([8, 8, 56, 56], fill="green", outline="darkgreen", width=2)
            draw.text((24, 26), "ON", fill="white")
        else:
            # Red circle for stopped
            draw.ellipse([8, 8, 56, 56], fill="red", outline="darkred", width=2)
            draw.text((20, 26), "OFF", fill="white")
        
        return image
    
    def prevent_sleep(self):
        """Use Windows API to prevent system sleep - KVM safe"""
        try:
            if self.use_display_required:
                # Prevent both system sleep and display sleep
                result = ctypes.windll.kernel32.SetThreadExecutionState(
                    ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
                )
            else:
                # Only prevent system sleep, allow display sleep
                result = ctypes.windll.kernel32.SetThreadExecutionState(
                    ES_CONTINUOUS | ES_SYSTEM_REQUIRED
                )
            
            if result != 0:
                self.total_jiggles += 1
                return True
            else:
                return self.fallback_method()
                
        except Exception as e:
            return self.fallback_method()
    
    def fallback_method(self):
        """Fallback method using keybd_event"""
        try:
            VK_SHIFT = 0x10
            KEYEVENTF_KEYUP = 0x0002
            
            # Brief shift key press
            ctypes.windll.user32.keybd_event(VK_SHIFT, 0, 0, 0)
            time.sleep(0.01)
            ctypes.windll.user32.keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, 0)
            
            self.total_jiggles += 1
            return True
            
        except Exception:
            return False
    
    def reset_sleep_prevention(self):
        """Reset the execution state to allow normal sleep"""
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        except Exception:
            pass
    
    def worker_thread(self):
        """Background thread that prevents sleep"""
        self.start_time = datetime.now()
        
        while self.running:
            try:
                # Wait for the specified interval
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    self.prevent_sleep()
                    # Update icon to show activity
                    if self.icon:
                        self.update_icon_title()
                        
            except Exception:
                break
        
        # Reset when stopping
        self.reset_sleep_prevention()
    
    def start_jiggling(self, icon=None, item=None):
        """Start preventing sleep"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.worker_thread, daemon=True)
        self.thread.start()
        
        # Update icon
        if self.icon:
            self.icon.icon = self.create_icon_image("green")
            self.update_icon_title()
    
    def stop_jiggling(self, icon=None, item=None):
        """Stop preventing sleep"""
        if not self.running:
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        self.reset_sleep_prevention()
        
        # Update icon
        if self.icon:
            self.icon.icon = self.create_icon_image("red")
            self.update_icon_title()
    
    def toggle_display_mode(self, icon=None, item=None):
        """Toggle display keep-awake mode"""
        self.use_display_required = not self.use_display_required
        if self.icon:
            self.update_icon_title()
    
    def set_interval_30(self, icon=None, item=None):
        """Set interval to 30 seconds"""
        self.interval = 30
        if self.icon:
            self.update_icon_title()
    
    def set_interval_60(self, icon=None, item=None):
        """Set interval to 60 seconds"""
        self.interval = 60
        if self.icon:
            self.update_icon_title()
    
    def set_interval_120(self, icon=None, item=None):
        """Set interval to 120 seconds"""
        self.interval = 120
        if self.icon:
            self.update_icon_title()
    
    def show_status(self, icon=None, item=None):
        """Show status information"""
        status = "Running" if self.running else "Stopped"
        runtime = datetime.now() - self.start_time if self.start_time else None
        display_mode = "Keep awake" if self.use_display_required else "Allow sleep"
        
        message = f"Status: {status}\n"
        message += f"Interval: {self.interval}s\n"
        message += f"Display: {display_mode}\n"
        message += f"Preventions: {self.total_jiggles}\n"
        if runtime:
            message += f"Runtime: {runtime}"
        
        # Simple message display (Windows notification would be better but requires more dependencies)
        print(message)  # In a real app, you'd show a popup
    
    def update_icon_title(self):
        """Update the icon tooltip"""
        if not self.icon:
            return
            
        status = "Running" if self.running else "Stopped"
        display_mode = "Keep Display" if self.use_display_required else "Allow Display Sleep"
        title = f"KVM-Safe Jiggler: {status}\n"
        title += f"Interval: {self.interval}s | {display_mode}\n"
        title += f"Preventions: {self.total_jiggles}"
        
        self.icon.title = title
    
    def quit_app(self, icon=None, item=None):
        """Quit the application"""
        self.stop_jiggling()
        if self.icon:
            self.icon.stop()
    
    def create_menu(self):
        """Create the system tray context menu"""
        return pystray.Menu(
            item('Start', self.start_jiggling, enabled=lambda item: not self.running),
            item('Stop', self.stop_jiggling, enabled=lambda item: self.running),
            pystray.Menu.SEPARATOR,
            item('Interval: 30s', self.set_interval_30),
            item('Interval: 60s', self.set_interval_60),
            item('Interval: 120s', self.set_interval_120),
            pystray.Menu.SEPARATOR,
            item('Toggle Display Mode', self.toggle_display_mode),
            item('Show Status', self.show_status),
            pystray.Menu.SEPARATOR,
            item('Quit', self.quit_app)
        )
    
    def run(self):
        """Run the system tray application"""
        # Create initial icon
        icon_image = self.create_icon_image("red")
        
        # Create system tray icon
        self.icon = pystray.Icon(
            "KVMSafeJiggler",
            icon_image,
            "KVM-Safe Jiggler: Stopped\nRight-click for options",
            menu=self.create_menu()
        )
        
        print("KVM-Safe Jiggler started in system tray")
        print("Right-click the tray icon for options")
        print("Uses Windows system calls - works with KVM switches!")
        
        # Run the icon (this blocks)
        self.icon.run()

def main():
    """Main entry point"""
    try:
        jiggler = KVMSafeTrayJiggler()
        jiggler.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
