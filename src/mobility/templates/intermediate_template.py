from src.mobility.templates.base_template import BaseTemplate


class IntermediateTemplate(BaseTemplate):
    """
    Stage 1:
        Daily
        33% Neck
    Stage 2:
        Bonus
        33% Neck
        20% Power
    Stage 3:
        Daily
        Flexability
        25% Neck
    """
    name = "Intermediate"

    def _power_exercise(self):
        return self.pop(self.all_exercises.power, chance=5)

    def _flexibility_exercise(self):
        return self.pop(self.all_exercises.flexibility)
    
    def _stage_1(self):
        return [
            self.pop(self.all_exercises.daily),
            self._neck_exercise()
        ]

    def _stage_2(self):
        return [
            self.pop(self.all_exercises.daily),
            self._neck_exercise(),
            self._power_exercise()
        ]

    def _stage_3(self):
        return [
            self.pop(self.all_exercises.daily),
            self._neck_exercise(chance=4),
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

            if self.is_empty(self.all_exercises.bonus):
                self.refill("bonus")
                self.refill("power")
                self.increase_stage()

            if self.is_empty(self.all_exercises.power):
                self.refill("power")
        # Stage 3
        elif self.stage == 3:
            exercises.extend(self._stage_3())

            if self.is_empty(self.all_exercises.daily):
                self.refill("daily")
                self.refill("flexibility")
                self.reset_stage()

            if self.is_empty(self.all_exercises.flexibility):
                self.refill("flexibility")
            
        return exercises
