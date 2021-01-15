import abc
import copy
import random

from src.callback import Callback


class BaseTemplate(metaclass=abc.ABCMeta):
    def __init__(self, exercises):
        self.stage = 3
        self.event_staged = False
        self.all_exercises = exercises
        self._exercises_copy = copy.deepcopy(self.all_exercises)
        self.IncreaseCallback = Callback

    def _random_choice(self, exercises, chance=1):
        if not exercises:
            return None
        if random.randint(1, chance) == 1:
            return random.choice(exercises)

    def pop(self, exercises, chance=1):
        exercise = self._random_choice(exercises, chance)
        if exercise:
            exercises.remove(exercise)
        return exercise

    def pop_n(self, category, chance=1, amount=1, increase=False, increase_callback=None):
        """
        :param category: category of exercises
        :param chance: chance of getting an exercise
        :param amount: how much exercises to return (if chance is 1)
        :param category: category of the exercise
        :param incrase: should we incrase the stage if finished all exercises
        :param increase_callback: additional functionality to execute when stage increased
        """
        result = []
        exercises = self.all_exercises[category]
        
        for n in range(amount):
            exercise = self.pop(exercises, chance=chance)
            result.append(exercise)
            if self.is_empty(exercises):
                exercises = self.refill(category)
                if increase:
                    self.increase_stage()
                    increase = False
        if self.event_staged and increase_callback:
            increase_callback.trigger()

        return result

    def get(self, exercises, chance=1):
        return self._random_choice(exercises, chance)

    def is_empty(self, exercises):
        return exercises == []

    def refill(self, category):
        self.all_exercises[category] = copy.deepcopy(self._exercises_copy[category])
        return self.all_exercises[category]

    def refill_multiple(self, *categories):
        for category in categories:
            self.refill(category)

    def increase_stage(self):
        self.stage += 1
        self.event_staged = True

    def _neck_exercise(self, chance=3):
        """
        This exercises is common for all the templates
        """
        return self.get(self.all_exercises.neck, chance=chance)

    @staticmethod
    def __flatten_exercises(exercises):
        flatten = []
        for item in exercises:
            if isinstance(item, list):
                for subitem in item:
                    flatten.append(subitem)
            else:
                flatten.append(item)
        
        # remove None
        flatten = [item for item in flatten if item is not None]
        # recursive flatten
        if [x for x in flatten if isinstance(x, list)]:
            flatten = BaseTemplate.__flatten_exercises(flatten)
        
        return flatten

    def _generate_exercises(self):
        """
        Implement logic in stage_x methods
        """
        max_stages = len([stage for stage in dir(self) if "_stage_" in stage])
        current_stage = (self.stage % max_stages) + 1
        stage_method = getattr(self, f"_stage_{current_stage}")
        self.event_staged = False
        return stage_method()
    
    def generate_exercises(self):
        exercises = self._generate_exercises()
        return self.__flatten_exercises(exercises)
