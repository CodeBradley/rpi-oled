"""
Main entry point for OLED stats service.
"""
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
    if not check_root():
        print("ERROR: Script must be run as root.")
        return
    if not check_i2c_enabled():
        print("ERROR: I2C is not enabled. Run 'sudo raspi-config' and enable I2C.")
        return
    if not check_oled_connected():
        print("ERROR: OLED display not detected on I2C bus.")
        return

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
