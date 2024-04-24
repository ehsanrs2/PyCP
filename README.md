
# PyCP

## Overview
PyCP is a command-line utility designed to enhance the file copying process by displaying a dynamic progress bar. This tool helps users monitor the progress of copying large files or directories, providing a more interactive and informative experience compared to traditional copy commands.


## Features
- **Progress Visualization:** Real-time progress bar for ongoing copy operations.
- **Recursive Copying:** Support for copying entire directory structures.
- **Overwrite Control:** Options to overwrite existing files or skip them.
- **Efficiency:** Optimized to handle large files and directories with minimal performance overhead.

## Installation

### Prerequisites
Before installing PyCP, you need to ensure the following dependencies are installed:
- Python 3
- Rich Library
- Gzip (for handling man pages)

You can install these on Ubuntu with:
```bash
sudo apt update
sudo apt install python3 python3-pip gzip
pip3 install rich
```

### Using the Installation Script
To install PyCP, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pycp.git
   cd pycp
   ```

2. Run the installation script with root privileges:
   ```bash
   sudo ./install.sh
   ```

This script will install PyCP to `/usr/local/bin` and its man page to `/usr/local/share/man/man1`, making it accessible from any terminal.

## Usage
To copy files or directories using PyCP, you can use the following commands:

- Copy a single file:
  ```bash
  pycp /path/to/source/file /path/to/destination/file
  ```

- Copy a directory recursively:
  ```bash
  pycp -r /path/to/source/directory /path/to/destination/directory
  ```

- Use the `--no-overwrite` flag to skip overwriting existing files:
  ```bash
  pycp --no-overwrite /path/to/source/file /path/to/destination/file
  ```
- Use the `--overwrite` flag to overwriting all existing files:
  ```bash
  pycp --overwrite /path/to/source/file /path/to/destination/file

## Contributing
Contributions to PyCP are welcome! Please refer to the CONTRIBUTING.md file for guidelines on how to make contributions.

## License
PyCP is released under the MIT License. See the LICENSE file for more details.

## Support
For support, feature requests, or bug reports, please open an issue on the [GitHub issues page](https://github.com/yourusername/pycp/issues).

Thank you for using PyCP!
