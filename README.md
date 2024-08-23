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
pip install pandas tkinter paramiko


## Usage

1. Place your WPILOG files in a folder named `wpilog` in the root directory of the project.

2. Run the script:
    ```bash
    python wpilog_converter.py
    ```

3. The script will create `csv` and `mf4` folders in the root directory and save the converted files there.

## Script Overview

### `parse_wpilog(wpilog_file)`

Parses a WPILOG file and extracts entries and records.

### `decode_payload(entry_type, payload)`

Decodes the payload based on the entry type.

### `wpilog_to_csv(entries, records, csv_file)`

Converts parsed WPILOG data into a CSV file.

### `create_enum(name, values)`

Dynamically creates enums for string values.

### `csv_to_mf4(csv_file, mf4_file)`

Converts CSV data into an MF4 file using the `asammdf` library.

### `main()`

Processes all WPILOG files in the `wpilog` folder, converting them to CSV and MF4 formats if they are not already up-to-date.

## Example

```bash
python wpilog_converter.py
