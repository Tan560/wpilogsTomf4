import paramiko
import os
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkcalendar import DateEntry
import subprocess
import threading
from datetime import datetime

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
    selected_date = cal.get_date()

    if not team_number.isdigit() or not (1 <= int(team_number) <= 9999):
        messagebox.showerror("Invalid Input", "Please enter a valid team number between 1 and 9999.")
        return

    sftp_ip = team_number_to_ip(team_number)
    os.environ["SFTP_SERVER_IP"] = sftp_ip

    def run_grab_files():
        try:
            max_attempts = 3
            attempts = 0
            while attempts < max_attempts:
                try:
                    terminal_output.insert(tk.END, f"Attempt {attempts + 1} to connect to SFTP server...\n")
                    transport = paramiko.Transport((sftp_ip, 22))
                    transport.connect(username="lvuser", password="")
                    sftp = paramiko.SFTPClient.from_transport(transport)
                    terminal_output.insert(tk.END, "Connected to SFTP server.\n")
                    break
                except (paramiko.SSHException, TimeoutError) as e:
                    attempts += 1
                    time.sleep(5)

            if attempts == max_attempts:
                messagebox.showerror("Error", f"Failed to connect after {max_attempts} attempts. Exiting.")
                return

            remote_files = sftp.listdir("logs/")
            wpilog_folder = os.path.join(os.getcwd(), "wpilog")
            os.makedirs(wpilog_folder, exist_ok=True)

            for file in remote_files:
                if file.endswith(".wpilog"):
                    file_attr = sftp.stat(f"logs/{file}")
                    file_mtime = datetime.fromtimestamp(file_attr.st_mtime)

                    # Download files modified on or after the selected date
                    if file_mtime.date() >= selected_date:
                        local_file_path = os.path.join(wpilog_folder, file)
                        if not os.path.exists(local_file_path):
                            sftp.get(f"logs/{file}", local_file_path)
                            terminal_output.insert(tk.END, f"Downloaded: {file}\n")
                        else:
                            terminal_output.insert(tk.END, f"Skipping {file}, already exists.\n")
                    else:
                        terminal_output.insert(tk.END, f"Skipping {file}, modified before selected date.\n")

            sftp.close()
            transport.close()
            terminal_output.insert(tk.END, f"All relevant .wpilog files downloaded to {wpilog_folder}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to RoboRio")
            terminal_output.delete(1.0, tk.END)

    threading.Thread(target=run_grab_files).start()

# Function to handle converting files
def convert_files():
    terminal_output.delete(1.0, tk.END)

    def run_convert_files():
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

# GUI Setup
root = tk.Tk()
root.title("WPIlog File Manager")
root.geometry("800x450")

# Team Number Input
label_team_number = tk.Label(root, text="Enter Team Number:")
label_team_number.pack(pady=5)

entry_team_number = tk.Entry(root)
entry_team_number.pack(pady=5)

# Date Picker
label_date = tk.Label(root, text="Select Date:")
label_date.pack(pady=5)

cal = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
cal.pack(pady=5)

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
