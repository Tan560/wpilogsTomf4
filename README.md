# wpilogsTomf4

This project provides tools to convert `.wpilog` files, commonly used in FRC robotics logging, to `.csv` & `.mf4` formats. It includes a Python-based GUI to streamline the process of downloading `.wpilog` files from a robot via SFTP and converting them to `.csv` & `.mf4`.

![Alt text](/GUI.png)

## Features

- **SFTP Download**: Connect to the robot's file system over SFTP and download `.wpilog` files.
- **wpilog to csv Conversion**: Convert `.wpilog` files to the `.csv` format for easier data analysis and visualization.
- **wpilog to mf4 Conversion**: Convert `.wpilog` files to the `.mf4` format for easier data analysis and visualization.
- **User-friendly GUI**: A Python GUI to manage file downloads and conversions with a simple interface.

## Getting Started

### Prerequisites

1. Ensure you have Python 3.x installed along with the following packages:
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
- Click on the "Grab Files" button to download .wpilog files from the robot and save them to the wpilog folder in the root directory

4. Convert Files:
- After downloading, click on the "Convert Files" button to convert the downloaded .wpilog files to .csv and .mf4.

## Scripts
- 'main.py': The main GUI script that integrates file downloading and conversion.
- 'wpilog2mf4.py': Converts .wpilog files to the .csv and .mf4 format.