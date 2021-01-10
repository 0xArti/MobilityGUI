from src.mobility.templates.base_template import BaseTemplate


class SimpleTemplate(BaseTemplate):
    """
    Stage 1: 
        Daily
        33% Neck
    """
    name = "Simple"

    def _stage_1(self):
        return [
            self.pop(self.all_exercises.daily),
            self._neck_exercise()
        ]

    def _generate_exercises(self):
        exercises = []

        if not self.is_empty(self.all_exercises.daily):
            exercises.extend(self._stage_1())

        if self.is_empty(self.all_exercises.daily):
            self.refill("daily")

        return exercises

