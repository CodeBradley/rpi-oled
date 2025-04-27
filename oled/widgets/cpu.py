"""
CPUWidget: Displays CPU usage percentage.
"""
import psutil
from .base import BaseWidget

class CPUWidget(BaseWidget):
    """
    Widget to display CPU usage.
    """
    def __init__(self):
        self.usage = 0

    def update(self):
        self.usage = psutil.cpu_percent(interval=None)

    def render(self, draw, y, width):
        text = f"CPU {int(self.usage)}%"
        draw.text((0, y), text, fill=255)
        return y + 12
