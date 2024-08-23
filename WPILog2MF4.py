import os
import struct
import csv
import asammdf
from enum import Enum

# Function to parse WPILOG file
def parse_wpilog(wpilog_file):
    entries = {}
    records = []

    with open(wpilog_file, 'rb') as f:
        # Read header
        header = f.read(8)
        if header[:6] != b'WPILOG':
            raise ValueError("Invalid WPILOG file")
        version = struct.unpack('<H', header[6:8])[0]
        extra_header_length = struct.unpack('<I', f.read(4))[0]
        extra_header = f.read(extra_header_length)

        # Read records
        while True:
            record_header = f.read(1)
            if not record_header:
                break
            header_length = record_header[0]
            entry_id_length = (header_length & 0b00000011) + 1
            payload_size_length = ((header_length >> 2) & 0b00000011) + 1
            timestamp_length = ((header_length >> 4) & 0b00000111) + 1

            entry_id = int.from_bytes(f.read(entry_id_length), 'little')
            payload_size = int.from_bytes(f.read(payload_size_length), 'little')
            timestamp = int.from_bytes(f.read(timestamp_length), 'little')

            payload = f.read(payload_size)

            if entry_id == 0:
                control_type = payload[0]
                if control_type == 0:  # Start
                    entry_id = struct.unpack('<I', payload[1:5])[0]
                    name_length = struct.unpack('<I', payload[5:9])[0]
                    name = payload[9:9+name_length].decode('utf-8')
                    type_length = struct.unpack('<I', payload[9+name_length:13+name_length])[0]
                    entry_type = payload[13+name_length:13+name_length+type_length].decode('utf-8')
                    metadata_length = struct.unpack('<I', payload[13+name_length+type_length:17+name_length+type_length])[0]
                    metadata = payload[17+name_length+type_length:17+name_length+type_length+metadata_length].decode('utf-8')
                    entries[entry_id] = {'name': name, 'type': entry_type, 'metadata': metadata}
                elif control_type == 1:  # Finish
                    entry_id = struct.unpack('<I', payload[1:5])[0]
                    if entry_id in entries:
                        del entries[entry_id]
                elif control_type == 2:  # Set Metadata
                    entry_id = struct.unpack('<I', payload[1:5])[0]
                    metadata_length = struct.unpack('<I', payload[5:9])[0]
                    metadata = payload[9:9+metadata_length].decode('utf-8')
                    if entry_id in entries:
                        entries[entry_id]['metadata'] = metadata
            else:
                records.append({'entry_id': entry_id, 'timestamp': timestamp, 'payload': payload})

    return entries, records

# Function to decode payload based on entry type
def decode_payload(entry_type, payload):
    if entry_type == 'int64':
        return struct.unpack('<q', payload)[0]
    elif entry_type == 'float':
        return struct.unpack('<f', payload)[0]
    elif entry_type == 'double':
        return struct.unpack('<d', payload)[0]
    elif entry_type == 'boolean':
        return struct.unpack('<?', payload)[0]
    elif entry_type == 'string':
        return payload.decode('utf-8')
    else:
        return payload

# Function to convert parsed WPILOG to CSV
def wpilog_to_csv(entries, records, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        # Write headers
        headers = ['timestamp'] + [entries[entry_id]['name'] for entry_id in entries if entries[entry_id]['name'] != 'NT:/SmartDashboard/Field/Robot']
        writer.writerow(headers)
        
        # Write data
        for record in records:
            row = [record['timestamp'] / 1_000_000]  # Convert timestamp from microseconds to seconds
            for entry_id in entries:
                if entries[entry_id]['name'] == 'NT:/SmartDashboard/Field/Robot':
                    continue
                if record['entry_id'] == entry_id:
                    entry_type = entries[entry_id]['type']
                    decoded_payload = decode_payload(entry_type, record['payload'])
                    row.append(decoded_payload)
                else:
                    row.append('')
            writer.writerow(row)

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

    # Append signals to MDF with comments for enums
    for key, data in signals_dict.items():
        signal = asammdf.Signal(
            samples=data['samples'],
            timestamps=data['timestamps'],
            name=key
        )
        
        # Add comments for enums
        if key in enums:
            comments = {enum.value: enum.name for enum in enums[key]}
            signal.comment = str(comments)
        
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

        entries, records = parse_wpilog(wpilog_path)
        wpilog_to_csv(entries, records, csv_file)
        csv_to_mf4(csv_file, mf4_file)

if __name__ == "__main__":
    main()
