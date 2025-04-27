"""
HostnameWidget: Displays hostname in bold, large font.
"""
import socket
from PIL import ImageFont
from .base import BaseWidget
import os

class HostnameWidget(BaseWidget):
    """
    Widget to display the hostname in bold.
    """
    def __init__(self):
        self.hostname = socket.gethostname()
        # Helvetica is not available by default; fallback to DejaVuSans-Bold
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)

    def update(self):
        self.hostname = socket.gethostname()

    def render(self, draw, y, width):
        draw.text((0, y), self.hostname, font=self.font, fill=255)
        return y + 14
