import hashlib
import os
import shutil

def quarantine_file(path):

    quarantine_folder = "quarantine"

    os.makedirs(quarantine_folder, exist_ok=True)

    shutil.move(
        path,
        os.path.join(quarantine_folder, os.path.basename(path))
    )

def get_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_signatures():

    with open("signatures.txt", "r") as file:
        return set(line.strip() for line in file)


signatures = load_signatures()

folder = "test_files"

for filename in os.listdir(folder):

    path = os.path.join(folder, filename)

    file_hash = get_hash(path)

    if file_hash in signatures:
        print(f"[!] Malware Found: {filename}")
        quarantine_file(path)
        print(f"Moved {filename} to quarantine")
    else:
        print(f"[✓] Safe: {filename}")