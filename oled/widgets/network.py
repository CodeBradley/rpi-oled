"""
NetworkWidget: Displays hostname (bold) and IP address.
"""
import socket
from PIL import ImageFont
from .base import BaseWidget
import os

class NetworkWidget(BaseWidget):
    """
    Widget to display hostname and IP address.
    """
    def __init__(self, font_path=None):
        self.hostname = socket.gethostname()
        self.ip = self._get_ip()
        # Helvetica is not available by default; fallback to DejaVuSans
        self.text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
        self.ip_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

    def _get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "0.0.0.0"

    def update(self):
        self.hostname = socket.gethostname()
        self.ip = self._get_ip()

    def render(self, draw, y, width):
        draw.text((0, y), self.hostname, font=self.text_font, fill=255)
        # Use getbbox() instead of getsize() for newer Pillow versions
        hostname_width = self.text_font.getbbox(self.hostname)[2] # width is in the 3rd position of bbox
        draw.text((hostname_width + 10, y), self.ip, font=self.ip_font, fill=255)
        return y + 14
