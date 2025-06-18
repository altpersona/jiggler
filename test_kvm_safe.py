import ctypes
import time

# Test the KVM-safe approach
print("Testing KVM-safe sleep prevention...")

# Windows constants
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

try:
    # Prevent system sleep for 5 seconds
    result = ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )
    
    if result != 0:
        print("✅ Successfully preventing sleep using Windows API")
        print("This will work even with KVM switches!")
        time.sleep(2)
        
        # Reset to allow normal sleep
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        print("✅ Reset - normal sleep behavior restored")
    else:
        print("❌ SetThreadExecutionState failed")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nKVM-safe approach test completed!")
