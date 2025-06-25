import os
import sys
import subprocess
import time
import glob
from pathlib import Path
import ctypes
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def terminate_process(process_name: str):
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", process_name],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"[SUCCESS] Terminated process: {process_name}")
        time.sleep(1)
    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr:
            print(f"[INFO] Process not running: {process_name}")
        else:
            print(f"[ERROR] Failed to terminate {process_name}: {e.stderr}")
def remove_file_or_dir(path: Path):
    if not path.exists():
        print(f"[INFO] Path not found, skipping: {path}")
        return
    try:
        if path.is_file():
            path.unlink()
            print(f"[SUCCESS] Deleted file: {path}")
        elif path.is_dir():
            import shutil
            shutil.rmtree(path)
            print(f"[SUCCESS] Deleted directory: {path}")
    except Exception as e:
        print(f"[ERROR] Could not delete {path}: {e}")
def clear_browser_cookies():
    if sys.platform != "win32":
        print("[ERROR] This script is designed for Windows only.")
        sys.exit(1)
    if not is_admin():
        print("[ERROR] Administrator privileges are required. Please re-run as an administrator.")
        sys.exit(1)
    app_data = Path(os.environ.get("APPDATA", ""))
    local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
    browsers = {
        'Google Chrome': ('chrome.exe', local_app_data / 'Google/Chrome/User Data/Default/Network/Cookies'),
        'Microsoft Edge': ('msedge.exe', local_app_data / 'Microsoft/Edge/User Data/Default/Network/Cookies'),
        'Brave': ('brave.exe', local_app_data / 'BraveSoftware/Brave-Browser/User Data/Default/Network/Cookies'),
        'Opera': ('opera.exe', app_data / 'Opera Software/Opera Stable/Network/Cookies'),
    }
    for name, (process, path) in browsers.items():
        print(f"\n--- Cleaning {name} ---")
        terminate_process(process)
        remove_file_or_dir(path)
    print("\n--- Cleaning Mozilla Firefox ---")
    terminate_process('firefox.exe')
    firefox_profile_path = app_data / 'Mozilla/Firefox/Profiles'
    if firefox_profile_path.exists():
        profile_dirs = glob.glob(str(firefox_profile_path / '*.default*'))
        for profile in profile_dirs:
            cookie_db = Path(profile) / 'cookies.sqlite'
            remove_file_or_dir(cookie_db)
    else:
        print("[INFO] Firefox profile directory not found.")
if __name__ == "__main__":
    clear_browser_cookies()
    print("\n[COMPLETE] Browser cleaning process finished.")