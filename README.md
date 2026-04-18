# 🚀 Smart File Organizer

A robust and automated file management system built with Python and the `watchdog` library. This script lives in your system background, monitoring your **Downloads** folder in real-time and organizing incoming files into dedicated system categories.

## 📝 Overview

The **Smart File Organizer** is designed to eliminate manual clutter in your terminal and OS by automatically sorting files based on their extensions. It intelligently handles file collisions and performs routine cleanups of old installers, ensuring your workspace remains organized without any manual intervention.

---

## ✨ Key Features

### 1. 🔍 Real-Time Monitoring (Watchdog)
Using the `watchdog` library, the script observes the system's file events. As soon as a file is fully downloaded, it is detected and processed immediately.

### 2. 📁 Dynamic Path Resolution
The script automatically finds your local system paths (Home, Downloads, Pictures, Documents) using `os.path.expanduser`, making it cross-platform compatible for different users.

### 3. 🖼️ Intelligent Sorting
Files are moved based on their extension into focused directories:
- **Pictures**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp`
- **Documents**: `.pdf`, `.docx`, `.doc`, `.txt`, `.xlsx`, `.pptx`, `.csv`
- **Other**: Browsers' temporary files (like `.crdownload` or `.part`) are ignored until the download is finalized.

### 4. 🧹 Automatic Installer Cleanup
A built-in maintenance routine scans for software installers (`.exe`, `.msi`, `.dmg`, `.pkg`). 
- **Policy**: If an installer is older than **30 days**, the script deletes it automatically to save storage space.
- **Schedule**: Cleanup runs immediately upon script startup and repeats every 24 hours.

### 5. 🛡️ Conflict Resolution
If you download a file that already exists in the destination folder, the script intelligently appends a counter (e.g., `image_1.jpg`, `image_2.jpg`) to prevent data loss or overwriting.

---

## 🛠️ How it Works (Under the Hood)

- **`DownloadHandler`**: A custom event handler that listens for the `on_created` event. It includes a **3-second delay** to ensure the operating system has finished writing the file before the script attempts to move it.
- **`shutil.move`**: Used for reliable cross-partition file movement.
- **`if __name__ == '__main__':`**: The entry point that initializes the observer and keeps the script alive in a continuous loop until interrupted by the user (`Ctrl+C`).

---

## 🚀 How to Use

### 1. Installation
Install the required dependency:
```bash
pip3 install watchdog
```

### 2. Running the Script
Keep it running in your terminal:
```bash
python3 organizer.py
```

### 3. Verification
Once running, try downloading an image or a PDF. Within seconds, you will see a log in the terminal, and the file will disappear from your Downloads folder, appearing instantly in your "Pictures" or "Documents" folder.

---

## 📦 Repository Structure

- **`organizer.py`**: The main logic and engine.
- **`requirements.txt`**: List of dependencies (`watchdog`).
- **`.gitignore`**: Prevents cluttering the repo with Python cache files.

---
*Created with ❤️ for a cleaner digital workspace.*
