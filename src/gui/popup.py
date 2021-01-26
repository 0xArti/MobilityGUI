import json
import PySimpleGUI as sg

from time import sleep
from datetime import datetime

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
    EXERCISE_KEY = "Exercises."
    ON_REMOVE_EXERCISE = "onRemove"
    ON_PRESS_DOWN = "onPressDown"
    ON_PRESS_UP = "onPressUp"
    ON_SELECT = "onSelect"

    def __init__(self):   
        self._first_run = True
        self.gui_config = create_config_values()
        self._apply_config()
        self.current_values = []
        self.selection = 0
        self.listbox = None
        self.events = {
            f"{self.EXERCISE_KEY}{self.ON_REMOVE_EXERCISE}": self.onRemoveItem,
            f"{self.EXERCISE_KEY}{self.ON_PRESS_DOWN}": self.onPressDown,
            f"{self.EXERCISE_KEY}{self.ON_PRESS_UP}": self.onPressUp,
           f"{self.EXERCISE_KEY}{self.ON_SELECT}": self.onSelect
        }
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
        
    def initialize(self):
        pass

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
            self._setup_listbox()
            self._first_run = False

        updated = self.current_values != exercises
        if updated:
            self.update(exercises)
        
        if self.window._Hidden and exercises and updated:
            self.window.UnHide()

        return self._read_event(timeout=timeout)

    def _read_event(self, timeout=None):
        first_time_snapshot = datetime.now()
        event, item = self.window.read(timeout=timeout)
        listbox_event = event in self.events
        if listbox_event:
            self.events[event](event, item)
            second_time_snapshot = datetime.now()
            new_timeout = self._calculate_timeout(
                timeout, 
                second_time_snapshot - first_time_snapshot
            )
            self._read_event(timeout=new_timeout)
        elif event != "__TIMEOUT__":
            self.window.Hide()
        
        is_done = event == self.DONE_KEY
        self.current_values = self.get_values()
        if is_done:
            self.current_values = []
            self.update(self.current_values)

        return is_done

    def _calculate_timeout(self, past_timeout, time_delta):
        milliseconds_delta = time_delta.total_seconds() * 1000
        new_timeout = past_timeout - milliseconds_delta
        if new_timeout <= 0:
            new_timeout = 0.01
        return new_timeout

    def close(self):
        self.window.close()

    def update(self, exercises):
        self.listbox.Update(values=exercises)
        self.selection = 0
        self.listbox.Widget.select_clear(self.selection)
        self.listbox.Widget.select_set(self.selection)

    def get_values(self):
        return self.listbox.get_list_values()

    def _apply_config(self):
        sg.theme(self.gui_config.theme)

    def _setup_listbox(self):
        self.listbox = self.window.FindElement(self.EXERCISE_KEY)
        self.listbox.bind("<BackSpace>", self.ON_REMOVE_EXERCISE)
        self.listbox.bind("<Delete>", self.ON_REMOVE_EXERCISE)
        self.listbox.bind("<Down>", self.ON_PRESS_DOWN)
        self.listbox.bind("<Up>", self.ON_PRESS_UP)
        self.listbox.bind("<<ListboxSelect>>", self.ON_SELECT)

    def _create_layout(self):
        return [
            [
                sg.Text(self.WINDOW_NAME),
                elements.close_button(self.EXIT_KEY)
            ],
            [
                elements.exercise_list(self.EXERCISE_KEY, font=(self.gui_config.font, 16))
            ],
            [
                elements.ignore_button(self.IGNORE_KEY, font=(self.gui_config.font, 14)),
                elements.done_button(self.DONE_KEY)
            ]
        ]

    def onRemoveItem(self, event, item):
        if item[self.EXERCISE_KEY] == []:
            return
        exercise = item[self.EXERCISE_KEY][0]
        values = self.get_values()
        values.remove(exercise)
        self.update(values)

    def onPressDown(self, event, item):
        if self.selection < len(self.listbox.Values)-1:
            self.listbox.Widget.select_clear(self.selection)
            self.selection += 1
            self.listbox.Widget.select_set(self.selection)

    def onPressUp(self, event, item):
        if self.selection > 0:
            self.listbox.Widget.select_clear(self.selection)
            self.selection -= 1
            self.listbox.Widget.select_set(self.selection)

    def onSelect(self, event, item):
        self.selection = self.listbox.Widget.curselection()[0]
