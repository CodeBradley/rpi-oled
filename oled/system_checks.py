"""
System checks for I2C, OLED, and permissions.
These are used to verify system requirements before starting the OLED service.
"""
import subprocess
import os
import re

def check_i2c_enabled(bus=1):
    """
    Check if I2C is enabled and the bus is available on the system.
    
    Args:
        bus: The I2C bus number (default 1 for most Raspberry Pi models)
        
    Returns:
        bool: True if I2C is enabled, False otherwise
    """
    try:
        # Check if I2C device exists
        if not os.path.exists(f"/dev/i2c-{bus}"):
            print(f"I2C bus {bus} not available. Check if I2C is enabled.")
            return False
            
        # Check if i2c-dev kernel module is loaded
        lsmod_output = subprocess.check_output(['lsmod'], text=True)
        if 'i2c_dev' not in lsmod_output:
            print("i2c_dev kernel module not loaded")
            return False
            
        return True
    except Exception as e:
        print(f"Error checking I2C configuration: {e}")
        return False

def check_oled_connected(address=0x3C, bus=1):
    """
    Checks if the OLED display is connected and detectable on the I2C bus.
    
    Args:
        address: The I2C address to check (default 0x3C for SSD1306)
        bus: The I2C bus number (default 1 for most Raspberry Pi models)
        
    Returns:
        bool: True if the OLED is detected, False otherwise
    """
    try:
        # Run i2cdetect to find connected devices
        output = subprocess.check_output(['i2cdetect', '-y', str(bus)], text=True)
        
        # Convert hex address to the format shown in i2cdetect (without 0x prefix)
        addr_hex = f"{address:02x}"
        
        # Use regex to find the address in the i2cdetect output
        # i2cdetect gives different output on different systems, this makes detection more robust
        pattern = r'[^-]' + addr_hex + r'[^-]' # Match the address not surrounded by - characters
        if re.search(pattern, output) or addr_hex in output:
            return True
            
        print(f"OLED display not found at address 0x{addr_hex} on bus {bus}")
        return False
    except Exception as e:
        print(f"Error checking for OLED display: {e}")
        return False

def check_root_user():
    """
    Checks if the script is running as root, which is required for
    direct hardware access on the Raspberry Pi.
    
    Returns:
        bool: True if running as root, False otherwise
    """
    if os.geteuid() == 0:
        return True
    print("This script must be run as root for direct hardware access.")
    return False
