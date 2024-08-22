# WPILOG to CSV and MF4 Converter

This repository contains a Python script to parse WPILOG files, convert them to CSV format, and then convert the CSV files to MF4 format using the `asammdf` library. This tool is useful for handling data logs from WPILOG files and converting them into more accessible formats for analysis.

## Features

- **Parse WPILOG Files**: Extract entries and records from WPILOG files.
- **Convert to CSV**: Transform parsed WPILOG data into CSV format.
- **Convert to MF4**: Convert CSV data into MF4 format using `asammdf`.
- **Dynamic Enum Creation**: Automatically create enums for string values in the CSV data.

## Requirements

- Python 3.x
- `asammdf` library
- `enum34` (for Python versions < 3.4)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/wpilog-converter.git
    cd wpilog-converter
    ```

2. Install the required Python packages:
    ```bash
    pip install asammdf enum34
    ```

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
