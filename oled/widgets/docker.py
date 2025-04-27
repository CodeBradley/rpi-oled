"""
DockerWidget: Displays Docker icon if docker is running.
"""
import subprocess
from PIL import ImageFont
from .base import BaseWidget
import os

class DockerWidget(BaseWidget):
    """
    Widget to display Docker icon if Docker is running.
    """
    def __init__(self, font_path=None):
        self.font_path = font_path or os.path.join(os.path.dirname(__file__), '../../fonts/lakenet-boxicons.ttf')
        self.icon_font = ImageFont.truetype(self.font_path, 12)
        self.icon_char = chr(0xE91B)  # boxicons Docker icon (bxl-docker)
        self.active = False

    def update(self):
        try:
            subprocess.check_output(['systemctl', 'is-active', '--quiet', 'docker'])
            self.active = True
        except subprocess.CalledProcessError:
            self.active = False

    def render(self, draw, y, width):
        if self.active:
            draw.text((width - 40, y), self.icon_char, font=self.icon_font, fill=255)
        return y
