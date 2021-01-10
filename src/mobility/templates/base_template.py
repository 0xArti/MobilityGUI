import abc
import copy
import random


class BaseTemplate(metaclass=abc.ABCMeta):
    def __init__(self, exercises):
        self.stage = 1
        self.all_exercises = exercises
        self._exercises_copy = copy.deepcopy(self.all_exercises)

    def _random_choice(self, exercises, chance=1):
        if random.randint(1, chance):
            return random.choice(exercises)

    def pop(self, exercises, chance=1):
        exercise = self._random_choice(exercises, chance)
        exercises.remove(exercise)
        return exercise

    def get(self, exercises, chance=1):
        return self._random_choice(exercises, chance)

    def is_empty(self, exercises):
        return exercises == []

    def refill(self, category):
        self.all_exercises[category] = copy.deepcopy(self._exercises_copy[category])

    def increase_stage(self):
        self.stage += 1

    def reset_stage(self):
        self.stage = 1

    def _neck_exercise(self, chance=3):
        """
        This exercises is common for all the templates
        """
        return self.get(self.all_exercises.neck, chance=chance)

    @abc.abstractmethod
    def _generate_exercises(self):
        """
        Implement logic here
        Note: For multiple types of exercises
              it's best practice to use 'Stages'
        """
        raise NotImplementedError()
    
    def generate_exercises(self):
        return [exercise for exercise in self._generate_exercises()
                if exercise is not None]
