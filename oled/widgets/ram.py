"""
RAMWidget: Displays RAM usage percentage with BoxIcon.
"""
import psutil
from .base import ResourceWidget

class RAMWidget(ResourceWidget):
    """
    Widget to display RAM usage with a memory icon.
    """
    def __init__(self):
        # Memory card icon from BoxIcons (bxs-memory-card)
        super().__init__(icon_char=chr(0xEB83))  # Updated to bxs-memory-card hex value
        self.value = 0

    def update(self):
        # Get RAM usage percentage
        mem = psutil.virtual_memory()
        self.value = mem.percent
