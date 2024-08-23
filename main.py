import paramiko
import os
import time
import argparse
import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading

# Function to convert team number to IP address
def team_number_to_ip(team_number):
    team_number = int(team_number)
    high_byte = (team_number // 100) % 100
    low_byte = team_number % 100
    return f"10.{high_byte:02d}.{low_byte:02d}.2"

# Function to handle grabbing files
def grab_files():
    terminal_output.delete(1.0, tk.END)
    team_number = entry_team_number.get()
    if not team_number.isdigit() or not (1 <= int(team_number) <= 9999):
        messagebox.showerror("Invalid Input", "Please enter a valid team number between 1 and 9999.")
        return

    sftp_ip = team_number_to_ip(team_number)
    os.environ["SFTP_SERVER_IP"] = sftp_ip

    def run_grab_files():
        try:
            # Attempt to connect to the SFTP server with retry logic
            max_attempts = 3
            attempts = 0
            while attempts < max_attempts:
                try:
                    terminal_output.insert(tk.END, f"Attempt {attempts + 1} to connect to SFTP server...")
                    transport = paramiko.Transport((sftp_ip, 22))
                    transport.connect(username="lvuser", password="")
                    sftp = paramiko.SFTPClient.from_transport(transport)
                    terminal_output.insert(tk.END, "Connected to SFTP server.")
                    break  # Exit the loop if connection is successful
                except (paramiko.SSHException, TimeoutError) as e:
                    attempts += 1
                    time.sleep(5)  # Wait before retrying

            if attempts == max_attempts:
                messagebox.showerror("Error", f"Failed to connect after {max_attempts} attempts. Exiting.")                
                return

            # List files in the remote directory
            remote_files = sftp.listdir("logs/")

            # Download each .wpilog file if it doesn't already exist locally
            wpilog_folder = os.path.join(os.getcwd(), "wpilog")
            os.makedirs(wpilog_folder, exist_ok=True)
            for file in remote_files:
                if file.endswith(".wpilog"):
                    local_file_path = os.path.join(wpilog_folder, file)
                    if not os.path.exists(local_file_path):
                        remote_file = os.path.join("logs/", file)
                        sftp.get(remote_file, local_file_path)
                        terminal_output.insert(tk.END, f"Downloaded: {file}\n")
                    else:
                        terminal_output.insert(tk.END, f"Skipping {file}, already exists.\n")

            # Close the SFTP connection
            sftp.close()
            transport.close()
            terminal_output.insert(tk.END, f"All new .wpilog files downloaded to {wpilog_folder}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to RoboRio")
            terminal_output.delete(1.0, tk.END)


    threading.Thread(target=run_grab_files).start()

# Function to handle converting files
def convert_files():
    terminal_output.delete(1.0, tk.END)

    def run_convert_files():
        # Call the second script
        try:
            process = subprocess.Popen(
                ["python", "WPILog2MF4.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            for line in iter(process.stdout.readline, ''):
                terminal_output.insert(tk.END, line)
                terminal_output.see(tk.END)
            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Success", "Files converted successfully!")
            else:
                messagebox.showerror("Error", f"Failed to convert files:\n{process.stderr.read()}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to convert files:\n{e}")
    
    threading.Thread(target=run_convert_files).start()
    
# Function to update terminal output in real-t
# GUI Setup
root = tk.Tk()
root.title("WPIlog File Manager")
root.geometry("800x400")  # Set window size to 300x400 pixels

# Team Number Input
label_team_number = tk.Label(root, text="Enter Team Number:")
label_team_number.pack(pady=5)

entry_team_number = tk.Entry(root)
entry_team_number.pack(pady=5)

# Grab Files Button
btn_grab_files = tk.Button(root, text="Grab Files", command=grab_files)
btn_grab_files.pack(pady=10)

# Convert Files Button
btn_convert_files = tk.Button(root, text="Convert Files", command=convert_files)
btn_convert_files.pack(pady=10)

# Terminal Output
terminal_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=90)
terminal_output.pack(pady=10)

# Run the GUI
root.mainloop()
#testing main block
