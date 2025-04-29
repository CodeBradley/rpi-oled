#!/usr/bin/env python3
"""
Main script to run the OLED stats service.
"""
import sys
import os
import time
import argparse

# Add parent directory to path for imports to work in systemd context
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  

from oled.display_manager import DisplayManager
from oled.system_checks import check_i2c_enabled, check_oled_connected, check_root_user

# Import all widgets
from oled.widgets.cpu import CPUWidget
from oled.widgets.ram import RAMWidget
from oled.widgets.temp import TempWidget
from oled.widgets.docker import DockerWidget
from oled.widgets.ceph import CephWidget
from oled.widgets.network import IPAddressWidget
from oled.widgets.hostname import HostnameWidget

def main():
    """
    Main entry point - set up display, widgets, and run the update loop.
    """
    parser = argparse.ArgumentParser(description='OLED Stats Display')
    parser.add_argument('--dev', action='store_true', help='Development mode (bypass hardware checks)')
    args = parser.parse_args()
    
    dev_mode = args.dev
    
    # Skip hardware checks in dev mode
    if not dev_mode:
        # Perform system checks
        if not check_root_user():
            print("Error: This script must be run as root.")
            sys.exit(1)

        if not check_i2c_enabled():
            print("Error: I2C is not enabled. Please enable it using 'sudo raspi-config'.")
            sys.exit(1)

        if not check_oled_connected():
            print("Error: OLED display not detected on I2C bus. Check connections.")
            sys.exit(1)
    
    # Initialize display manager with standard 128x32 SSD1306 display
    # using default I2C port 1 and address 0x3C
    display = DisplayManager()
    
    # Add resource widgets for top row (CPU, RAM, Temperature)
    display.add_resource_widget(CPUWidget())
    display.add_resource_widget(RAMWidget())
    display.add_resource_widget(TempWidget())
    
    # Add service widgets for top row (Docker, Ceph)
    display.add_service_widget(DockerWidget())
    display.add_service_widget(CephWidget())
    
    # Add text widgets for bottom row (Hostname, IP)
    display.add_text_widget(HostnameWidget())
    display.add_text_widget(IPAddressWidget())
    
    try:
        print("OLED stats display running. Press Ctrl+C to exit.")
        while True:
            display.update()  # This calls update() on all widgets and renders
            time.sleep(1)     # Update once per second
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
