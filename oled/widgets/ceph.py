"""
CephWidget: Displays Ceph icon if ceph-osd service is running.
"""
import subprocess
from PIL import ImageFont
from .base import BaseWidget
import os

class CephWidget(BaseWidget):
    """
    Widget to display Ceph icon if ceph-osd is running.
    """
    def __init__(self, font_path=None):
        self.font_path = font_path or os.path.join(os.path.dirname(__file__), '../../fonts/lakenet-boxicons.ttf')
        self.icon_font = ImageFont.truetype(self.font_path, 12)
        self.icon_char = chr(0xEF5B)  # custom microceph icon
        self.active = False

    def update(self):
        try:
            subprocess.check_output(['systemctl', 'is-active', '--quiet', 'ceph-osd'])
            self.active = True
        except subprocess.CalledProcessError:
            self.active = False

    def render(self, draw, y, width):
        if self.active:
            draw.text((width - 24, y), self.icon_char, font=self.icon_font, fill=255)
        return y
