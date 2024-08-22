from ftplib import FTP

# FTP server details
ftp_server = 'ftp.example.com'
ftp_user = 'your_username'
ftp_password = 'your_password'
remote_file_path = '/path/to/your/file.txt'
local_file_path = 'file.txt'

# Connect to the FTP server
ftp = FTP(ftp_server)
ftp.login(user=ftp_user, passwd=ftp_password)

# Navigate to the directory and retrieve the file
with open(local_file_path, 'wb') as local_file:
    ftp.retrbinary(f'RETR {remote_file_path}', local_file.write)

# Close the connection
ftp.quit()

print(f'File {remote_file_path} downloaded successfully as {local_file_path}')
