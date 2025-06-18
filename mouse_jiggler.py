"""
Windows Mouse Jiggler - Security Friendly Version

This mouse jiggler is designed to be minimal and transparent to avoid
triggering Windows security features. It uses small, subtle movements
and provides clear user control.

Features:
- Minimal mouse movements (1-2 pixels)
- Configurable intervals
- Easy start/stop with keyboard shortcuts
- Visual feedback in console
- Graceful shutdown
"""

import time
import pyautogui
import threading
import sys
from datetime import datetime

class MouseJiggler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 60  # Default: move every 60 seconds
        self.movement_distance = 1  # Very small movement
        
        # Disable pyautogui failsafe for controlled operation
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
    def jiggle_mouse(self):
        """Perform a subtle mouse movement"""
        try:
            # Get current mouse position
            current_x, current_y = pyautogui.position()
            
            # Move mouse slightly and return to original position
            pyautogui.moveRel(self.movement_distance, 0, duration=0.1)
            time.sleep(0.05)
            pyautogui.moveRel(-self.movement_distance, 0, duration=0.1)
            
            return True
        except Exception as e:
            print(f"Error during mouse movement: {e}")
            return False
    
    def worker_thread(self):
        """Background thread that performs the jiggling"""
        print(f"Mouse jiggler started. Moving every {self.interval} seconds.")
        print("Press Ctrl+C to stop gracefully.\n")
        
        while self.running:
            try:
                # Wait for the specified interval
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    if self.jiggle_mouse():
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] Mouse jiggled - keeping system active")
                    else:
                        print(f"[{timestamp}] Failed to jiggle mouse")
                        
            except Exception as e:
                print(f"Error in worker thread: {e}")
                break
    
    def start(self):
        """Start the mouse jiggler"""
        if self.running:
            print("Mouse jiggler is already running!")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.worker_thread, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the mouse jiggler"""
        if not self.running:
            print("Mouse jiggler is not running!")
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("Mouse jiggler stopped.")
    
    def set_interval(self, seconds):
        """Set the interval between jiggles"""
        if seconds < 5:
            print("Minimum interval is 5 seconds")
            return
        self.interval = seconds
        print(f"Interval set to {seconds} seconds")
    
    def set_movement_distance(self, pixels):
        """Set the movement distance (1-5 pixels recommended)"""
        if pixels < 1 or pixels > 10:
            print("Movement distance should be between 1-10 pixels")
            return
        self.movement_distance = pixels
        print(f"Movement distance set to {pixels} pixels")

def print_help():
    """Print help information"""
    help_text = """
Windows Mouse Jiggler - Commands:

start          - Start the mouse jiggler
stop           - Stop the mouse jiggler  
interval X     - Set interval to X seconds (minimum 5)
distance X     - Set movement distance to X pixels (1-10)
status         - Show current status
help           - Show this help
quit/exit      - Exit the program

Example:
> interval 30    # Set to jiggle every 30 seconds
> distance 2     # Set movement to 2 pixels
> start          # Begin jiggling
> stop           # Stop jiggling
"""
    print(help_text)

def main():
    jiggler = MouseJiggler()
    
    print("=" * 60)
    print("Windows Mouse Jiggler - Security Friendly Version")
    print("=" * 60)
    print("This tool performs minimal mouse movements to prevent")
    print("system sleep/screensaver activation.")
    print()
    print("Type 'help' for commands or 'start' to begin.")
    print("=" * 60)
    
    try:
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == "start":
                    jiggler.start()
                elif command == "stop":
                    jiggler.stop()
                elif command == "status":
                    status = "Running" if jiggler.running else "Stopped"
                    print(f"Status: {status}")
                    print(f"Interval: {jiggler.interval} seconds")
                    print(f"Movement: {jiggler.movement_distance} pixels")
                elif command == "help":
                    print_help()
                elif command in ["quit", "exit"]:
                    if jiggler.running:
                        jiggler.stop()
                    print("Goodbye!")
                    break
                elif command.startswith("interval "):
                    try:
                        seconds = int(command.split()[1])
                        jiggler.set_interval(seconds)
                    except (IndexError, ValueError):
                        print("Usage: interval <seconds>")
                elif command.startswith("distance "):
                    try:
                        pixels = int(command.split()[1])
                        jiggler.set_movement_distance(pixels)
                    except (IndexError, ValueError):
                        print("Usage: distance <pixels>")
                elif command == "":
                    continue
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n\nReceived Ctrl+C - stopping gracefully...")
                if jiggler.running:
                    jiggler.stop()
                break
            except EOFError:
                print("\nExiting...")
                if jiggler.running:
                    jiggler.stop()
                break
                
    except Exception as e:
        print(f"Unexpected error: {e}")
        if jiggler.running:
            jiggler.stop()

if __name__ == "__main__":
    main()
