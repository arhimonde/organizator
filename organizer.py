import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Detectarea dinamică a folderelor utilizatorului
HOME = os.path.expanduser("~")
DOWNLOADS_PATH = os.path.join(HOME, "Downloads")
PICTURES_PATH = os.path.join(HOME, "Pictures")
DOCUMENTS_PATH = os.path.join(HOME, "Documents")

# Extensiile monitorizate
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"}
DOC_EXT = {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".pages"}
INSTALLER_EXT = {".exe", ".msi", ".dmg", ".pkg"}
TEMP_EXT = {".crdownload", ".part", ".tmp"}

def get_unique_path(path):
    """Gestionează duplicatele adăugând un număr la finalul numelui fișierului."""
    if not os.path.exists(path):
        return path
    
    base, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(f"{base}_{counter}{extension}"):
        counter += 1
    return f"{base}_{counter}{extension}"

def cleanup_old_installers(downloads_path):
    """Scanăm și ștergem instalatoarele mai vechi de 30 de zile."""
    print("🧹 Curățare imediată: Verificăm instalatoarele vechi în folderul Downloads...")
    now = time.time()
    seconds_in_30_days = 30 * 24 * 60 * 60

    for filename in os.listdir(downloads_path):
        file_path = os.path.join(downloads_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in INSTALLER_EXT:
                file_age = os.path.getmtime(file_path)
                if (now - file_age) > seconds_in_30_days:
                    try:
                        os.remove(file_path)
                        print(f"🗑️ Fișier vechi șters: {filename}")
                    except Exception as e:
                        print(f"❌ Eroare la ștergerea {filename}: {e}")

def sort_file(file_path):
    """Verificăm extensia și mutăm fișierul la destinația corespunzătoare."""
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        return

    filename = os.path.basename(file_path)
    if filename.startswith('.'):
        return

    ext = os.path.splitext(filename)[1].lower()
    if ext in TEMP_EXT:
        return

    dest_dir = None
    if ext in IMAGE_EXT:
        dest_dir = PICTURES_PATH
    elif ext in DOC_EXT:
        dest_dir = DOCUMENTS_PATH

    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        final_dest = get_unique_path(os.path.join(dest_dir, filename))
        try:
            shutil.move(file_path, final_dest)
            print(f"📦 Fișier organizat: {filename} -> {os.path.basename(dest_dir)}")
        except Exception as e:
            print(f"❌ Eroare la mutare {filename}: {e}")

class DownloadHandler(FileSystemEventHandler):
    """Handler pentru detectarea descărcărilor noi."""
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = event.src_path
        print(f"🕒 Fișier nou detectat. Așteptăm finalizarea...")
        time.sleep(3) # Așteptare siguranță
        
        if os.path.exists(file_path):
            sort_file(file_path)
        else:
            # În caz că fișierul a fost redenumit de browser după descărcare
            for f in os.listdir(DOWNLOADS_PATH):
                sort_file(os.path.join(DOWNLOADS_PATH, f))

if __name__ == "__main__":
    # 1. Curățare imediată la pornirea scriptului
    cleanup_old_installers(DOWNLOADS_PATH)
    
    # 2. Inițializarea Watchdog
    print(f"🚀 Pornire monitorizare în fundal pentru: {DOWNLOADS_PATH}")
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_PATH, recursive=False)
    
    # 3. Pornirea observatorului
    observer.start()
    
    # 4. Buclă continuă până la oprirea manuală (Ctrl+C)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Oprire Smart File Organizer...")
        observer.stop()
    
    observer.join()
