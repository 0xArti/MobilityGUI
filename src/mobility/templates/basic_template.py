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
            self._neck_exercise(),
            self.pop_n(category="daily", increase=True)
        ]

    def _stage_2(self):
        return [
            self._neck_exercise(),
            self.pop_n(category="bonus", increase=True)
        ]
