"""
KVM-Safe Windows Jiggler - Version 1.2
Works even when mouse is disconnected via KVM switch

This version uses Windows system calls instead of mouse movements
to prevent the system from going to sleep, making it KVM-switch safe.
"""

import time
import threading
import sys
from datetime import datetime
import ctypes
from ctypes import wintypes

# Windows constants for SetThreadExecutionState
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040

class KVMSafeJiggler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 60  # seconds
        self.total_jiggles = 0
        self.start_time = None
        self.use_display_required = True
        
    def prevent_sleep(self):
        """Use Windows API to prevent system sleep - KVM safe"""
        try:
            # Method 1: SetThreadExecutionState to prevent sleep
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
                print("Warning: SetThreadExecutionState failed")
                return self.fallback_method()
                
        except Exception as e:
            print(f"Error in prevent_sleep: {e}")
            return self.fallback_method()
    
    def fallback_method(self):
        """Fallback method using keybd_event for very old systems"""
        try:
            # Send a "do nothing" key event (VK_SHIFT press and release)
            # This is less intrusive than mouse movement
            VK_SHIFT = 0x10
            KEYEVENTF_KEYUP = 0x0002
            
            # Press shift (very briefly)
            ctypes.windll.user32.keybd_event(VK_SHIFT, 0, 0, 0)
            time.sleep(0.01)  # 10ms
            # Release shift
            ctypes.windll.user32.keybd_event(VK_SHIFT, 0, KEYEVENTF_KEYUP, 0)
            
            self.total_jiggles += 1
            return True
            
        except Exception as e:
            print(f"Fallback method failed: {e}")
            return False
    
    def reset_sleep_prevention(self):
        """Reset the execution state to allow normal sleep"""
        try:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        except Exception as e:
            print(f"Error resetting sleep prevention: {e}")
    
    def worker_thread(self):
        """Background thread that prevents sleep"""
        self.start_time = datetime.now()
        print(f"KVM-Safe jiggler started. Interval: {self.interval}s")
        print("Uses Windows system calls - works even with KVM switches!")
        print("Press Ctrl+C to stop\n")
        
        while self.running:
            try:
                # Wait for the specified interval
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    if self.prevent_sleep():
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] Sleep prevented #{self.total_jiggles} - system kept active")
                    else:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"[{timestamp}] Warning: Failed to prevent sleep")
                        
            except Exception as e:
                print(f"Error in worker thread: {e}")
                break
        
        # Reset when stopping
        self.reset_sleep_prevention()
    
    def start(self):
        """Start the jiggler"""
        if self.running:
            print("KVM-Safe jiggler is already running!")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.worker_thread, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the jiggler"""
        if not self.running:
            print("KVM-Safe jiggler is not running!")
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        self.reset_sleep_prevention()
        
        if self.start_time:
            runtime = datetime.now() - self.start_time
            print(f"\nKVM-Safe jiggler stopped after {runtime}")
            print(f"Total sleep preventions: {self.total_jiggles}")
    
    def set_interval(self, seconds):
        """Set the interval between sleep preventions"""
        if seconds < 5:
            print("Minimum interval is 5 seconds")
            return
        self.interval = seconds
        print(f"Interval set to {seconds} seconds")
    
    def set_display_mode(self, keep_display_on):
        """Set whether to keep display on or allow it to sleep"""
        self.use_display_required = keep_display_on
        mode = "keep display awake" if keep_display_on else "allow display sleep"
        print(f"Display mode: {mode}")
    
    def get_status(self):
        """Get current status"""
        status = "Running" if self.running else "Stopped"
        runtime = datetime.now() - self.start_time if self.start_time else None
        
        print(f"\nStatus: {status}")
        print(f"Interval: {self.interval} seconds")
        print(f"Display mode: {'Keep awake' if self.use_display_required else 'Allow sleep'}")
        print(f"Total preventions: {self.total_jiggles}")
        if runtime:
            print(f"Runtime: {runtime}")

def print_help():
    """Print help information"""
    help_text = """
KVM-Safe Windows Jiggler - Commands:

start              - Start preventing sleep
stop               - Stop preventing sleep
interval X         - Set interval to X seconds (minimum 5)
display on/off     - Keep display awake or allow display sleep
status             - Show current status
help               - Show this help
quit/exit          - Exit the program

Example:
> interval 30      # Prevent sleep every 30 seconds
> display off      # Allow display to sleep, keep system awake
> start            # Begin preventing sleep
> stop             # Stop preventing sleep

KVM Switch Safe:
This version uses Windows system calls instead of mouse movements,
so it works even when your mouse/keyboard is switched to another
computer via a KVM switch.

Display Modes:
- display on  = Keep both system and display awake
- display off = Keep system awake, allow display to sleep
"""
    print(help_text)

def main():
    print("=" * 65)
    print("KVM-Safe Windows Jiggler - Version 1.2")
    print("=" * 65)
    print("Uses Windows system calls instead of mouse movements")
    print("Works even when mouse is disconnected via KVM switch!")
    print()
    print("Type 'help' for commands or 'start' to begin.")
    print("=" * 65)
    
    jiggler = KVMSafeJiggler()
    
    try:
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == "start":
                    jiggler.start()
                elif command == "stop":
                    jiggler.stop()
                elif command == "status":
                    jiggler.get_status()
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
                elif command.startswith("display "):
                    try:
                        mode = command.split()[1]
                        if mode in ["on", "true", "yes"]:
                            jiggler.set_display_mode(True)
                        elif mode in ["off", "false", "no"]:
                            jiggler.set_display_mode(False)
                        else:
                            print("Usage: display on/off")
                    except IndexError:
                        print("Usage: display on/off")
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
