"""
DisplayManager: Handles OLED initialization, widget layout, and screen refresh.
"""
import time
import subprocess
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
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
            # Run i2cdetect to see if the address is detected
            try:
                print(f"Checking for OLED display at address 0x{i2c_address:02X}...")
                result = subprocess.run(['i2cdetect', '-y', str(i2c_port)], 
                                      capture_output=True, text=True)
                print("I2C devices found:")
                print(result.stdout)
                
                # Try several options for connecting
                for attempt in range(3):
                    try:
                        print(f"Connection attempt {attempt+1}...")
                        # Give the I2C bus a moment to settle
                        time.sleep(0.5)
                        
                        # Try with different configuration options
                        if attempt == 0:
                            # Standard approach
                            self.serial = i2c(port=i2c_port, address=i2c_address)
                            self.device = ssd1306(self.serial, width=width, height=height)
                        elif attempt == 1:
                            # Try with I2C device path explicitly
                            self.serial = i2c(port=i2c_port, address=i2c_address, device='/dev/i2c-1')
                            self.device = ssd1306(self.serial, width=width, height=height)
                        elif attempt == 2:
                            # Try with rotate option
                            self.serial = i2c(port=i2c_port, address=i2c_address)
                            self.device = ssd1306(self.serial, width=width, height=height, rotate=0)
                        
                        print("Successfully connected to OLED display!")
                        
                        # Test the display
                        with canvas(self.device) as draw:
                            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                            draw.text((10, 10), "OLED OK", fill="white")
                        time.sleep(1)  # Show the test message briefly
                        
                        break  # Success, exit loop
                    except Exception as e:
                        print(f"Attempt {attempt+1} failed: {e}")
                        if attempt == 2:  # Last attempt
                            raise
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
