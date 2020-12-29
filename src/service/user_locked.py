import pywintypes
import win32.lib.win32con as win32con
import win32.win32gui as win32gui
import win32.win32api as win32api
import win32.win32process as win32process


def is_locked_workstation():
    """
    Note: In case that the program runs as user, error 5 "Access is denied" could raise
    Returns:
        bool: True if Workstation is locked
    """
    try:
        window_handle = win32gui.GetForegroundWindow()
        (_, pid) = win32process.GetWindowThreadProcessId(window_handle)
        process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        file_name = win32process.GetModuleFileNameEx(process_handle, 0)
        return "LockApp.exe" in file_name
    except pywintypes.error as windows_error:
        if "Access is denied" in windows_error.args[2]:
            return False
    except Exception:
        return False
