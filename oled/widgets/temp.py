"""
TempWidget: Displays CPU temperature with icon.
"""
from PIL import ImageFont
from .base import BaseWidget
import os

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0
    except Exception:
        return 0.0

class TempWidget(BaseWidget):
    """
    Widget to display CPU temperature.
    """
    def __init__(self, font_path=None):
        self.temp = 0.0
        self.font_path = font_path or os.path.join(os.path.dirname(__file__), '../../fonts/lakenet-boxicons.ttf')
        self.icon_font = ImageFont.truetype(self.font_path, 12)
        self.text_font = ImageFont.load_default()
        self.icon_char = chr(0xE9D9)  # boxicons thermometer icon (bxs-thermometer)

    def update(self):
        self.temp = get_cpu_temp()

    def render(self, draw, y, width):
        # Draw thermometer icon
        draw.text((0, y), self.icon_char, font=self.icon_font, fill=255)
        # Draw temperature text
        text = f"{int(self.temp)}°"
        draw.text((18, y), text, font=self.text_font, fill=255)
        return y + 12
