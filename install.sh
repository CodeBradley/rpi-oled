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

# Installation locations
INSTALL_DIR="/opt/rpi-oled"
SERVICE_FILE="/etc/systemd/system/rpi-oled.service"
REPO_URL="https://github.com/CodeBradley/rpi-oled.git"
TMP_DIR="/tmp/rpi-oled-install"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "${YELLOW}Git is not installed. Installing...${NORMAL}"
    apt update
    apt install -y git
fi

echo "${BOLD}OLED Stats Display Installation${NORMAL}"
echo "=============================="
echo

# Step 0: Clone repository
echo "${BOLD}Step 0:${NORMAL} Preparing installation files..."

# Clean up any old temporary files
if [ -d "$TMP_DIR" ]; then
  rm -rf "$TMP_DIR"
fi

# Clone the repository
echo "Cloning repository from $REPO_URL..."
git clone "$REPO_URL" "$TMP_DIR"

if [ ! -d "$TMP_DIR" ]; then
  echo "${RED}${BOLD}Error:${NORMAL}${RED} Failed to clone repository. Check your internet connection.${NORMAL}"
  exit 1
fi

# Use the cloned repository for all subsequent operations
SOURCE_DIR="$TMP_DIR"

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
apt install -y python3-pip python3-venv python3-dev i2c-tools libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7-dev libtiff5-dev libfontconfig1-dev

# Step 4: Install the application
echo "${BOLD}Step 4:${NORMAL} Installing OLED stats application to ${INSTALL_DIR}..."
# Remove old installation if it exists
if [ -d "$INSTALL_DIR" ]; then
  rm -rf "$INSTALL_DIR"
fi

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy all files
cp -r "$SOURCE_DIR"/* "$INSTALL_DIR"

# Create fonts directory if it doesn't exist
if [ ! -d "$INSTALL_DIR/fonts" ]; then
  echo "${YELLOW}Creating fonts directory...${NORMAL}"
  mkdir -p "$INSTALL_DIR/fonts"
fi

# Check if custom font is available
if [ ! -f "$INSTALL_DIR/fonts/lakenet-boxicons.ttf" ]; then
  echo "${YELLOW}Warning: Custom BoxIcons font not found in fonts directory.${NORMAL}"
  echo "${YELLOW}The application will attempt to use system fonts instead.${NORMAL}"
fi

# Create Python virtual environment
echo "${BOLD}Step 5:${NORMAL} Setting up Python virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip first
python3 -m pip install --upgrade pip setuptools wheel

# Install Python requirements with proper build tools enabled
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
  python3 -m pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
else
  echo "${YELLOW}Warning: requirements.txt not found, installing dependencies manually...${NORMAL}"
  python3 -m pip install luma.oled>=3.8.1 RPi.GPIO>=0.7.0 smbus2>=0.4.1 psutil>=5.8.0 Pillow>=8.4.0 --extra-index-url https://www.piwheels.org/simple
fi

# Step 6: Install systemd service
echo "${BOLD}Step 6:${NORMAL} Installing systemd service..."

# Check if service file exists
if [ -f "$INSTALL_DIR/scripts/rpi-oled.service" ]; then
  cp "$INSTALL_DIR/scripts/rpi-oled.service" "$SERVICE_FILE"
else
  echo "${YELLOW}Service file not found, creating one...${NORMAL}"
  
  # Create the service file directly
  cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Raspberry Pi OLED Stats Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/scripts/run_oled_service.py
Restart=on-failure
RestartSec=5
User=root
# Give the service some time to start
TimeoutStartSec=10
# Make sure this service restarts after system upgrades
Restart=always

[Install]
WantedBy=multi-user.target
EOF
  
  echo "${GREEN}Created systemd service file: $SERVICE_FILE${NORMAL}"
fi

# Make sure the I2C device has proper permissions
echo "${BOLD}Step 6a:${NORMAL} Setting up I2C permissions..."
if grep -q "i2c:" /etc/group; then
  echo "${GREEN}I2C group exists${NORMAL}"
else
  echo "${YELLOW}Creating I2C group...${NORMAL}"
  groupadd i2c
fi

# Add current user to i2c group
if [ -n "$SUDO_USER" ]; then
  echo "Adding user $SUDO_USER to i2c group..."
  usermod -aG i2c "$SUDO_USER"
fi

# Set permissions on I2C device
if [ -e /dev/i2c-1 ]; then
  echo "Setting permissions on /dev/i2c-1..."
  chmod 660 /dev/i2c-1
  chown root:i2c /dev/i2c-1
  
  # Create udev rule for persistent permissions
  echo 'KERNEL=="i2c-[0-9]*", GROUP="i2c", MODE="0660"' > /etc/udev/rules.d/99-i2c.rules
  udevadm control --reload-rules
fi

# Make scripts executable
if [ -f "$INSTALL_DIR/scripts/run_oled_service.py" ]; then
  chmod +x "$INSTALL_DIR/scripts/run_oled_service.py"
else
  echo "${YELLOW}Warning: run_oled_service.py not found in expected location.${NORMAL}"
  
  # Check if the script exists in another location
  run_script=$(find "$INSTALL_DIR" -name "run_oled_service.py" | head -n 1)
  
  if [ -n "$run_script" ]; then
    echo "${GREEN}Found script at: $run_script${NORMAL}"
    chmod +x "$run_script"
    
    # Update service file with correct path
    sed -i "s|ExecStart=.*|ExecStart=$INSTALL_DIR/venv/bin/python3 $run_script|" "$SERVICE_FILE"
  else
    echo "${RED}Error: Could not find run_oled_service.py in the installation directory.${NORMAL}"
    echo "${YELLOW}You may need to manually create this file or check the repository structure.${NORMAL}"
  fi
fi

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

# Clean up temporary files
if [ -d "$TMP_DIR" ]; then
  echo ""
  echo "Cleaning up temporary files..."
  rm -rf "$TMP_DIR"
fi

echo
