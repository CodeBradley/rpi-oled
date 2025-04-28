"""
Main entry point for OLED stats service.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from oled.display_manager import DisplayManager
from oled.widgets.cpu import CPUWidget
from oled.widgets.ram import RAMWidget
from oled.widgets.temp import TempWidget
from oled.widgets.docker import DockerWidget
from oled.widgets.ceph import CephWidget
from oled.widgets.network import NetworkWidget
from oled.widgets.hostname import HostnameWidget
from oled.system_checks import check_i2c_enabled, check_oled_connected, check_root


def main():
    # For development/testing, set this to True to bypass hardware checks
    DEV_MODE = True
    
    if not check_root():
        print("ERROR: Script must be run as root.")
        return
    
    if not check_i2c_enabled():
        print("WARNING: I2C is not enabled. Run 'sudo raspi-config' and enable I2C.")
        if not DEV_MODE:
            return
    
    if not check_oled_connected():
        print("WARNING: OLED display not detected on I2C bus.")
        if not DEV_MODE:
            return
        print("Running in DEV_MODE without OLED display.")
        
    # Try to detect the I2C address
    print("Available I2C devices:")
    try:
        import subprocess
        result = subprocess.run(['i2cdetect', '-y', '1'], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error detecting I2C devices: {e}")


    display = DisplayManager(dev_mode=DEV_MODE)
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
