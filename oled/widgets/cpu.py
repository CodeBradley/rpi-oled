"""
CPUWidget: Displays CPU usage percentage with BoxIcon.
"""
import psutil
from .base import ResourceWidget

class CPUWidget(ResourceWidget):
    """
    Widget to display CPU usage with a CPU icon.
    """
    def __init__(self):
        # CPU icon from BoxIcons (bxs-chip)
        super().__init__(icon_char=chr(0xE9BD))
        self.value = 0

    def update(self):
        # Get CPU usage percentage
        self.value = psutil.cpu_percent(interval=None)
