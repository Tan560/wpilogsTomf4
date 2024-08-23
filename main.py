import tkinter as tk
from tkinter import messagebox
import subprocess

# Function to convert team number to IP address
def team_number_to_ip(team_number):
    team_number = int(team_number)
    high_byte = (team_number // 100) % 100
    low_byte = team_number % 100
    return f"10.{high_byte:02d}.{low_byte:02d}.2"

# Function to handle grabbing files
def grab_files():
    team_number = entry_team_number.get()
    if not team_number.isdigit() or not (1 <= int(team_number) <= 9999):
        messagebox.showerror("Invalid Input", "Please enter a valid team number between 1 and 9999.")
        return
    
    sftp_ip = team_number_to_ip(team_number)
    
    # Call the first script with the IP address as an argument
    try:
        subprocess.run(["python", "grabFile.py", sftp_ip], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to grab files:\n{e}")

# Function to handle converting files
def convert_files():
    # Call the second script
    try:
        subprocess.run(["python", "WPILog2MF4.py"], check=True)
        messagebox.showinfo("Success", "Files converted successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to convert files:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("WPIlog File Manager")
root.geometry("300x200")  # Set window size to 300x200 pixels

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

# Run the GUI
root.mainloop()
