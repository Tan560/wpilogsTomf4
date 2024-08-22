import paramiko
import os
import time

# SFTP server details
current_path = os.getcwd()
sftp_server = '10.99.97.2'
sftp_user = 'lvuser'
sftp_password = ''
remote_file_path = 'logs/'
wpilog_folder = os.path.join(current_path, 'wpilog')
max_attempts = 3  # Maximum number of connection attempts

# Create local folder if it doesn't exist
os.makedirs(wpilog_folder, exist_ok=True)

# Attempt to connect to the SFTP server with retry logic
attempts = 0
while attempts < max_attempts:
    try:
        print(f"Attempt {attempts + 1} to connect to SFTP server...")
        transport = paramiko.Transport((sftp_server, 22))
        transport.connect(username=sftp_user, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Connected to SFTP server.")
        break  # Exit the loop if connection is successful
    except (paramiko.SSHException, TimeoutError) as e:
        print(f"Connection attempt {attempts + 1} failed: {e}")
        attempts += 1
        time.sleep(5)  # Wait before retrying

if attempts == max_attempts:
    print(f"Failed to connect after {max_attempts} attempts. Exiting.")
else:
    # List files in the remote directory
    remote_files = sftp.listdir(remote_file_path)

    # Download each .WPIlog file if it doesn't already exist locally
    for file in remote_files:
        if file.endswith('.wpilog'):
            local_file_path = os.path.join(wpilog_folder, file)
            if not os.path.exists(local_file_path):
                remote_file = os.path.join(remote_file_path, file)
                sftp.get(remote_file, local_file_path)
                print(f'Downloaded: {file}')
            else:
                print(f'Skipping {file}, already exists.')

    # Close the SFTP connection
    sftp.close()
    transport.close()
    print(f'All new .wpilog files downloaded to {wpilog_folder}')
