import sys
import subprocess
import ctypes
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def execute_network_command(command: list[str], title: str):
    print(f"--- {title} ---")
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            shell=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"Standard Error:\n{result.stderr}")
        print(f"[SUCCESS] {title} completed.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to execute {title}.")
        print(f"Return Code: {e.returncode}")
        print(f"Output:\n{e.stdout}")
        print(f"Error Output:\n{e.stderr}\n")
        return False
    except FileNotFoundError:
        print(f"[ERROR] Command '{command[0]}' not found. Ensure you are on Windows.\n")
        return False
def clean_network_state():
    if sys.platform != "win32":
        print("[ERROR] This script is designed for Windows only.")
        sys.exit(1)
    if not is_admin():
        print("[ERROR] Administrator privileges are required. Please re-run as an administrator.")
        sys.exit(1)
    commands = [
        (["ipconfig", "/flushdns"], "Flushing DNS Resolver Cache"),
        (["netsh", "winsock", "reset"], "Resetting Winsock Catalog"),
        (["netsh", "int", "ip", "reset"], "Resetting TCP/IP Stack"),
    ]
    success_count = 0
    for cmd, title in commands:
        if execute_network_command(cmd, title):
            success_count += 1
    print("--- Network Cleaning Summary ---")
    print(f"Successfully executed {success_count} out of {len(commands)} commands.")
    if success_count > 0:
        print("\n[IMPORTANT] A computer restart is recommended to complete all reset operations.")
if __name__ == "__main__":
    clean_network_state()