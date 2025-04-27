"""
DisplayManager: Handles OLED initialization, widget layout, and screen refresh.
"""
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

class DisplayManager:
    """
    Manages the OLED display and renders widgets.
    """
    def __init__(self, width=128, height=32, i2c_port=1, i2c_address=0x3C):
        self.width = width
        self.height = height
        self.serial = i2c(port=i2c_port, address=i2c_address)
        self.device = ssd1306(self.serial, width=width, height=height)
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def render(self):
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        y = 0
        for widget in self.widgets:
            y = widget.render(draw, y, self.width)
        self.device.display(image)

    def update(self):
        for widget in self.widgets:
            widget.update()
        self.render()
