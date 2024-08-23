# WPILogsToMF4

This project provides tools to convert `.WPIlog` files, commonly used in FRC robotics logging, to the `.MF4` format. It includes a Python-based GUI to streamline the process of downloading `.WPIlog` files from a robot via SFTP and converting them to `.MF4`.

## Features

- **SFTP Download**: Connect to the robot's file system over SFTP and download `.WPIlog` files.
- **WPIlog to MF4 Conversion**: Convert `.WPIlog` files to the `.MF4` format for easier data analysis and visualization.
- **User-friendly GUI**: A Python GUI to manage file downloads and conversions with a simple interface.

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed along with the following packages:

```bash
    git clone https://github.com/yourusername/wpilog-converter.git
    cd wpilog-converter
```

2. Install the required Python packages:
    ```bash
    pip install asammdf enum34 pandas tkinter paramiko
    ```

## Usage

1. Run the GUI
    ```bash
    python main.py
    ```

2. Enter the Team Number:
- Input the team number, which is used to generate the robot’s IP address.

3. Download Files:
- Click on the "Grab Files" button to download .WPIlog files from the robot.

4. Convert Files:
- After downloading, click on the "Convert Files" button to convert the downloaded .WPIlog files to .MF4.

## Scripts
- 'main.py': The main GUI script that integrates file downloading and conversion.
- 'WPILog2MF4.py': Converts .WPIlog files to the .MF4 format.