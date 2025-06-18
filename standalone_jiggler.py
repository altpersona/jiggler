"""
Standalone Windows Mouse Jiggler
Optimized for PyInstaller compilation - No Python Required!

This version is designed to be compiled into a standalone .exe
that can run on any Windows machine without Python installed.
"""

import time
import sys
import threading
from datetime import datetime

# Try to import pyautogui with error handling for standalone builds
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
except ImportError as e:
    print("Error: PyAutoGUI not available. This shouldn't happen in standalone build.")
    print(f"Import error: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

class StandaloneMouseJiggler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 60  # seconds
        self.movement_distance = 1  # pixels
        self.total_jiggles = 0
        self.start_time = None
        
    def jiggle_mouse(self):
        """Perform minimal mouse movement"""
        try:
            # Get current position
            current_x, current_y = pyautogui.position()
            
            # Minimal movement pattern: right and back
            pyautogui.moveRel(self.movement_distance, 0, duration=0.05)
            time.sleep(0.02)
            pyautogui.moveRel(-self.movement_distance, 0, duration=0.05)
            
            self.total_jiggles += 1
            return True
            
        except Exception as e:
            print(f"Error during mouse movement: {e}")
            return False
    
    def worker_thread(self):
        """Background thread for jiggling"""
        self.start_time = datetime.now()
        print(f"Mouse jiggler started - interval: {self.interval}s, movement: {self.movement_distance}px")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                # Wait for interval
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    if self.jiggle_mouse():
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] Jiggle #{self.total_jiggles} - system kept active")
                    
            except Exception as e:
                print(f"Error in worker thread: {e}")
                break
    
    def start(self):
        """Start the jiggler"""
        if self.running:
            print("Already running!")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.worker_thread, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the jiggler"""
        if not self.running:
            print("Not running!")
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        runtime = datetime.now() - self.start_time if self.start_time else None
        print(f"\nStopped after {runtime} - {self.total_jiggles} total jiggles")
    
    def set_interval(self, seconds):
        """Set jiggle interval"""
        if seconds < 5:
            print("Minimum interval is 5 seconds")
            return False
        self.interval = seconds
        print(f"Interval set to {seconds} seconds")
        return True
    
    def set_distance(self, pixels):
        """Set movement distance"""
        if pixels < 1 or pixels > 10:
            print("Distance must be 1-10 pixels")
            return False
        self.movement_distance = pixels
        print(f"Movement distance set to {pixels} pixels")
        return True
    
    def get_status(self):
        """Get current status"""
        status = "Running" if self.running else "Stopped"
        runtime = datetime.now() - self.start_time if self.start_time else "Not started"
        return {
            'status': status,
            'runtime': str(runtime),
            'total_jiggles': self.total_jiggles,
            'interval': self.interval,
            'distance': self.movement_distance
        }

def print_help():
    """Print available commands"""
    print("""
Available Commands:
start              - Start mouse jiggler
stop               - Stop mouse jiggler
interval <seconds> - Set interval (5-300 seconds)
distance <pixels>  - Set movement distance (1-10 pixels)
status             - Show current status
help               - Show this help
quit/exit          - Exit program

Examples:
> interval 30      # Jiggle every 30 seconds
> distance 2       # Move 2 pixels
> start            # Begin jiggling
> stop             # Stop jiggling
""")

def main():
    # Check if we can access mouse (basic functionality test)
    try:
        pos = pyautogui.position()
        print(f"Mouse access OK - current position: {pos}")
    except Exception as e:
        print(f"Error: Cannot access mouse functionality: {e}")
        input("Press Enter to exit...")
        return
    
    jiggler = StandaloneMouseJiggler()
    
    print("=" * 60)
    print("Windows Mouse Jiggler - Standalone Version")
    print("=" * 60)
    print("No Python installation required!")
    print("Performs minimal mouse movements to prevent system sleep.")
    print()
    print("Quick start: type 'start' to begin, 'help' for all commands")
    print("Emergency stop: move mouse to top-left corner")
    print("=" * 60)
    
    try:
        while True:
            try:
                command = input("\n> ").strip().lower()
                parts = command.split()
                
                if command == "start":
                    jiggler.start()
                elif command == "stop":
                    jiggler.stop()
                elif command == "status":
                    status = jiggler.get_status()
                    print("\nCurrent Status:")
                    for key, value in status.items():
                        print(f"  {key.replace('_', ' ').title()}: {value}")
                elif command == "help":
                    print_help()
                elif command in ["quit", "exit"]:
                    if jiggler.running:
                        jiggler.stop()
                    print("Goodbye!")
                    break
                elif parts[0] == "interval" and len(parts) == 2:
                    try:
                        seconds = int(parts[1])
                        if 5 <= seconds <= 300:
                            jiggler.set_interval(seconds)
                        else:
                            print("Interval must be between 5-300 seconds")
                    except ValueError:
                        print("Usage: interval <seconds>")
                elif parts[0] == "distance" and len(parts) == 2:
                    try:
                        pixels = int(parts[1])
                        jiggler.set_distance(pixels)
                    except ValueError:
                        print("Usage: distance <pixels>")
                elif command == "":
                    continue
                else:
                    print(f"Unknown command: '{command}' - type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n\nCtrl+C pressed - stopping...")
                if jiggler.running:
                    jiggler.stop()
                break
            except EOFError:
                if jiggler.running:
                    jiggler.stop()
                break
                
    except Exception as e:
        print(f"Unexpected error: {e}")
        if jiggler.running:
            jiggler.stop()
    
    # Keep console open if running as .exe
    if getattr(sys, 'frozen', False):
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
