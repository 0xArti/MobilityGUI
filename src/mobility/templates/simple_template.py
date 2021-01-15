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
            self._neck_exercise(),
            self.pop_n(category="daily", increase=True)
        ]
