#!/usr/bin/env python3
"""
Simple test script for SSD1306 OLED display using our widget architecture.
This provides a direct way to test the display and ensure connectivity.
"""
import time
import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

# Import our widgets for testing
from oled.widgets.cpu import CPUWidget
from oled.widgets.ram import RAMWidget
from oled.widgets.temp import TempWidget
from oled.widgets.hostname import HostnameWidget
from oled.widgets.network import IPAddressWidget

# Try direct connection to I2C bus 1, address 0x3C first (common for SSD1306)
try:
    # Create serial interface
    print("Attempting to connect to OLED on /dev/i2c-1, address 0x3C...")
    serial = i2c(port=1, address=0x3C)
    
    # Create the OLED device
    device = ssd1306(serial, width=128, height=32)  # 0.91" display is 128x32
    
    print("✅ Connected to SSD1306 OLED display!")
    
    # Initialize our widgets
    cpu_widget = CPUWidget()
    ram_widget = RAMWidget()
    temp_widget = TempWidget()
    hostname_widget = HostnameWidget()
    ip_widget = IPAddressWidget()
    
    print("Starting display refresh loop. Press Ctrl+C to exit.")
    
    # Refresh loop for widgets
    while True:
        # Create a new image with a black background
        image = Image.new("1", (device.width, device.height))
        draw = ImageDraw.Draw(image)
        
        # Draw a nice border
        draw.rectangle((0, 0, device.width-1, device.height-1), outline=255, fill=0)
        
        # Update all widgets
        cpu_widget.update()
        ram_widget.update()
        temp_widget.update()
        hostname_widget.update()
        ip_widget.update()
        
        # Render - Top row for system stats
        x_pos = 2  # Start with a 2px margin
        y_pos = 1  # Start with a 1px margin
        
        # Render resource widgets on top row
        x_pos, _ = cpu_widget.render(draw, x_pos, y_pos, device.width)
        x_pos, _ = ram_widget.render(draw, x_pos, y_pos, device.width)
        x_pos, _ = temp_widget.render(draw, x_pos, y_pos, device.width)
        
        # Bottom row for hostname and IP
        x_pos = 2  # Reset to left margin
        y_pos = 16  # Start halfway down the display for second row
        
        # Render text widgets
        x_pos, _ = hostname_widget.render(draw, x_pos, y_pos, device.width)
        x_pos, _ = ip_widget.render(draw, x_pos, y_pos, device.width)
        
        # Show the resulting image on the display
        device.display(image)
        
        # Update once per second
        time.sleep(1)

except KeyboardInterrupt:
    print("Test ended by user.")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nDebugging information:")
    import subprocess
    try:
        print("\nRunning i2cdetect to see available devices:")
        subprocess.run(['i2cdetect', '-y', '1'], check=True)
        
        print("\nChecking if i2c-dev kernel module is loaded:")
        subprocess.run(['lsmod', '|', 'grep', 'i2c_dev'], shell=True)
        
        print("\nChecking I2C device permissions:")
        subprocess.run(['ls', '-la', '/dev/i2c*'])
        
        print("\nChecking if user has access to I2C group:")
        subprocess.run(['groups'], shell=True)
    except Exception as inner_e:
        print(f"Debug command failed: {inner_e}")
