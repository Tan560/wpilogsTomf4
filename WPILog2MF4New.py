import os
import csv
import asammdf
from enum import Enum
from collections import defaultdict
import subprocess

# Function to convert WPIlog to CSV using AdvantageScope's Node.js script
def wpilog_to_csv(wpilog_file, csv_file):
    # Path to the Node.js script
    node_script = r"W:\Fuel Cell\Diagnostic Strat\Tools\WPILogsToMF4\export.js"
    # Command to run the Node.js script
    command = ["node", node_script, wpilog_file, csv_file]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

# Function to dynamically create enums
def create_enum(name, values):
    return Enum(name, {value: i for i, value in enumerate(values)})

# Function to convert CSV to MF4
def csv_to_mf4(csv_file, mf4_file):
    mdf = asammdf.MDF()
    signals_dict = {}
    string_values = {}

    # First pass to collect all unique string values
    with open(csv_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            for key, value in row.items():
                if key != 'timestamp' and value:
                    try:
                        float(value)
                    except ValueError:
                        if key not in string_values:
                            string_values[key] = set()
                        string_values[key].add(value)

    # Create enums for each string column
    enums = {key: create_enum(key, values) for key, values in string_values.items()}

    # Second pass to convert values and collect data
    
    with open(csv_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        print("Converting File: " + csv_file)
        for row in reader:
            timestamp = float(row['timestamp'])
            for key, value in row.items():
                if key != 'timestamp' and value:
                    try:
                        value = float(value)
                    except ValueError:
                        if key in enums:
                            value = enums[key][value].value
                        else:
                            continue  # Skip values that are not in the enum

                    if key not in signals_dict:
                        signals_dict[key] = {'timestamps': [], 'samples': []}

                    signals_dict[key]['timestamps'].append(timestamp)
                    signals_dict[key]['samples'].append(value)

    # Find the maximum timestamp across all signals
    max_timestamp = max(max(data['timestamps']) for data in signals_dict.values())

    # Append signals to MDF with comments for enums
    for key, data in signals_dict.items():
        # Add a second point at the end of the overall timeline
        data['timestamps'].append(max_timestamp)  # Append the final timestamp
        
        # Duplicate the last sample value
        data['samples'].append(data['samples'][-1])  # Append the last sample value
        
        signal = asammdf.Signal(
            samples=data['samples'],
            timestamps=data['timestamps'],
            name=key
        )
        
        # Add comments for enums
        if key in enums:
            comments = "\n".join([f"{enum.value}: {enum.name}" for enum in enums[key]])
            signal.comment = comments
        
        mdf.append(signal)

    # Save the MDF file
    mdf.save(mf4_file)

# Main function to process all WPILOG files in a folder
def main():
    current_path = os.getcwd()
    wpilog_folder = os.path.join(current_path, 'wpilog')
    csv_folder = os.path.join(current_path, 'csv')
    mf4_folder = os.path.join(current_path, 'mf4')

    # Create output directories if they don't exist
    os.makedirs(csv_folder, exist_ok=True)
    os.makedirs(mf4_folder, exist_ok=True)

    wpilog_files = [f for f in os.listdir(wpilog_folder) if f.endswith('.wpilog')]

    if not wpilog_files:
        print("No WPIlog files found in the wpilog folder.")
        return

    for wpilog_file in wpilog_files:
        wpilog_path = os.path.join(wpilog_folder, wpilog_file)
        csv_file = os.path.join(csv_folder, f"{os.path.splitext(wpilog_file)[0]}.csv")
        mf4_file = os.path.join(mf4_folder, f"{os.path.splitext(wpilog_file)[0]}.mf4")

        # Check if the CSV and MF4 files are up-to-date
        if os.path.exists(csv_file) and os.path.exists(mf4_file):
            wpilog_mtime = os.path.getmtime(wpilog_path)
            csv_mtime = os.path.getmtime(csv_file)
            mf4_mtime = os.path.getmtime(mf4_file)
            if csv_mtime > wpilog_mtime and mf4_mtime > wpilog_mtime:
                print(f"Skipping conversion for {wpilog_file} as it is already up-to-date.")
                continue

        # Convert WPIlog to CSV
        wpilog_to_csv(wpilog_path, csv_file)

        # Convert CSV to MF4
        csv_to_mf4(csv_file, mf4_file)

if __name__ == "__main__":
    main()