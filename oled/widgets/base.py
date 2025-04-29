"""
Base widget classes for OLED display.
"""
from abc import ABC, abstractmethod
import os
from PIL import ImageFont

class BaseWidget(ABC):
    """
    Abstract base class for all widgets.
    """
    def __init__(self):
        """Initialize the widget."""
        pass
        
    @abstractmethod
    def update(self):
        """Update widget data - called before rendering."""
        pass

    @abstractmethod
    def render(self, draw, x, y, width, align_right=False):
        """
        Render the widget to the display.
        
        Args:
            draw: PIL.ImageDraw object
            x: Current x position (horizontal)
            y: Current y position (vertical)
            width: Total display width
            align_right: If True, position from right edge
            
        Returns:
            tuple: New (x, y) position after this widget
        """
        pass

class ResourceWidget(BaseWidget):
    """
    Base class for resource widgets (CPU, RAM, Temp) showing icon + value.
    """
    def __init__(self, icon_char, font_path=None):
        """
        Initialize a resource widget.
        
        Args:
            icon_char: Unicode character for the icon
            font_path: Path to the icon font file
        """
        self.icon_char = icon_char
        self.value = 0
        
        # Load fonts
        self.font_path = font_path or os.path.join(os.path.dirname(__file__), '../../fonts/lakenet-boxicons.ttf')
        self.icon_font = ImageFont.truetype(self.font_path, 12)
        self.text_font = ImageFont.load_default()
    
    @abstractmethod
    def update(self):
        """Update resource value."""
        pass
        
    def render(self, draw, x, y, width, align_right=False):
        """
        Draw icon and value side by side.
        
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
        
        # Calculate icon width - approximate if getbbox() isn't available
        try:
            icon_width = self.icon_font.getbbox(self.icon_char)[2]
        except AttributeError:
            icon_width = 12  # Fallback width if using older PIL
        
        # Draw value right after icon
        value_text = f"{int(self.value)}%"
        draw.text((x + icon_width + 1, y), value_text, font=self.text_font, fill=255)
        
        # Calculate total width
        try:
            value_width = self.text_font.getbbox(value_text)[2]
        except AttributeError:
            value_width = len(value_text) * 6  # Approximate width
            
        # Return new x position (advanced horizontally)
        return (x + icon_width + value_width + 5, y)

class ServiceWidget(BaseWidget):
    """
    Base class for service widgets (Docker, Ceph) showing icon if active.
    """
    def __init__(self, icon_char, font_path=None):
        """
        Initialize a service widget.
        
        Args:
            icon_char: Unicode character for the icon
            font_path: Path to the icon font file
        """
        self.icon_char = icon_char
        self.active = False
        
        # Load font
        self.font_path = font_path or os.path.join(os.path.dirname(__file__), '../../fonts/lakenet-boxicons.ttf')
        self.icon_font = ImageFont.truetype(self.font_path, 12)
    
    @abstractmethod
    def update(self):
        """Update service status."""
        pass
        
    def render(self, draw, x, y, width, align_right=False):
        """
        Draw icon if service is active.
        
        Args:
            draw: PIL.ImageDraw object
            x: Current x position (horizontal)
            y: Current y position (vertical)
            width: Total display width
            align_right: If True, position the icon from the right edge
            
        Returns:
            tuple: Updated (x, y) position for next widget
        """
        # Calculate icon width
        try:
            icon_width = self.icon_font.getbbox(self.icon_char)[2] if self.active else 0
        except AttributeError:
            icon_width = 12 if self.active else 0
            
        # Determine position based on alignment
        if align_right:
            # Position from right edge
            icon_x = x - icon_width - 4  # 4px margin
            if self.active:
                draw.text((icon_x, y), self.icon_char, font=self.icon_font, fill=255)
            return (icon_x, y)  # Return new x position to the left
        else:
            # Position from left edge
            if self.active:
                draw.text((x, y), self.icon_char, font=self.icon_font, fill=255)
            return (x + icon_width + 4, y)  # Return new x position to the right

class TextWidget(BaseWidget):
    """
    Base class for text widgets (hostname, IP address).
    """
    CASE_ORIGINAL = 0
    CASE_UPPER = 1
    CASE_LOWER = 2
    CASE_TITLE = 3
    
    def __init__(self, text="", font_path=None, font_size=10, case_mode=CASE_ORIGINAL, bold=False):
        """
        Initialize a text widget.
        
        Args:
            text: Initial text content
            font_path: Path to the font file
            font_size: Font size in pixels
            case_mode: Text case transformation mode
            bold: Whether to use bold font
        """
        self.text = text
        self.case_mode = case_mode
        
        # Use system DejaVu Sans font with fallback to default
        try:
            font_suffix = "-Bold.ttf" if bold else ".ttf"
            self.font = ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{font_suffix}", font_size)
        except IOError:
            self.font = ImageFont.load_default()
    
    def _transform_case(self, text):
        """Apply case transformation to text."""
        if self.case_mode == self.CASE_UPPER:
            return text.upper()
        elif self.case_mode == self.CASE_LOWER:
            return text.lower()
        elif self.case_mode == self.CASE_TITLE:
            return text.title()
        return text  # CASE_ORIGINAL
    
    def render(self, draw, x, y, width, align_right=False):
        """
        Draw text at specified position.
        
        Args:
            draw: PIL.ImageDraw object
            x: Current x position (horizontal)
            y: Current y position (vertical)
            width: Total display width
            align_right: If True, position text from right edge
            
        Returns:
            tuple: Updated (x, y) position after text
        """
        transformed_text = self._transform_case(self.text)
        
        # Calculate text width
        try:
            text_width = self.font.getbbox(transformed_text)[2]
        except AttributeError:
            text_width = len(transformed_text) * 6  # Approximate width
        
        # Determine text position based on alignment
        if align_right:
            # Position from right edge, moving leftward
            text_x = x - text_width - 2  # 2px margin
            draw.text((text_x, y), transformed_text, font=self.font, fill=255)
            return (text_x, y)  # Return position to the left
        else:
            # Position from left edge, moving rightward
            draw.text((x, y), transformed_text, font=self.font, fill=255)
            return (x + text_width + 2, y)  # Return position to the right with margin
