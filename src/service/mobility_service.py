import json
import threading
import win32serviceutil
import servicemanager
import win32event
import win32service

from time import sleep
from datetime import datetime

from src.service.user_locked import is_locked_workstation
from src.mobility.exercise_cache import ExerciseCache
from src.gui.popup import Popup

MINUTE = 60         # seconds
SECOND = 1000       # milliseconds 
USER_DELAY = 1      # 1000 milliseconds for the UI


def run_threaded(func):
    def run(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return run


class MobilityService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MobilityService"
    _svc_display_name_ = "Mobility Service"
    _svc_description_ = "Display GUI popup based on interval to remind you that you need to move. \
        and provide an exercise designed for you"
    _DEFAULT_MINUTES_INTERVAL = 0.5  # Best value 20

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.popup = None
        self.exercises = None
        self.date = None
        self.worker_thread = None
        self.seconds_interval = None
        self.seconds_counter = None
        self.updated = None

    def SvcStop(self):
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def _get_date(self):
        return datetime.now().strftime("%Y/%m/%d")

    def _is_timeout(self):
        if self.seconds_counter >= self.seconds_interval:
            self.seconds_counter = 0
            return True
        return False

    def _is_day_changed(self):
        current_date = self._get_date()
        if current_date != self.date:
            self.date = current_date
            return True
        return False

    def start(self):
        self.popup = Popup()
        self.popup.initialize()
        self.exercises = ExerciseCache()
        self.date = self._get_date()
        self.worker_thread = None
        self.seconds_interval = MINUTE * self._DEFAULT_MINUTES_INTERVAL
        self.seconds_counter = 0
        self.updated = False

    def stop(self):
        self.popup.close()

    @run_threaded
    def worker(self):
        # Don't increase timer when user is away from computer
        if is_locked_workstation():
            return

        self.seconds_counter += USER_DELAY
        # Don't display popup if timeout is not reached yet
        if not self._is_timeout():
            return

        # Clear previous exercises at day change (midnight)
        if self._is_day_changed():
            self.exercises.reset()

        # Display user popup with exercises and get result
        self.exercises.generate_exercise(by_order=True)
        self.updated = True

    def process(self):
        """
        Service logic
        Note: Calling display() will cause the service to wait for user IO
          if timeout is reached, the function returns
        """
        if not self.worker_thread:
            self.worker_thread = self.worker()
            self.worker_thread.join()
            self.worker_thread = None
        user_result = self.popup.display(
            self.exercises.current, 
            timeout=USER_DELAY * SECOND, 
            updated=self.updated
        )
        self.updated = False
        if user_result:
            self.exercises.clear()
        
    def main(self):
        """
        Service loop
        """
        while True:
            self.process()
            