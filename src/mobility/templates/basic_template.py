from src.mobility.templates.base_template import BaseTemplate


class BasicTemplate(BaseTemplate):
    """
    Stage 1:
        Daily
        33% Neck
    Stage 2:
        Bonus
        33% Neck
    """
    name = "Basic"

    def _stage_1(self):
        return [
            self.pop(self.all_exercises.daily),
            self._neck_exercise()
        ]

    def _stage_2(self):
        return [
            self.pop(self.all_exercises.daily),
            self._neck_exercise()
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
                self.reset_stage()

        return exercises
