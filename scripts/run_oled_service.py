"""
Main entry point for OLED stats service.
"""
import sys
import os
import time

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from oled.display_manager import DisplayManager
from oled.widgets.cpu import CPUWidget
from oled.widgets.ram import RAMWidget
from oled.widgets.temp import TempWidget
from oled.widgets.docker import DockerWidget
from oled.widgets.ceph import CephWidget
from oled.widgets.network import NetworkWidget
from oled.widgets.hostname import HostnameWidget


def main():
    # Simple initial check for root
    if os.geteuid() != 0:
        print("ERROR: Script must be run as root for I2C/GPIO access.")
        return
    
    # Initialize display manager with standard parameters
    display = DisplayManager()
    display.add_widget(CPUWidget())
    display.add_widget(RAMWidget())
    display.add_widget(TempWidget())
    display.add_widget(DockerWidget())
    display.add_widget(CephWidget())
    display.add_widget(NetworkWidget())
    display.add_widget(HostnameWidget())

    try:
        while True:
            display.update()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting OLED stats service.")

if __name__ == "__main__":
    main()
