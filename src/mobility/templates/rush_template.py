import random
from src.mobility.templates.base_template import BaseTemplate


class RushTemplate(BaseTemplate):
    """
    Stage 1:
        Daily * 4
        50% Neck
    Stage 2:
        Bonus * 3
        33% Neck
        25% Power
    Stage 3:
        Flexibility
        33% Neck
        20% Power
    Stage 4:
        Balance
        Massage
        33% Neck
    """
    name = "Rush"

    def _stage_1(self):
        return [
            self._neck_exercise(chance=2),
            self.pop_n(category="daily", amount=4, increase=True)
        ]

    def _stage_2(self):
        return [
            self._neck_exercise(),
            self.pop_n(category="bonus", amount=3, increase=True),
            self.pop_n(category="power", chance=4)
        ]

    def _stage_3(self):
        return [
            self._neck_exercise(),
            self.pop_n(category="flexibility", increase=True),
            self.pop_n(category="power", chance=5)
        ]

    def _stage_4(self):
        return [
            self._neck_exercise(),
            self.pop_n(category="balance", increase=True),
            self.pop_n(category="massage"),
        ]
