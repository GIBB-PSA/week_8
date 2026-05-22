import os
import random
import string
from pathlib import Path

ROOT_DIR = Path("./mock_root")
VIRTUAL_DIRS = [
    "etc/systemd/system",
    "var/log/nginx",
    "var/www/html/dvwa",
    "opt/custom_app/bin",
    "usr/local/bin"
]

TOTAL_FILES = 5_000
MAX_DEPTH = 15
EXTENSIONS = [".json", ".log", ".txt", ".conf", ".yml", ".bak", ".csv", ".tmp"]
OUTPUT_FILE = r"generated_files_list.txt"


def generate_payload(size):
    if size == 0:
        return ""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))


def build_random_filesystem():
    tracked_files = []
    folder_count = 16
    for d in VIRTUAL_DIRS:
        (ROOT_DIR / d).mkdir(parents=True, exist_ok=True)

    while len(tracked_files) < TOTAL_FILES:
        current_path = ROOT_DIR / random.choice(VIRTUAL_DIRS)
        for _ in range(MAX_DEPTH):
            if random.random() < 0.4:
                break
            if current_path.exists():
                subdirs = [d for d in current_path.iterdir() if d.is_dir()]
            else:
                subdirs = []
            if subdirs and random.random() < 0.6:
                current_path = random.choice(subdirs)
            else:
                new_dir_name = f"{''.join(random.choices(string.ascii_lowercase, k=8))}"
                current_path = current_path / new_dir_name
                current_path.mkdir(parents=True, exist_ok=True)
                folder_count += 1
        current_path.mkdir(parents=True, exist_ok=True)
        ext = random.choice(EXTENSIONS)
        filename = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}{ext}"
        filepath = current_path / filename
        file_size = random.randint(0, 4096)
        filepath.write_text(generate_payload(file_size), encoding="utf-8")

        tracked_files.append(filepath.absolute().__str__())
        if len(tracked_files) % 250 == 0:
            print(f"\t{len(tracked_files)} / {TOTAL_FILES} Dateien erstellt")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write('\n'.join(tracked_files))
    print(f"Es wurden {folder_count} Ordner und {TOTAL_FILES} Dateien erstellt")


if __name__ == "__main__":
    build_random_filesystem()
