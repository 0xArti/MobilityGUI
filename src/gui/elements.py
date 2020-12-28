import os
import base64
import PySimpleGUI as sg

from pathlib import Path

from src import config_loader


DISABLE_BORDER_WIDTH = 0


def _read_close_button_image():
    return config_loader.load_from_assets("x-button.png")


def close_button(exit_key):
    return sg.Button(
        button_text="",
        image_data=_read_close_button_image(),
        button_color=(sg.theme_background_color(), sg.theme_background_color()),
        border_width=DISABLE_BORDER_WIDTH,
        pad=((296, 0), (0, 0)),
        key=exit_key
    )


def title(title_name):
    return sg.Text(
        text=title_name
    )


def exercise_list(exercise_key, exercises):
    return sg.Listbox(
        values=exercises,
        size=(30, 5),
        pad=((20, 0), (10, 0)),
        no_scrollbar=True,
        key=exercise_key
    )


def done_button(done_key):
    return sg.Button(
        button_text=done_key,
        button_color=("White", "DarkGreen"),
        highlight_colors=("White", "White"),
        focus=True,
        border_width=DISABLE_BORDER_WIDTH,
        size=(10, 1),
        pad=((173, 0), (15, 0)),
        key=done_key
    )


def ignore_button(ignore_key, font):
    return sg.Button(
        button_text=ignore_key,
        button_color=("Black", "Gold"),
        border_width=DISABLE_BORDER_WIDTH,
        font=font,
        size=(5, 1),
        pad=((22, 0), (15, 0)),
        key=ignore_key
    )
