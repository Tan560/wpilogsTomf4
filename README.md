# wpilogsTomf4

This project provides tools to convert `.wpilog` files, commonly used in FRC robotics logging, to `.csv` & `.mf4` formats. It includes a Python-based GUI to streamline the process of downloading `.wpilog` files from a robot via SFTP and converting them to `.csv` & `.mf4`.

![Alt text](/GUI.png)

## Features

- **SFTP Download**: Connect to the robot's file system over SFTP and download `.wpilog` files.
- **Date Filtering**: Select a date to download only `.wpilog` files modified on or after that date.
- **Cut or Copy Files**: Option to either move or copy the downloaded files to a specified directory.
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
    pip install asammdf enum34 pandas tkinter paramiko tkcalendar
    ```

## Usage

1. **Run the GUI**
    ```bash
    python main.py
    ```

2. **Enter the Team Number**:
   - Input the team number, which is used to generate the robot’s IP address.

3. **Select the Date**:
   - Choose a date from the calendar widget. The program will only download `.wpilog` files modified on or after this date.

4. **Download Files**:
   - Click on the "Grab Files" button to download `.wpilog` files from the robot and save them to the `wpilog` folder in the root directory.

5. **Cut or Copy Files**:
   - Choose between "Cut" or "Copy" to either move or duplicate the downloaded files into another folder.

6. **Convert Files**:
   - After downloading, click on the "Convert Files" button to convert the downloaded `.wpilog` files to `.csv` and `.mf4`.

## Scripts

- **`main.py`**: The main GUI script that integrates file downloading, file handling (cut/copy), and conversion.
- **`wpilog2mf4.py`**: Converts `.wpilog` files to the `.csv` and `.mf4` formats.

## IP Address Format

The robot's IP address is generated based on the team number using the format: `10.XX.YY.2`, where `XX` is the high byte and `YY` is the low byte of the team number.

### Example

For team number `254`, the IP address would be `10.2.54.2`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Thanks to the FRC community and contributors for their tools and inspiration.