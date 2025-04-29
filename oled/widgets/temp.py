"""
TempWidget: Displays CPU temperature with BoxIcon.
"""
from .base import ResourceWidget

def get_cpu_temp():
    """
    Read CPU temperature from thermal zone.
    Returns temperature in Celsius.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0
    except Exception:
        return 0.0

class TempWidget(ResourceWidget):
    """
    Widget to display CPU temperature with a thermometer icon.
    """
    def __init__(self):
        # Thermometer icon from BoxIcons (bxs-thermometer)
        super().__init__(icon_char=chr(0xEEC6))  # Updated to bxs-thermometer hex value
        self.value = 0
        
    def update(self):
        # Get CPU temperature
        self.value = get_cpu_temp()
        
    def render(self, draw, x, y, width, align_right=False):
        """
        Draw temperature with icon and degree symbol instead of percentage.
        
        Args:
            draw: PIL.ImageDraw object
            x: Current x position (horizontal)
            y: Current y position (vertical)
            width: Total display width
            align_right: If True, position from right edge (ignored for ResourceWidget)
            
        Returns:
            tuple: Updated (x, y) position for next widget
        """
        # Draw icon
        draw.text((x, y), self.icon_char, font=self.icon_font, fill=255)
        
        # Calculate icon width
        try:
            icon_width = self.icon_font.getbbox(self.icon_char)[2]
        except AttributeError:
            icon_width = 12  # Fallback width
        
        # Draw temperature with degree symbol
        temp_text = f"{int(self.value)}°"
        draw.text((x + icon_width + 1, y), temp_text, font=self.text_font, fill=255)
        
        # Calculate text width
        try:
            text_width = self.text_font.getbbox(temp_text)[2]
        except AttributeError:
            text_width = len(temp_text) * 6  # Approximate width
            
        # Return new position
        return (x + icon_width + text_width + 5, y)
