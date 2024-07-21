#This code continuously monitors for new USB devices and automatically transfers photos taken within the last day 
#from the detected devices to a specified destination folder. It extracts the date taken from the photo metadata 
#and copies eligible photos to the destination folder, ensuring new devices are processed as they are connected.
import os
import time
import shutil
import psutil
from datetime import datetime, timedelta
from PIL import Image
from PIL.ExifTags import TAGS

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

# Function to move photos from the source folder to the destination folder
def move_photos(source_folder, destination_folder, days_before=1):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                date_taken = get_date_taken(file_path)
                if date_taken >= datetime.now() - timedelta(days=days_before):
                    shutil.copy(file_path, destination_folder)
                    print(f'Moved {file_path} to {destination_folder}')

# Monitor for new drives and move photos(It will continuously moniter new drives until you exit the program)
def monitor_usb(destination_folder):
    existing_partitions = psutil.disk_partitions()
    existing_mounts = {partition.device for partition in existing_partitions}
    
    while True:
        time.sleep(3)  # Check every 3 seconds
        current_partitions = psutil.disk_partitions()
        current_mounts = {partition.device for partition in current_partitions}
        
        new_mounts = current_mounts - existing_mounts
        if new_mounts:
            for mount in new_mounts:
                mount_path = next((p.mountpoint for p in current_partitions if p.device == mount), None)
                if mount_path:
                    print(f'Device mounted at {mount_path}')
                    move_photos(mount_path, destination_folder)
                    print(f'All photos moved to {destination_folder}')
        existing_mounts = current_mounts

if __name__ == "__main__":
    print("Monitoring for USB devices...")
    monitor_usb(DESTINATION_FOLDER)
