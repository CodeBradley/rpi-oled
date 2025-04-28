#!/usr/bin/env python3
"""
Direct test script for SSD1306 OLED display.
This script uses the most direct approach to test the OLED display
without any abstractions or widget system.
"""
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# Try I2C bus 1, address 0x3C first (most common for SSD1306)
try:
    # Create serial interface
    serial = i2c(port=1, address=0x3C)
    
    # Create device 
    device = ssd1306(serial, width=128, height=32)  # 0.91" display is 128x32
    
    print("Connected to SSD1306 OLED display!")
    
    # Draw something simple
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((10, 10), "OLED Test OK", fill="white")
    
    time.sleep(2)
    
    # Show some basic information
    while True:
        with canvas(device) as draw:
            draw.text((0, 0), "HYDROGEN", fill="white")
            draw.text((0, 12), "OLED is working!", fill="white")
        
        time.sleep(2)

except Exception as e:
    print(f"Error: {e}")
    print("\nDebugging information:")
    import subprocess
    try:
        print("\nRunning i2cdetect:")
        subprocess.run(['i2cdetect', '-y', '1'], check=True)
        
        print("\nChecking if i2c-dev is loaded:")
        subprocess.run(['lsmod', '|', 'grep', 'i2c_dev'], shell=True)
        
        print("\nChecking permissions:")
        subprocess.run(['ls', '-la', '/dev/i2c*'])
    except Exception as inner_e:
        print(f"Debug command failed: {inner_e}")
