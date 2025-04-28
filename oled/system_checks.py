"""
System checks for I2C, OLED, and permissions.
"""
import subprocess
import os

def is_i2c_available(address=0x3C, bus=1):
    """
    Checks if the I2C device at the specified address is available.
    
    Args:
        address: The I2C address to check (default 0x3C for SSD1306)
        bus: The I2C bus number (default 1 for most Raspberry Pi models)
        
    Returns:
        bool: True if the device is available, False otherwise
    """
    try:
        output = subprocess.check_output(['i2cdetect', '-y', str(bus)]).decode()
        return f"{address:02x}" in output
    except Exception as e:
        print(f"Error checking I2C: {e}")
        return False

def is_root():
    """
    Checks if the script is running as root, which is required for
    direct hardware access on the Raspberry Pi.
    
    Returns:
        bool: True if running as root, False otherwise
    """
    return os.geteuid() == 0
