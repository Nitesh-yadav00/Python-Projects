import os
import time
import shutil
import psutil
from datetime import datetime, timedelta
from PIL import Image
from PIL.ExifTags import TAGS
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from threading import Thread

# Set the destination folder
DESTINATION_FOLDER = '/Users/capta/Desktop/KJ'

# Function to extract the date taken from the photo
def get_date_taken(path):
    try:
        image = Image.open(path)
        info = image._getexif()
        if info:
            for tag, value in info.items():
                if TAGS.get(tag, tag) == 'DateTimeOriginal':
                    return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        return datetime.fromtimestamp(os.path.getctime(path))
    except Exception as e:
        print(f"Error getting date taken for {path}: {e}")
        return datetime.fromtimestamp(os.path.getctime(path))

def progressbar(total_size):
    # Simulate data transfer
    def simulate_data_transfer(progress, total_size, percentage_label):
        transferred = 0
        chunk_size = total_size // 100  # Divide total size into 100 chunks

        for _ in range(100):
            time.sleep(0.1)  # Simulate time delay for data transfer
            transferred += chunk_size
            progress['value'] += 1
            percentage = progress['value']
            percentage_label.config(text=f"{percentage}%")
            root.update_idletasks()

            print(f"Total data transferred: {transferred} units")
    
    def start_transfer():
        progress['value'] = 0
        Thread(target=simulate_data_transfer, args=(progress, total_size, percentage_label)).start()
                  
    root = tk.Tk()
    root.title("Transfer is in progress")
    
    # Create a frame for the progress bar and percentage label
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Create a progress bar
    progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress.grid(row=0, column=0, padx=10, pady=10)
    
    # Create a percentage label
    percentage_label = ttk.Label(frame, text="0%")
    percentage_label.grid(row=0, column=1, padx=10, pady=10)
    
    start_transfer()
    root.mainloop()

# Function to move photos from the source folder to the destination folder
def move_photos(source_folder, destination_folder, days_before=1):
    count = 0  # Initialize count here to avoid UnboundLocalError
    total_size = 0  # Variable to store total size of files to be transferred

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                date_taken = get_date_taken(file_path)
                if date_taken >= datetime.now() - timedelta(days=days_before):
                    shutil.copy(file_path, destination_folder)
                    print(f'Moved {file_path} to {destination_folder}')
                    total_size += os.path.getsize(file_path)  # Add file size to total size
                    count += 1  # Increment count here

    if count > 0:
        progressbar(total_size)  # Show progress bar only if there are files to transfer
    
    return count

# Monitor for new drives and move photos
def monitor_usb(destination_folder):
    existing_partitions = psutil.disk_partitions()
    existing_mounts = {partition.device for partition in existing_partitions}
    
    while True:
        time.sleep(5)  # Check every 5 seconds
        current_partitions = psutil.disk_partitions()
        current_mounts = {partition.device for partition in current_partitions}
        
        new_mounts = current_mounts - existing_mounts
        if new_mounts:
            for mount in new_mounts:
                mount_path = next((p.mountpoint for p in current_partitions if p.device == mount), None)
                if mount_path:
                    messagebox.showinfo("USB Device Inserted",f"USB Device{mount}")
                    print(f'Device mounted at {mount_path}')
                    move_photos(mount_path, destination_folder)
                    print(f'All photos moved to {destination_folder}')
            return mount_path
        existing_mounts = current_mounts

if __name__ == "__main__":
    print("Monitoring for USB devices...")
    monitor_usb(DESTINATION_FOLDER)
