"""
CephWidget: Displays Ceph icon if ceph-osd service is running.
"""
import subprocess
from .base import ServiceWidget

class CephWidget(ServiceWidget):
    """
    Widget to display Ceph icon if ceph-osd is running.
    """
    def __init__(self):
        # Custom microceph icon provided in the lakenet-boxicons.ttf font
        super().__init__(icon_char=chr(0xEF5B))
        self.active = False

    def update(self):
        # Check if ceph-osd service is active
        try:
            subprocess.check_output(['systemctl', 'is-active', '--quiet', 'ceph-osd'])
            self.active = True
        except subprocess.CalledProcessError:
            self.active = False
        except FileNotFoundError:
            # Handle systems without systemctl
            try:
                subprocess.check_output(['ceph', 'status'], stderr=subprocess.DEVNULL)
                self.active = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.active = False
