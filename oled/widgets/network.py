"""
IPAddressWidget: Displays the device IP address.
"""
import socket
from .base import TextWidget

class IPAddressWidget(TextWidget):
    """
    Widget to display device IP address in regular font.
    """
    def __init__(self):
        # Initialize with IP address
        super().__init__(
            text=self._get_ip(),
            font_size=10,
            case_mode=TextWidget.CASE_ORIGINAL,
            bold=False
        )

    def _get_ip(self):
        """
        Get the current IP address of the device.
        Returns a fallback of 0.0.0.0 if unavailable.
        """
        try:
            # Use a socket connection to determine the outgoing IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "0.0.0.0"

    def update(self):
        # Refresh the IP address
        self.text = self._get_ip()
