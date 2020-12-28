import json
import win32serviceutil
import servicemanager
import win32event
import win32service

from time import sleep
from datetime import datetime

from src.service.user_locked import is_locked_workstation
from src.mobility.exercise_cache import ExerciseCache
from src.gui.popup import Popup

MINUTE = 60  # seconds
DELAY = 1


class MobilityService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MobilityService"
    _svc_display_name_ = "Mobility Service"
    _svc_description_ = "Display GUI popup based on interval to remind you that you need to move. \
        and provide an exercise designed for you"
    _DEFAULT_MINUTES_INTERVAL = 20  # Best value 20

    @classmethod
    def parse_command_line(cls):
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.popup = None
        self.exercises = None
        self.date = None
        self.seconds_interval = None
        self.seconds_counter = None

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
        self.seconds_interval = MINUTE * self._DEFAULT_MINUTES_INTERVAL
        self.seconds_counter = 0

    def stop(self):
        self.popup.close()

    def process(self):
        """
        Service logic
        """
        # Don't increase timer when user is away from computer
        if is_locked_workstation():
            return

        self.seconds_counter += DELAY
        # Don't display popup if timeout is not reached yet
        if not self._is_timeout():
            return

        # Clear previous exercises at day change (midnight)
        if self._is_day_changed():
            self.exercises.reset()

        # Display user popup with exercises and get result
        self.exercises.generate_exercise(by_order=True)
        user_result = self.popup.display(self.exercises.current)
        if user_result:
            self.exercises.clear()
        
    def main(self):
        """
        Service loop
        """
        while True:
            self.process()    
            sleep(DELAY)
            