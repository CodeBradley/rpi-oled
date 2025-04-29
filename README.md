# Raspberry Pi OLED Stats Service

Displays real-time system stats on a 0.91" SSD1306 OLED using luma.oled and RPi.GPIO. Modular, extensible, and documented with Sphinx.

## Features
- Modular widgets (CPU, RAM, Temp, Docker, Network, Hostname)
- Real-time updates
- Hardware/OS checks for I2C and OLED
- Runs as a service or cron job
- Easy to extend and configure

## Deployment
```bash
curl -sSL https://github.com/CodeBradley/rpi-oled/raw/main/install.sh | sudo bash
```

## Setup
- Python 3.7+
- Run as root (for GPIO/I2C access)
- See `requirements.txt`

## Documentation
- Sphinx docs in `docs/`
