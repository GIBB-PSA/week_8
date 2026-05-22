import os
import re


def parse_log_file(filepath):
    if not os.path.exists(filepath):
        print(f"Fehler: Datei '{filepath}' wurde nicht gefunden.")
        return None

    log_data = {}

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("-"):
                try:
                    action, path = line.split('\t')
                    log_data[path] = action
                except Exception as e:
                    pass
    return log_data


def compare_logs(ref_file, student_file):
    ref_data = parse_log_file(ref_file)
    student_data = parse_log_file(student_file)
    if ref_data is None or student_data is None:
        return

    error_count = 0

    for path, expected_action in ref_data.items():
        if path not in student_data:
            print(f"Die Datei '{path}' wurde nicht korrekt getrackt.")
            print(f"\tDurchgeführte Aktion: {expected_action}\n")
            error_count += 1
        else:
            student_action = student_data[path]
            if expected_action != student_action:
                print(f"Falsche Aktion für '{path}'.")
                print(f"\tErwartet: {expected_action}, Gefunden: {student_action}\n")
                error_count += 1

    for path, student_action in student_data.items():
        if path not in ref_data:
            print(f"Die Datei '{path}' wurde fälschlicherweise getrackt.")
            print(f"\tAusgegebene Aktion: {student_action}\n")

    if not error_count:
        print("\n\nAusgezeichnet! Alle Änderungen wurden korrekt getrackt!")
    else:
        print(f"\n\nAuswertung beendet. Es wurde{'' if error_count == 1 else 'n'} {error_count} Fehler gefunden.")


if __name__ == "__main__":
    REFERENCE_LOG = "file_activity.log"
    STUDENT_LOG = "file_activity_tracker.log"
    compare_logs(REFERENCE_LOG, STUDENT_LOG)