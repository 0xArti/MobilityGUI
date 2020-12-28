import json
import PySimpleGUI as sg

from time import sleep

from src.gui import elements
from src import config_loader


def create_config_values():
    config = config_loader.load_from_configuration("gui.json")
    return config_loader.DynamicConfig(**config)


class Popup():
    WINDOW_NAME = "Mobility"
    EXIT_KEY = "Exit"
    IGNORE_KEY = "Ignore"
    DONE_KEY = "Done"
    EXERCISE_KEY = "Exercises"

    def __init__(self):
        self._first_run = True
        self.exercises = None
        self.gui_config = None
        self.layout = None
        self.window = None
        
    def initialize(self):
        self.gui_config = create_config_values()
        self.exercises = []
        self._apply_config()

        self.layout = self._create_layout()
        self.window = sg.Window(
            title=self.WINDOW_NAME,
            layout=self.layout, 
            size=(self.gui_config.WIDTH, self.gui_config.HEIGHT),
            location=(self.gui_config.X, self.gui_config.Y),
            alpha_channel=self.gui_config.alpha, 
            font=(self.gui_config.font, 16),
            no_titlebar=True,
            keep_on_top=True,
            resizable=False
        )
        
    def display(self, exercises):
        if self._first_run:
            self.window.finalize()
        exercises_list = self.window.FindElement(self.EXERCISE_KEY)
        exercises_list.Update(values=exercises)
        if not self._first_run:
            sleep(1)  # Small delay for clear exercise's list update
        self.window.UnHide()
        event, _ = self.window.read()
        self.window.Hide()
        self._first_run = False

        return event == self.DONE_KEY

    def close(self):
        self.window.close()

    def _apply_config(self):
        sg.theme(self.gui_config.theme)

    def _create_layout(self):
        return [
            [
                sg.Text(self.WINDOW_NAME),
                elements.close_button(self.EXIT_KEY)
            ],
            [
                elements.exercise_list(self.EXERCISE_KEY, self.exercises)
            ],
            [
                elements.ignore_button(self.IGNORE_KEY, font=(self.gui_config.font, 14)),
                elements.done_button(self.DONE_KEY)
            ]
        ]
