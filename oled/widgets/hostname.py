"""
HostnameWidget: Displays hostname in bold, uppercase format.
"""
import socket
from .base import TextWidget

class HostnameWidget(TextWidget):
    """
    Widget to display the hostname in bold and uppercase.
    """
    def __init__(self):
        # Initialize with hostname in uppercase, bold font
        super().__init__(
            text=socket.gethostname(),
            font_size=10,
            case_mode=TextWidget.CASE_UPPER,
            bold=True
        )

    def update(self):
        # Get the current hostname in case it changed
        self.text = socket.gethostname()
