import os
import json
from random import randint

from src import config_loader


class Exercise(config_loader.DynamicConfig):
    def __init__(self, **options):
        super(Exercise, self).__init__(**options)
        self._repetitions = None

    def _random(self):
        """
        Generates random number of repetitions in range
        if not already generated
        """
        if not self._repetitions:
            self._repetitions = randint(int(self.min), int(self.max))
        return self._repetitions

    def _repeat(self):
        """
        For reapeat --> x<Number>
        for seconds --> <number> sec
        """
        if self.measure == "repeat":
            return f"x{self._random()}"
        if self.measure == "hold":
            return f"{self._random()} sec"

    def __str__(self):
        return f"{self.name} {self._repeat()}"


def get_exercise_metadata():
    return config_loader.DynamicConfig(
        **config_loader.load_from_configuration("exercises.json", key="metadata")
    )


def get_exercises():
    return [Exercise(**exercise_data) for exercise_data 
            in config_loader.load_from_configuration("exercises.json", key="exercises")]
