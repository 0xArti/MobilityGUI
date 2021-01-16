import json
import PySimpleGUI as sg

from time import sleep

from src.gui import elements
from src import config_loader


def create_config_values():
    config = config_loader.load_from_configuration("gui.json")
    return config_loader.DynamicConfig(**config)


class Popup:
    WINDOW_NAME = "Mobility"
    EXIT_KEY = "Exit"
    IGNORE_KEY = "Ignore"
    DONE_KEY = "Done"
    EXERCISE_KEY = "Exercises"
    REMOVE_EXERCISE = "Remove"

    def __init__(self):
        self.current_values = None
        self._first_run = True
        self.gui_config = None
        self.exercises_list = None
        self.layout = None
        self.window = None
        
    def initialize(self):
        self.current_values = []
        self.gui_config = create_config_values()
        self.exercises = []
        self._apply_config()

        self.layout = self._create_layout()
        self.window = sg.Window(
            title=self.WINDOW_NAME,
            layout=self.layout, 
            size=(self.gui_config.width, self.gui_config.height),
            location=(self.gui_config.x, self.gui_config.y),
            alpha_channel=self.gui_config.alpha, 
            font=(self.gui_config.font, 16),
            no_titlebar=True,
            keep_on_top=True,
            resizable=False
        )

    def is_hidden(self):
        return self.window._Hidden
        
    def display(self, exercises, timeout=None):
        """
        :param exercises: list of exercises information
        :param timeout: timeout in milliseconds to wait for user input
        :returns: True if user clicked on the "Done" button
        """
        if self._first_run:
            self.window.finalize()
            self.window.Hide()
            exercises_list = self.window.FindElement(self.EXERCISE_KEY)
            exercises_list.bind("<BackSpace>", self.REMOVE_EXERCISE)
            exercises_list.bind("<Delete>", self.REMOVE_EXERCISE)
            self.exercises_list = self.window.FindElement(self.EXERCISE_KEY)
            self._first_run = False

        updated = self.current_values != exercises
        if updated:
            self.update(exercises)
        
        if self.window._Hidden and exercises and updated:
            self.window.UnHide()

        event, item = self.window.read(timeout=timeout)
        if self.REMOVE_EXERCISE in event:
            self._remove_item(item)
        elif event != "__TIMEOUT__":
            self.window.Hide()
        
        is_done = event == self.DONE_KEY
        self.current_values = self.get_values()
        if is_done:
            self.current_values = []
            self.update(self.current_values)

        return is_done

    def close(self):
        self.window.close()

    def update(self, exercises):
        self.exercises_list.Update(values=exercises)

    def get_values(self):
        return self.exercises_list.get_list_values()

    def _apply_config(self):
        sg.theme(self.gui_config.theme)

    def _create_layout(self):
        return [
            [
                sg.Text(self.WINDOW_NAME),
                elements.close_button(self.EXIT_KEY)
            ],
            [
                elements.exercise_list(self.EXERCISE_KEY, self.exercises, font=(self.gui_config.font, 16))
            ],
            [
                elements.ignore_button(self.IGNORE_KEY, font=(self.gui_config.font, 14)),
                elements.done_button(self.DONE_KEY)
            ]
        ]

    def _remove_item(self, item):
        if item[self.EXERCISE_KEY] == []:
            return
        exercise = item[self.EXERCISE_KEY][0]
        values = self.get_values()
        values.remove(exercise)
        self.update(values)
