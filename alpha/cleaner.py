import os
import sys
import subprocess
import shutil
import winreg
import ctypes
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def run_command(command: list[str]):
    try:
        print(f"Executing: {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        print(f"[SUCCESS] {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}\n{e.stderr}")
    except FileNotFoundError:
        print(f"[ERROR] Command not found: {command[0]}")
def delete_directory(path: str):
    path_obj = Path(path)
    if path_obj.exists():
        print(f"Deleting directory: {path_obj}")
        try:
            shutil.rmtree(path_obj, ignore_errors=True)
            print(f"[SUCCESS] Removed {path_obj}")
        except Exception as e:
            print(f"[ERROR] Failed to remove {path_obj}: {e}")
    else:
        print(f"[INFO] Directory not found, skipping: {path_obj}")
def delete_registry_key_recursive(hive, key_path: str):
    print(f"Attempting to delete registry key: HKEY\\...\\{key_path}")
    try:
        with winreg.OpenKey(hive, str(Path(key_path)), 0, winreg.KEY_ALL_ACCESS) as key:
            sub_keys = []
            try:
                i = 0
                while True:
                    sub_keys.append(winreg.EnumKey(key, i))
                    i += 1
            except OSError:
                pass
            for sub_key in sub_keys:
                delete_registry_key_recursive(hive, str(Path(key_path) / sub_key))
        winreg.DeleteKey(hive, str(Path(key_path)))
        print(f"[SUCCESS] Deleted registry key: HKEY\\...\\{key_path}")
    except FileNotFoundError:
        print(f"[INFO] Registry key not found: HKEY\\...\\{key_path}")
    except Exception as e:
        print(f"[ERROR] Could not delete registry key {key_path}: {e}")
def purge_blizzard_installations():
    if sys.platform != "win32":
        print("[ERROR] This script is designed for Windows only.")
        return
    if not is_admin():
        print("[FATAL] Administrator privileges are required for this operation.")
        sys.exit(1)
    print("### BATTLE.NET & OVERWATCH PURGE SCRIPT ###")
    print("### WARNING: THIS IS A DESTRUCTIVE OPERATION ###\n")
    agent_path = Path(os.environ.get("PROGRAMDATA", "C:/ProgramData")) / "Battle.net/Agent/Blizzard Uninstaller.exe"
    if agent_path.exists():
        print("--- Running Blizzard Uninstallers ---")
        run_command([f'"{agent_path}"', '--product=bna'])
        run_command([f'"{agent_path}"', '--product=pro'])
    else:
        print("[WARNING] Blizzard Uninstaller not found. Proceeding with manual file/registry cleanup.")
    print("\n--- Terminating All Blizzard Processes ---")
    processes = ["Agent.exe", "Battle.net.exe", "Overwatch.exe"]
    for p in processes:
        run_command(["taskkill", "/F", "/IM", p])
    print("\n--- Deleting Known Directories ---")
    home = Path.home()
    dirs_to_delete = [
        home / "Documents/Overwatch",
        home / "AppData/Local/Battle.net",
        home / "AppData/Local/Blizzard Entertainment",
        home / "AppData/Roaming/Battle.net",
        os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)") + "/Battle.net",
        os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)") + "/Overwatch",
        os.environ.get("PROGRAMDATA", "C:/ProgramData") + "/Battle.net",
        os.environ.get("PROGRAMDATA", "C:/ProgramData") + "/Blizzard Entertainment",
    ]
    for d in dirs_to_delete:
        delete_directory(d)
    print("\n--- Deleting Registry Keys ---")
    keys_to_delete_hklm = [
        r"SOFTWARE\WOW6432Node\Blizzard Entertainment",
        r"SOFTWARE\Blizzard Entertainment",
    ]
    keys_to_delete_hkcu = [
        r"Software\Blizzard Entertainment",
    ]
    for key in keys_to_delete_hklm:
        delete_registry_key_recursive(winreg.HKEY_LOCAL_MACHINE, key)
    for key in keys_to_delete_hkcu:
        delete_registry_key_recursive(winreg.HKEY_CURRENT_USER, key)
    print("\n[COMPLETE] Blizzard purge process finished.")
if __name__ == "__main__":
    from pathlib import Path
    purge_blizzard_installations()