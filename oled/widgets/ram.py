"""
RAMWidget: Displays RAM usage percentage with icon.
"""
import psutil
from PIL import ImageFont
from .base import BaseWidget
import os

class RAMWidget(BaseWidget):
    """
    Widget to display RAM usage.
    """
    def __init__(self, font_path=None):
        self.usage = 0
        self.font_path = font_path or os.path.join(os.path.dirname(__file__), '../../fonts/lakenet-boxicons.ttf')
        self.icon_font = ImageFont.truetype(self.font_path, 12)
        self.text_font = ImageFont.load_default()
        self.icon_char = chr(0xE9C8)  # boxicons RAM icon (bxs-memory-card)

    def update(self):
        mem = psutil.virtual_memory()
        self.usage = mem.percent

    def render(self, draw, y, width):
        # Draw RAM icon
        draw.text((0, y), self.icon_char, font=self.icon_font, fill=255)
        # Draw RAM usage text
        text = f"{int(self.usage)}%"
        draw.text((18, y), text, font=self.text_font, fill=255)
        return y + 12
