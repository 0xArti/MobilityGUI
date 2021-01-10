import random
from src.mobility.templates.base_template import BaseTemplate


class AdvancedTemplate(BaseTemplate):
    """
    Stage 1:
        Daily * 2
        50% Neck
    Stage 2:
        50% Bonus * 2 OR Daily and Bonus
        33% Neck
        20% Power
        Flexability
    """
    name = "Advanced"

    def _power_exercise(self):
        return self.pop(self.all_exercises.power, chance=5)

    def _flexibility_exercise(self):
        return self.pop(self.all_exercises.flexibility)
    
    def _stage_1(self):
        neck_exercise = self._neck_exercise(chance=2)
        first_exercise = self.pop(self.all_exercises.daily)
        if self.is_empty(self.all_exercises.daily):
            self.refill("daily")
            self.increase_stage()
            second_exercise = self.get(self._exercises_copy.daily)
        else:
            second_exercise = self.pop(self.all_exercises.daily)
        
        return [
            neck_exercise,
            first_exercise,
            second_exercise
        ]

    def _stage_2(self):
        if random.randint(0, 1) == 0:
            first_exercise = self.pop(self.all_exercises.bonus)
            if self.is_empty(self.all_exercises.bonus):
                self.refill("bonus")
                second_exercise = self.get(self._exercises_copy.bonus)
            else:
                second_exercise = self.pop(self.all_exercises.bonus)
        else:
            first_exercise = self.pop(self.all_exercises.daily)
            second_exercise = self.pop(self.all_exercises.bonus)
        return [
            first_exercise,
            second_exercise,
            self._neck_exercise(),
            self._power_exercise(),
            self._flexibility_exercise()
        ]

    def _generate_exercises(self):
        exercises = []
        # Stage 1
        if self.stage == 1:
            exercises.extend(self._stage_1())

            if self.is_empty(self.all_exercises.daily):
                self.refill("daily")
                self.increase_stage()
        # Stage 2
        elif self.stage == 2:
            exercises.extend(self._stage_2())

            if self.is_empty(self.all_exercises.daily):
                self.refill("daily")
            if self.is_empty(self.all_exercises.bonus):
                self.refill("bonus")
            if self.is_empty(self.all_exercises.power):
                self.refill("power")
            if self.is_empty(self.all_exercises.flexibility):
                self.refill("flexibility")
                self.refill("power")
                self.refill("bonus")
                self.refill("daily")
                self.reset_stage()
            
        return exercises
