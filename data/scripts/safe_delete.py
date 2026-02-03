#!/usr/bin/env python3
import os
import sys
import shutil
from datetime import datetime

def safe_delete(target_path):
    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        sys.exit(1)

    # Get the directory of the file to determine where .bin should go
    target_dir = os.path.dirname(os.path.abspath(target_path))
    bin_dir = os.path.join(target_dir, ".bin")

    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)

    # Prepare new filename with timestamp
    filename = os.path.basename(target_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{timestamp}{ext}"
    dest_path = os.path.join(bin_dir, new_filename)

    try:
        shutil.move(target_path, dest_path)
        print(f"Successfully moved '{filename}' to '{dest_path}'")
    except Exception as e:
        print(f"Error moving file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: safe_delete.py <path_to_file_or_dir>")
        sys.exit(1)
    
    safe_delete(sys.argv[1])
