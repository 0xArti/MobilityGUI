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
        Flexibility * 2
        25% Neck
    """
    name = "Intermediate"

    def _stage_1(self):
        return [
            self._neck_exercise(),
            self.pop_n(category="daily", increase=True)
        ]

    def _stage_2(self):
        return [
            self._neck_exercise(),
            self.pop_n(category="bonus", increase=True),
            self.pop_n(category="power", chance=5)
        ]

    def _stage_3(self):
        return [
            self._neck_exercise(chance=4),
            self.pop_n(category="daily"),
            self.pop_n(
                category="flexibility",
                amount=2,
                increase=True
            )
        ]
