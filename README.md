# Video Editor

This Python-based Video Editor provides a simple GUI for basic video editing functions using `moviepy` and `Tkinter`.

## Features

- Concatenate Videos: Merge two video clips into one.
- Mute Video: Remove the audio track from a video.
- Trim Video: Cut a segment from a video based on start and end times.

## Usage

1. Run `Videoeditor.py`.
2. Browse and select video files.
3. Choose an operation (Concatenate, Mute, Trim).
4. Save the processed video.

---

# Image Date Segregator

This tool segregates images based on their capture **date and time** using EXIF metadata.

## Features

- Select a source folder and destination folder.
- Choose a date and time range for filtering images.
- Copies selected images to the destination folder.

## Usage

1. Run `img-date-segregator.py`.
2. Browse and select folders.
3. Input the date and time range.
4. Click "Start" to segregate images.

---

# Automatic Photo Transfer from USB

This script monitors USB devices and automatically transfers recent photos based on their metadata.

## Features

- Detects newly inserted USB devices.
- Transfers images taken within the last day.
- Uses `psutil` to monitor new drives.

## Usage

1. Run `auto_photo_transfer.py`.
2. Insert a USB device with images.
3. The script will detect and transfer recent photos to the destination folder automatically.

---
