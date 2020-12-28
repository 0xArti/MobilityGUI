import random

from src.config_loader import DynamicConfig
from src.mobility.exercises_provider import get_exercises, get_exercise_metadata


class ExerciseCache():
    def __init__(self):
        self._exercise_metadata = None
        self._all_exercises = None
        self.sorted_exercises = DynamicConfig(
            must=None,
            bonus=None,
            advanced=None
        )
        self._current = None
        self._initialize()

    def _initialize(self, renew=True):
        self._exercise_metadata = get_exercise_metadata()
        self._all_exercises = get_exercises()
        for key, value in self.sorted_exercises.items():
            self.sorted_exercises[key] = [exercise for exercise in self._all_exercises 
                                            if exercise.type == key]
        if renew:
            self._current = []

    def _finished_all_exercises(self):
        return self.sorted_exercises.must == [] and self.sorted_exercises.bonus == []

    def _random_exercise(self, exercises):
        return random.choice(exercises)

    def _choose_exercise(self, exercises):
        exercise = self._random_exercise(exercises)
        exercises.remove(exercise)
        return exercise

    def reset(self):
        self._initialize()

    def clear(self):
        self._current = []

    def add(self, exercise):
        self._current.append(exercise)

    def one_exercise(self, by_order):
        if by_order:
            if self.sorted_exercises.must:
                return self._choose_exercise(self.sorted_exercises.must)
            elif self.sorted_exercises.bonus:
                return self._choose_exercise(self.sorted_exercises.bonus)
        else:
            simple_exercises = self.sorted_exercises.must.copy()
            simple_exercises.extend(self.sorted_exercises.bonus)
            return self._random_exercise(simple_exercises)

    def salty_advanced(self):
        if random.random() <= self._exercise_metadata.chance:
            self.add(self._random_exercise(self.sorted_exercises.advanced))

    def generate_exercise(self, by_order=False):
        if self._finished_all_exercises():
            self._initialize(renew=False)

        exercise = self.one_exercise(by_order)
        self.add(exercise)

        if self._exercise_metadata.enabled and self.sorted_exercises.advanced != []:
            self.salty_advanced()

    @property
    def current(self):
        return [str(exercise) for exercise in self._current]
