import hashlib
import os
import json

HASH_FILE = "file_hashes.json"

# Function to calculate the hash of a file
def calculate_hash(file_path, algorithm='sha256'):
    hasher = hashlib.new(algorithm)
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Function to store initial hashes
def store_initial_hashes(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = calculate_hash(file_path)
    with open(HASH_FILE, 'w') as f:
        json.dump(file_hashes, f, indent=4)
    print("Initial file hashes stored.")

# Function to check file integrity
def check_integrity():
    if not os.path.exists(HASH_FILE):
        print("Hash file not found. Run store_initial_hashes() first.")
        return
    
    with open(HASH_FILE, 'r') as f:
        old_hashes = json.load(f)
    
    for file_path, old_hash in old_hashes.items():
        new_hash = calculate_hash(file_path)
        if new_hash is None:
            print(f"WARNING: {file_path} is missing!")
        elif new_hash != old_hash:
            print(f"ALERT: {file_path} has been modified!")
        else:
            print(f"OK: {file_path} is unchanged.")

if __name__ == "__main__":
    directory = input("Enter the directory to monitor: ")
    option = input("Choose an option: (1) Store Initial Hashes (2) Check Integrity: ")
    
    if option == '1':
        store_initial_hashes(directory)
    elif option == '2':
        check_integrity()
    else:
        print("Invalid option.")
