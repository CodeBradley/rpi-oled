"""
DisplayManager: Handles OLED initialization, widget layout, and screen refresh.
"""
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

class MockDevice:
    """A mock device for development without actual OLED hardware."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def display(self, image):
        # Just print that we would display rather than actually displaying
        print(f"[MOCK] Display update: {self.width}x{self.height}")

class DisplayManager:
    """
    Manages the OLED display and renders widgets.
    """
    def __init__(self, width=128, height=32, i2c_port=1, i2c_address=0x3C, dev_mode=False):
        self.width = width
        self.height = height
        self.widgets = []
        
        if dev_mode:
            print("Running with mock display device")
            self.device = MockDevice(width, height)
        else:
            try:
                self.serial = i2c(port=i2c_port, address=i2c_address)
                self.device = ssd1306(self.serial, width=width, height=height)
            except Exception as e:
                print(f"Error initializing display: {e}")
                print("Falling back to mock display")
                self.device = MockDevice(width, height)

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
