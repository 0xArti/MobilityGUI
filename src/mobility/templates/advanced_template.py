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
        Flexibility
    """
    name = "Advanced"
    
    def _stage_1(self):
        return [
            self._neck_exercise(chance=2),
            self.pop_n(category="daily", amount=2, increase=True)
        ]

    def _stage_2(self):
        if random.randint(0, 1) == 0:
            first_exercise, second_exercise = self.pop_n(category="bonus", amount=2)
        else:
            first_exercise = self.pop_n(category="daily")
            second_exercise = self.pop_n(category="bonus")

        return [
            first_exercise,
            second_exercise,
            self._neck_exercise(),
            self.pop_n(category="power"),
            self.pop_n(
                category="flexibility", 
                increase=True,
                increase_callback=self.IncreaseCallback(
                    self.refill_multiple, "power", "bonus", "daily"
                )
            )
        ]
