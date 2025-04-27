"""
BaseWidget: Abstract base class for all widgets.
"""
from abc import ABC, abstractmethod

class BaseWidget(ABC):
    """
    Interface for OLED widgets.
    """
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, draw, y, width):
        """
        Draws the widget to the display.
        Args:
            draw: PIL.ImageDraw object
            y: int, vertical offset
            width: int, display width
        Returns:
            int: new y offset after drawing
        """
        pass
