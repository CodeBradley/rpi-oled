#!/bin/bash
#
# OLED Stats Display Installation Script
# This script installs the OLED stats display service for Raspberry Pi
# Must be run as root
#

# Text formatting
BOLD=$(tput bold)
NORMAL=$(tput sgr0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)

# Check if script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "${RED}${BOLD}Error:${NORMAL}${RED} This script must be run as root. Try 'sudo ./install.sh'${NORMAL}"
  exit 1
fi

# Directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
INSTALL_DIR="/opt/rpi-oled"
SERVICE_FILE="/etc/systemd/system/rpi-oled.service"

echo "${BOLD}OLED Stats Display Installation${NORMAL}"
echo "=============================="
echo

# Step 1: Check if I2C is enabled
echo "${BOLD}Step 1:${NORMAL} Checking if I2C is enabled..."
if ! grep -q "^dtparam=i2c_arm=on" /boot/config.txt; then
  echo "${YELLOW}I2C does not appear to be enabled. Enabling it now...${NORMAL}"
  echo "dtparam=i2c_arm=on" >> /boot/config.txt
  echo "${GREEN}I2C has been enabled in /boot/config.txt${NORMAL}"
  REBOOT_REQUIRED=1
else
  echo "${GREEN}I2C is already enabled in /boot/config.txt${NORMAL}"
fi

# Step 2: Check if i2c-dev module is loaded
echo "${BOLD}Step 2:${NORMAL} Checking if i2c-dev module is loaded..."
if ! lsmod | grep -q "i2c_dev"; then
  echo "${YELLOW}i2c_dev module is not loaded. Loading it now...${NORMAL}"
  modprobe i2c-dev
  echo "i2c-dev" >> /etc/modules
  echo "${GREEN}i2c-dev module loaded and added to /etc/modules${NORMAL}"
else
  echo "${GREEN}i2c-dev module is already loaded${NORMAL}"
fi

# Step 3: Install required packages
echo "${BOLD}Step 3:${NORMAL} Installing required packages..."
apt update
apt install -y python3-pip python3-venv i2c-tools

# Step 4: Install the application
echo "${BOLD}Step 4:${NORMAL} Installing OLED stats application to ${INSTALL_DIR}..."
# Remove old installation if it exists
if [ -d "$INSTALL_DIR" ]; then
  rm -rf "$INSTALL_DIR"
fi

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy all files
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR"

# Create Python virtual environment
echo "${BOLD}Step 5:${NORMAL} Setting up Python virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Step 6: Install systemd service
echo "${BOLD}Step 6:${NORMAL} Installing systemd service..."
cp "$INSTALL_DIR/scripts/rpi-oled.service" "$SERVICE_FILE"

# Make scripts executable
chmod +x "$INSTALL_DIR/scripts/run_oled_service.py"

# Enable and start the service
systemctl daemon-reload
systemctl enable rpi-oled.service
systemctl start rpi-oled.service

# Check if service is running
sleep 2
if systemctl is-active --quiet rpi-oled.service; then
  echo "${GREEN}${BOLD}OLED stats service is now installed and running!${NORMAL}"
else
  echo "${YELLOW}${BOLD}OLED stats service installation completed but service is not running.${NORMAL}"
  echo "${YELLOW}Check logs with: journalctl -u rpi-oled.service${NORMAL}"
fi

# Step 7: Test I2C connection
echo "${BOLD}Step 7:${NORMAL} Testing I2C connection..."
echo "Running i2cdetect to check for OLED display at 0x3C..."
i2cdetect -y 1

# Finish
echo
echo "${GREEN}${BOLD}Installation completed!${NORMAL}"
if [ "$REBOOT_REQUIRED" == "1" ]; then
  echo "${YELLOW}${BOLD}NOTE:${NORMAL}${YELLOW} A reboot is recommended to fully enable I2C.${NORMAL}"
  echo "      Run 'sudo reboot' after this script completes."
fi
echo
echo "If your OLED display is properly connected to the I2C bus,"
echo "you should now see stats displaying on it."
echo
echo "To check service status: ${BOLD}systemctl status rpi-oled.service${NORMAL}"
echo "To view service logs:    ${BOLD}journalctl -u rpi-oled.service${NORMAL}"
echo "To run test script:      ${BOLD}cd ${INSTALL_DIR} && sudo python3 direct_test.py${NORMAL}"
echo
