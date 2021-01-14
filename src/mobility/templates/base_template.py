import abc
import copy
import random


class BaseTemplate(metaclass=abc.ABCMeta):
    def __init__(self, exercises):
        self.stage = 1
        self.all_exercises = exercises
        self._exercises_copy = copy.deepcopy(self.all_exercises)

    def _random_choice(self, exercises, chance=1):
        if random.randint(1, chance) == 1:
            return random.choice(exercises)

    def pop(self, exercises, chance=1):
        exercise = self._random_choice(exercises, chance)
        exercises.remove(exercise)
        return exercise

    def pop_n(self, category, chance=1, amount=None, increase=False, trace=False):
        """
        :param category: category of exercises
        :param chance: chance of getting an exercise
        :param amount: how much exercises to return (if chance is 1)
        :param category: category of the exercise
        :param incrase: should we incrase the stage if finished all exercises
        :param trace: last exercise is from fresh list or current
        """
        result = []
        exercises = self.all_exercises[category]
        
        if not trace:
            exercise = self.get(self._exercises_copy[category], chance=chance)
            result.append(exercise)
            amount -= 1

        for n in range(amount):
            exercise = self.pop(exercises, chance=chance)
            result.append(exercise)
            if self.is_empty(exercises):
                self.refill(category)
                exercises = self.all_exercises[category]
                if increase:
                    self.increase_stage()
                    increase = False

        return result

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

    @abc.abstractmethod
    def _generate_exercises(self):
        """
        Implement logic here
        Note: For multiple types of exercises
              it's best practice to use 'Stages'
        """
        raise NotImplementedError()
    
    def generate_exercises(self):
        exercises = self._generate_exercises()
        return self.__flatten_exercises(exercises)
