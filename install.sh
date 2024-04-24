#!/bin/bash

# Define installation directories
BIN_DIR="/usr/local/bin"
MAN_DIR="/usr/local/share/man/man1"

# Check for root privileges
if [[ $(id -u) -ne 0 ]]; then
    echo "Please run as root or use sudo"
    exit 1
fi

# Ensure the script is run from the directory where pycp and pycp.1.gz are located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
echo "Running installation from directory: $SCRIPT_DIR"

# Change to the directory where the script is located
cd "$SCRIPT_DIR"

# Check if the executable file exists
if [ ! -f "pycp" ]; then
    echo "Error: The required file 'pycp' is missing in $SCRIPT_DIR."
    exit 1
fi

# Check if the man page file exists
if [ ! -f "pycp.1.gz" ]; then
    echo "Error: The required man page file 'pycp.1.gz' is missing in $SCRIPT_DIR."
    exit 1
fi

# Copying files to the appropriate directories
echo "Installing pycp to $BIN_DIR"
cp "pycp" "$BIN_DIR"
chmod +x "$BIN_DIR/pycp"

echo "Installing pycp.1.gz to $MAN_DIR"
cp "pycp.1.gz" "$MAN_DIR"

echo "Installation completed successfully!"
