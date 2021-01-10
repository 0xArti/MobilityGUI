import sys

from src import consts

try:
    import pywintypes
    import win32.lib.win32con as win32con
    import win32.win32gui as win32gui
    import win32.win32api as win32api
    import win32.win32process as win32process
except ImportError:
    pass


def _win_is_locked_workstation():
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


def _win_get_user_idle():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / consts.SECOND


def _unix_is_locked_workstation():
    pass


def _unix_get_user_idle():
    pass


def is_locked_workstation():
    if sys.platform == "win32":
        return _win_is_locked_workstation()
    else:
        return _unix_is_locked_workstation()



def is_user_idle(idle_timeout):
    if sys.platform == "win32":
        idle_time = _win_get_user_idle()
    else:
        idle_time = _unix_get_user_idle()

    return idle_time >= idle_timeout
