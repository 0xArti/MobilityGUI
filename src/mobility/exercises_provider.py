import os
import json
from random import randint

from src import config_loader
from src.mobility.exercise_model import Exercise


def _get_all_exercises():
    return [Exercise(**exercise_data) for exercise_data 
            in config_loader.load_from_configuration("exercises.json", key="exercises")]


def get_exercises_types():
    all_exercises = _get_all_exercises()
    types = {}
    for exercise in all_exercises:
        if isinstance(exercise.type, str) and exercise.type not in types:
            types[exercise.type] = None
    return types


def get_exercise_metadata():
    return config_loader.DynamicConfig(
        **config_loader.load_from_configuration("exercises.json", key="metadata")
    )


def get_exercises(equipment_enabled, equipments):
    all_exercises = _get_all_exercises()
    enabled_exercises = [exercise for exercise in all_exercises if exercise.enabled]
    equipped_exercises = [exercise for exercise in enabled_exercises 
                            if exercise._is_equipped(equipment_enabled, equipments)]
    return equipped_exercises
