"""
DisplayManager: Handles OLED initialization, widget layout, and screen refresh.
"""
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

class DisplayManager:
    """
    Manages the OLED display and renders widgets in a layout matching the mockup.
    """
    def __init__(self, width=128, height=32, i2c_port=1, i2c_address=0x3C):
        """
        Initialize the display manager and connect to the OLED.
        
        Args:
            width: Display width in pixels (default: 128)
            height: Display height in pixels (default: 32)
            i2c_port: I2C bus number (default: 1)
            i2c_address: I2C address of the OLED (default: 0x3C)
        """
        self.width = width
        self.height = height
        
        # Initialize the OLED display using standard luma.oled approach
        self.serial = i2c(port=i2c_port, address=i2c_address)
        # Create the device with 180 degree rotation to fix upside-down display
        self.device = ssd1306(self.serial, width=width, height=height, rotate=2)  # rotate=2 is 180 degrees
        
        # Widget collections by row
        self.top_row_widgets = []    # Resource and service widgets
        self.bottom_row_widgets = [] # Text widgets

    def add_resource_widget(self, widget):
        """Add a resource widget to the top row."""
        self.top_row_widgets.append(("resource", widget))

    def add_service_widget(self, widget):
        """Add a service widget to the top row."""
        self.top_row_widgets.append(("service", widget))

    def add_text_widget(self, widget):
        """Add a text widget to the bottom row."""
        self.bottom_row_widgets.append(widget)

    def render(self):
        """Create and render the complete display layout."""
        # Create a new blank image
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        
        # Define row positions
        top_row_y = 0
        bottom_row_y = 16  # Start halfway down the 32px display
        
        # Render resource widgets from left to right
        x = 0
        for widget_type, widget in self.top_row_widgets:
            if widget_type == "resource":
                x, _ = widget.render(draw, x, top_row_y, self.width)
        
        # Render service widgets from right to left, spaced horizontally
        # Align them to the right side of the display
        service_x = self.width
        service_widgets = [(t, w) for t, w in self.top_row_widgets if t == "service"]
        service_widgets.reverse()  # Process right-to-left
        
        # Calculate proper spacing for service widgets
        service_spacing = 20  # Each icon gets 20px of space
        
        # Start from right edge with proper spacing
        for i, (_, widget) in enumerate(service_widgets):
            # Position from right edge with consistent spacing
            widget_x = self.width - (i + 1) * service_spacing
            widget.render(draw, widget_x, top_row_y, self.width)
        
        # Draw a horizontal divider line with a dashed pattern to simulate 50% opacity
        # Since OLED is monochrome and doesn't support opacity, we use a dashed pattern
        y_divider = 15  # Position between top and bottom rows
        
        # Draw dashed line (alternating pixels on/off to simulate 50% opacity)
        for x_pos in range(0, self.width, 2):  # Every other pixel
            draw.point((x_pos, y_divider), fill=255)
        
        # Render text widgets on bottom row
        x = 0
        for widget in self.bottom_row_widgets:
            x, _ = widget.render(draw, x, bottom_row_y, self.width)
        
        # Show on the display
        self.device.display(image)

    def update(self):
        """Update data for all widgets and redraw the display."""
        # Update all widgets
        for _, widget in self.top_row_widgets:
            widget.update()
            
        for widget in self.bottom_row_widgets:
            widget.update()
            
        # Render the updated widgets
        self.render()
