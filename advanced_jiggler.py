"""
Advanced Windows Mouse Jiggler - Maximum Security Compliance

This version includes additional features for enterprise environments
and maximum security compliance.
"""

import time
import pyautogui
import threading
import sys
import json
import os
import logging
from datetime import datetime, timedelta
from pathlib import Path

class AdvancedMouseJiggler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.interval = 60
        self.movement_distance = 1
        self.total_jiggles = 0
        self.start_time = None
        self.config_file = "jiggler_config.json"
        self.log_file = "jiggler_activity.log"
        
        # Security features
        self.max_runtime_hours = 8  # Auto-stop after 8 hours
        self.activity_logging = True
        self.stealth_mode = False  # If True, even smaller movements
        
        # Setup logging
        self.setup_logging()
        
        # Load configuration
        self.load_config()
        
        # Configure pyautogui for security
        pyautogui.FAILSAFE = True  # Move to corner to emergency stop
        pyautogui.PAUSE = 0.1
        
    def setup_logging(self):
        """Setup activity logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.interval = config.get('interval', 60)
                    self.movement_distance = config.get('movement_distance', 1)
                    self.max_runtime_hours = config.get('max_runtime_hours', 8)
                    self.stealth_mode = config.get('stealth_mode', False)
                    self.activity_logging = config.get('activity_logging', True)
                    print("Configuration loaded from file")
        except Exception as e:
            print(f"Could not load config: {e}")
            
    def save_config(self):
        """Save current configuration to file"""
        try:
            config = {
                'interval': self.interval,
                'movement_distance': self.movement_distance,
                'max_runtime_hours': self.max_runtime_hours,
                'stealth_mode': self.stealth_mode,
                'activity_logging': self.activity_logging
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print("Configuration saved")
        except Exception as e:
            print(f"Could not save config: {e}")
            
    def jiggle_mouse(self):
        """Perform mouse movement with security considerations"""
        try:
            # Get current position
            current_x, current_y = pyautogui.position()
            
            # In stealth mode, use even smaller movements
            distance = self.movement_distance
            if self.stealth_mode:
                distance = max(1, distance // 2)
            
            # Perform minimal movement pattern
            # Pattern: right -> back -> down -> back (forms tiny square)
            movements = [
                (distance, 0),
                (-distance, 0),
                (0, distance),
                (0, -distance)
            ]
            
            for dx, dy in movements:
                pyautogui.moveRel(dx, dy, duration=0.05)
                time.sleep(0.02)
            
            self.total_jiggles += 1
            
            if self.activity_logging:
                self.logger.info(f"Mouse jiggle #{self.total_jiggles} completed")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during mouse movement: {e}")
            return False
    
    def check_runtime_limit(self):
        """Check if maximum runtime has been exceeded"""
        if self.start_time:
            runtime = datetime.now() - self.start_time
            max_runtime = timedelta(hours=self.max_runtime_hours)
            
            if runtime > max_runtime:
                self.logger.warning(f"Maximum runtime of {self.max_runtime_hours} hours exceeded. Auto-stopping.")
                return True
        return False
    
    def worker_thread(self):
        """Enhanced background thread with security features"""
        self.start_time = datetime.now()
        self.logger.info(f"Mouse jiggler started. Interval: {self.interval}s, Distance: {self.movement_distance}px")
        self.logger.info(f"Stealth mode: {self.stealth_mode}, Max runtime: {self.max_runtime_hours}h")
        
        while self.running:
            try:
                # Check runtime limit
                if self.check_runtime_limit():
                    self.running = False
                    break
                
                # Wait for the specified interval
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    success = self.jiggle_mouse()
                    if not success:
                        self.logger.error("Failed to perform mouse jiggle")
                        
            except Exception as e:
                self.logger.error(f"Error in worker thread: {e}")
                break
        
        self.logger.info("Mouse jiggler stopped")
    
    def start(self):
        """Start the mouse jiggler with enhanced checks"""
        if self.running:
            print("Mouse jiggler is already running!")
            return
        
        # Security confirmation
        print(f"Starting mouse jiggler with the following settings:")
        print(f"  Interval: {self.interval} seconds")
        print(f"  Movement: {self.movement_distance} pixels")
        print(f"  Stealth mode: {self.stealth_mode}")
        print(f"  Max runtime: {self.max_runtime_hours} hours")
        print(f"  Activity logging: {self.activity_logging}")
        
        self.running = True
        self.thread = threading.Thread(target=self.worker_thread, daemon=True)
        self.thread.start()
        
        if self.activity_logging:
            self.logger.info("Mouse jiggler started by user")
    
    def stop(self):
        """Stop the mouse jiggler"""
        if not self.running:
            print("Mouse jiggler is not running!")
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
        runtime = datetime.now() - self.start_time if self.start_time else timedelta(0)
        print(f"Mouse jiggler stopped after {runtime}")
        print(f"Total jiggles performed: {self.total_jiggles}")
        
        if self.activity_logging:
            self.logger.info(f"Mouse jiggler stopped. Runtime: {runtime}, Total jiggles: {self.total_jiggles}")
    
    def get_status(self):
        """Get detailed status information"""
        status = "Running" if self.running else "Stopped"
        runtime = datetime.now() - self.start_time if self.start_time else timedelta(0)
        
        status_info = {
            'status': status,
            'runtime': str(runtime),
            'total_jiggles': self.total_jiggles,
            'interval': self.interval,
            'movement_distance': self.movement_distance,
            'stealth_mode': self.stealth_mode,
            'max_runtime_hours': self.max_runtime_hours,
            'activity_logging': self.activity_logging
        }
        
        return status_info
    
    def set_stealth_mode(self, enabled):
        """Enable/disable stealth mode for minimal movements"""
        self.stealth_mode = enabled
        mode = "enabled" if enabled else "disabled"
        print(f"Stealth mode {mode}")
        self.logger.info(f"Stealth mode {mode}")
    
    def set_max_runtime(self, hours):
        """Set maximum runtime in hours"""
        if hours < 1 or hours > 24:
            print("Maximum runtime should be between 1-24 hours")
            return
        self.max_runtime_hours = hours
        print(f"Maximum runtime set to {hours} hours")

def print_advanced_help():
    """Print help for advanced version"""
    help_text = """
Advanced Windows Mouse Jiggler - Commands:

Basic Commands:
start          - Start the mouse jiggler
stop           - Stop the mouse jiggler
status         - Show detailed status
quit/exit      - Exit and save config

Configuration:
interval X     - Set interval to X seconds (5-300)
distance X     - Set movement distance to X pixels (1-10)
stealth on/off - Enable/disable stealth mode (smaller movements)
maxtime X      - Set maximum runtime to X hours (1-24)
logging on/off - Enable/disable activity logging

Advanced:
save           - Save current configuration
load           - Reload configuration from file
log            - Show recent activity log
clear          - Clear activity log

Security Features:
- Auto-stop after maximum runtime
- Activity logging for audit trails
- Stealth mode for minimal visibility
- Configuration persistence
- Emergency stop (move mouse to top-left corner)

Examples:
> stealth on     # Enable stealth mode
> maxtime 4      # Auto-stop after 4 hours
> interval 45    # Jiggle every 45 seconds
> start          # Begin with security logging
"""
    print(help_text)

def show_activity_log(log_file, lines=10):
    """Show recent activity log entries"""
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                all_lines = f.readlines()
                recent_lines = all_lines[-lines:]
                print(f"\nRecent activity (last {len(recent_lines)} entries):")
                print("-" * 50)
                for line in recent_lines:
                    print(line.strip())
        else:
            print("No activity log found")
    except Exception as e:
        print(f"Error reading log: {e}")

def main():
    jiggler = AdvancedMouseJiggler()
    
    print("=" * 70)
    print("Advanced Windows Mouse Jiggler - Security Compliant Version")
    print("=" * 70)
    print("Enterprise-ready mouse jiggler with security features:")
    print("• Activity logging for audit trails")
    print("• Auto-stop after maximum runtime")
    print("• Stealth mode for minimal visibility")
    print("• Configuration persistence")
    print("• Emergency failsafe (mouse to top-left corner)")
    print()
    print("Type 'help' for commands or 'start' to begin.")
    print("=" * 70)
    
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
                    print_advanced_help()
                elif command in ["quit", "exit"]:
                    if jiggler.running:
                        jiggler.stop()
                    jiggler.save_config()
                    print("Configuration saved. Goodbye!")
                    break
                elif command == "save":
                    jiggler.save_config()
                elif command == "load":
                    jiggler.load_config()
                elif command == "log":
                    show_activity_log(jiggler.log_file)
                elif command == "clear":
                    try:
                        open(jiggler.log_file, 'w').close()
                        print("Activity log cleared")
                    except Exception as e:
                        print(f"Error clearing log: {e}")
                elif parts[0] == "interval" and len(parts) == 2:
                    try:
                        seconds = int(parts[1])
                        if 5 <= seconds <= 300:
                            jiggler.interval = seconds
                            print(f"Interval set to {seconds} seconds")
                        else:
                            print("Interval must be between 5-300 seconds")
                    except ValueError:
                        print("Usage: interval <seconds>")
                elif parts[0] == "distance" and len(parts) == 2:
                    try:
                        pixels = int(parts[1])
                        if 1 <= pixels <= 10:
                            jiggler.movement_distance = pixels
                            print(f"Movement distance set to {pixels} pixels")
                        else:
                            print("Distance must be between 1-10 pixels")
                    except ValueError:
                        print("Usage: distance <pixels>")
                elif parts[0] == "stealth" and len(parts) == 2:
                    if parts[1] in ["on", "true", "yes"]:
                        jiggler.set_stealth_mode(True)
                    elif parts[1] in ["off", "false", "no"]:
                        jiggler.set_stealth_mode(False)
                    else:
                        print("Usage: stealth on/off")
                elif parts[0] == "maxtime" and len(parts) == 2:
                    try:
                        hours = int(parts[1])
                        jiggler.set_max_runtime(hours)
                    except ValueError:
                        print("Usage: maxtime <hours>")
                elif parts[0] == "logging" and len(parts) == 2:
                    if parts[1] in ["on", "true", "yes"]:
                        jiggler.activity_logging = True
                        print("Activity logging enabled")
                    elif parts[1] in ["off", "false", "no"]:
                        jiggler.activity_logging = False
                        print("Activity logging disabled")
                    else:
                        print("Usage: logging on/off")
                elif command == "":
                    continue
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n\nReceived Ctrl+C - stopping gracefully...")
                if jiggler.running:
                    jiggler.stop()
                jiggler.save_config()
                break
            except EOFError:
                print("\nExiting...")
                if jiggler.running:
                    jiggler.stop()
                jiggler.save_config()
                break
                
    except Exception as e:
        print(f"Unexpected error: {e}")
        if jiggler.running:
            jiggler.stop()
        jiggler.save_config()

if __name__ == "__main__":
    main()
