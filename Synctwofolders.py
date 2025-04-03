import os
import shutil
import time
import hashlib
import argparse
from datetime import datetime

# Set up logging 
def write_log(log_file, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)  # Print for visibility
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(log_message + "\n")  # Save to file

# Get a file’s hash to check if it changed
def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):  # Read in small chunks
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Main function to sync two folders
def sync_folders(source_folder, replica_folder, log_file):
    # Make sure the replica folder exists
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)
        write_log(log_file, f"Created replica folder: {replica_folder}")

    # Go through all items in the source folder
    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        replica_path = os.path.join(replica_folder, item)

        # If it's a file and doesn't exist in the replica, or if it's different, copy it
        if os.path.isfile(source_path):
            if not os.path.exists(replica_path) or get_file_hash(source_path) != get_file_hash(replica_path):
                shutil.copy2(source_path, replica_path)
                write_log(log_file, f"Copied/Updated: {source_path} -> {replica_path}")

        # If it's a folder, sync it too 
        elif os.path.isdir(source_path):
            sync_folders(source_path, replica_path, log_file)

    # Check for extra files in the replica that no longer exist in the source
    for item in os.listdir(replica_folder):
        replica_path = os.path.join(replica_folder, item)
        source_path = os.path.join(source_folder, item)

        if not os.path.exists(source_path):  # If it’s not in the source anymore, delete it
            if os.path.isdir(replica_path):
                shutil.rmtree(replica_path)  # Remove folder
                write_log(log_file, f"Deleted folder: {replica_path}")
            else:
                os.remove(replica_path)  # Remove file
                write_log(log_file, f"Deleted file: {replica_path}")

# Handle command-line arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="Synchronize files from two folders.")
    parser.add_argument("source", help="The source folder to synchronize from.")
    parser.add_argument("replica", help="The folder destination to synchronize to")
    parser.add_argument("interval", type=int, help="Time interval between syncs (in seconds)")
    parser.add_argument("log_file", help="Path to the log file")
    return parser.parse_args()

# Run the script in an infinite loop
if __name__ == "__main__":
    args = get_arguments()

    # Make sure the source folder actually exists
    if not os.path.exists(args.source):
        print("Error: The source folder does not exist. Please check the path.")
        exit(1)

    # Keep syncing at the set interval
    while True:
        sync_folders(args.source, args.replica, args.log_file)
        print(f"Sync completed! Next sync in {args.interval} seconds...\n")
        time.sleep(args.interval)
