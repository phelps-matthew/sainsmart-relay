# SainSmart Relay Control Library

The `sainsmart_relay` library provides an interface and command-line tools to control SainSmart relays via FTDI's bit-bang mode.

## Installation

### Linux Prerequisites

The FTDI USB drivers should be installed by default in most debian distributions. If not, try:
```bash
sudo apt install libftdi1-2
```

In order to access devices as non-root user we need to add the local user to the `dialout` group and add a udev rule:
```bash
sudo usermod -a -G dialout $USER

# logout / reboot

# Add udev rule:
sudo touch /etc/udev/rules.d/99-libftdi.rules
# Add this line:
# SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", GROUP="dialout", MODE="0660"
```

### Python Library

To install the library, ensure 3.8 <= Python <= 3.11.

First, clone the repository:

```bash
git clone https://github.com/yourusername/sainsmart-relay.git
cd sainsmart-relay
```
Then install the library:

```bash
pip install .
```
# Usage
## Relay Server
To start the relay server, run:

```bash
relay-server
```
This will start the server that listens for commands to control the relays.

## Relay Client
To control the relays or query their status, use the relay command.

Change the state of a relay:

```bash
relay 1 on  # Turns relay 1 on
relay 2 off # Turns relay 2 off
```
Get the current status of all relays:

```bash
relay -s  # Displays the status of all relays
```
## Python API
The sainsmart_relay can also be used as a module in Python scripts:

```python
from sainsmart_relay.relay import FTDIBitbangRelay

# Initialize the relay controller with the device ID
relay_controller = FTDIBitbangRelay(device_id='your_device_id')

# Turn relay 1 on
relay_controller.set_relay(1, 'on')

# Retrieve the current relay state
state = relay_controller.get_relay_state()
print(f"Current Relay State: {state:08b}")
```
Replace 'your_device_id' with the actual device ID of your FTDI device.