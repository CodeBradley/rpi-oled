"""
DockerWidget: Displays Docker icon if Docker service is running.
"""
import subprocess
from .base import ServiceWidget

class DockerWidget(ServiceWidget):
    """
    Widget to display Docker icon if Docker is running.
    """
    def __init__(self):
        # Docker icon from BoxIcons (bxl-docker)
        super().__init__(icon_char=chr(0xE928))  # Updated to bxl-docker hex value
        self.active = False

    def update(self):
        # Check if Docker service is active
        try:
            subprocess.check_output(['systemctl', 'is-active', '--quiet', 'docker'])
            self.active = True
        except subprocess.CalledProcessError:
            self.active = False
        except FileNotFoundError:
            # Handle systems without systemctl
            try:
                subprocess.check_output(['docker', 'info'], stderr=subprocess.DEVNULL)
                self.active = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.active = False
