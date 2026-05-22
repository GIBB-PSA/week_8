import os
import random
import string
from datetime import datetime

FILE_LIST_PATH = "generated_files_list.txt"
LOG_FILE_PATH = "file_activity.log"
NUM_ACTIONS = random.randint(10, 200)
DIFFICULTY = 1


def get_random_string(max_length=4096):
    length = random.randint(0, max_length)
    chars = string.ascii_letters + string.digits + " " * 15 + "\n" * 2
    return ''.join(random.choice(chars) for _ in range(length))


def load_active_files(filepath):
    active_files = []
    if not os.path.exists(filepath):
        return active_files

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                active_files.append(line)
    return active_files


def update_file_list(filepath, active_files):
    with open(filepath, "w", encoding="utf-8") as f:
        for file in active_files:
            f.write(f"{file}\n")


def main():
    active_files = load_active_files(FILE_LIST_PATH)

    if not active_files:
        print(f"Fehler: '{FILE_LIST_PATH}' konnte nicht geladen werden oder ist leer.")
        return
    base_dirs = list(set(os.path.dirname(f) for f in active_files if os.path.dirname(f)))

    run_logs = []

    print(f"Starte {NUM_ACTIONS} zufällige Datei-Aktionen...\n")

    for _ in range(NUM_ACTIONS):
        action = random.choice(['alter', 'create', 'remove'][:DIFFICULTY])
        if action == 'alter' and active_files:
            target_file = random.choice(active_files)
            try:
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(get_random_string())
                run_logs.append(f"[Change]\t\"{target_file}\"")
            except Exception as e:
                print(f"Fehler bei Alter ({target_file}): {e}")
        elif action == 'remove' and active_files:
            target_file = random.choice(active_files)
            try:
                if os.path.exists(target_file):
                    os.remove(target_file)
                active_files.remove(target_file)
                update_file_list(FILE_LIST_PATH, active_files)
                run_logs.append(f"[Remove]\t\"{target_file}\"")
            except Exception as e:
                print(f"Fehler bei Remove ({target_file}): {e}")
        elif action == 'create' and base_dirs:
            extensions = ['.txt', '.log', '.csv', '.yml', '.json', '.bak', '.conf', '.tmp']
            filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + random.choice(extensions)
            target_dir = random.choice(base_dirs)
            new_file = os.path.join(target_dir, filename)
            try:
                os.makedirs(target_dir, exist_ok=True)
                with open(new_file, "w", encoding="utf-8") as f:
                    f.write(get_random_string())
                active_files.append(new_file)
                update_file_list(FILE_LIST_PATH, active_files)
                run_logs.append(f"[Create]\t\"{new_file}\"")

            except Exception as e:
                print(f"Fehler bei Create ({new_file}): {e}")

    if run_logs:
        current_datetime = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(f"\n--- Filesystem mit {NUM_ACTIONS} Actions bearbeitet am: {current_datetime} ---\n")
            f.write('\n'.join([f'{log}' for log in run_logs]))


if __name__ == "__main__":
    main()
