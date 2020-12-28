import win32gui
import win32api
import win32con
import win32process


def is_locked_workstation():
    """
    Note: The service need to run as Administrator for this function to work.
     GetProcess handle will fail to get admin's process if the current process
     is not admin. Thus, returning incorrect result.
    Note: Tested on Win10
    Returns:
        bool: True if Workstation is locked
    """
    try:
        window_handle = win32gui.GetForegroundWindow()
        (_, pid) = win32process.GetWindowThreadProcessId(window_handle)
        process_handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        file_name = win32process.GetModuleFileNameEx(process_handle, 0)
        return "LockApp.exe" in file_name
    except Exception:
        return True
