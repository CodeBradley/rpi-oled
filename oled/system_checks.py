"""
System checks for I2C, OLED, and permissions.
"""
import subprocess
import os

def check_i2c_enabled():
    """
    Checks if I2C is enabled using raspi-config.
    Returns True if enabled, False otherwise.
    """
    try:
        output = subprocess.check_output(['raspi-config', 'nonint', 'get_i2c'])
        return output.strip() == b'0'
    except Exception:
        return False

def check_oled_connected(address=0x3C, bus=1):
    """
    Uses i2cdetect to check if OLED is connected.
    Returns True if found, False otherwise.
    """
    try:
        output = subprocess.check_output(['i2cdetect', '-y', str(bus)]).decode()
        return f"{address:02x}" in output
    except Exception:
        return False

def check_root():
    """
    Checks if running as root (needed for GPIO/I2C).
    """
    return os.geteuid() == 0
