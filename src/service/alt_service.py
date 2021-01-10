import json
import threading

from time import sleep
from datetime import datetime

from src import consts
from src.config_loader import DynamicConfig, load_from_configuration
from src.service import user_inactive
from src.mobility.exercise_storage import ExerciseStorage
from src.gui.popup import Popup


def run_threaded(func):
    def run(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return run


class MobilityService:
    def __init__(self):
        self.settings = DynamicConfig(
            **load_from_configuration("settings.json")
        )
        self.popup = Popup()
        self.popup.initialize()
        self.exercises = ExerciseStorage()
        self.date = self._get_date()
        self.worker_thread = None
        self.seconds_interval = consts.MINUTE * self.settings.popup_timeout
        self.seconds_counter = 0
        self.updated = False

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
        """
        Service loop
        """
        while True:
            self.process()

    def stop(self):
        self.popup.close()

    @run_threaded
    def worker(self):
        # Don't increase timer when user is away from computer
        if user_inactive.is_locked_workstation():
            return
        if user_inactive.is_user_idle(self.settings.idle_timeout):
            return

        self.seconds_counter += consts.USER_DELAY
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
            timeout=consts.USER_DELAY * consts.SECOND, 
            updated=self.updated
        )
        self.updated = False
        if user_result:
            self.exercises.clear()
            
