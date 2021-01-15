from random import randint

from src import config_loader


class Exercise(config_loader.DynamicConfig):
    _ENABLED_KEY = "enabled"
    _EQUIPMENT_KEY = "equipment"

    def __init__(self, **options):
        super(Exercise, self).__init__(**options)

        if not hasattr(self, self._ENABLED_KEY):
            self[self._ENABLED_KEY] = True
        self._repetitions = None

    def _is_equipped(self, equipment_enabled, equipments):
        """
        If an exercises required any sort of equipment
         Check if user enabled 'equipment' in settings
         Check if the user have the specified equipment
         If not, ignore the exercise
        """
        if hasattr(self, self._EQUIPMENT_KEY):
            if not equipment_enabled:
                return False
            return equipments[self.equipment]
        return True
    
    def _regenerate_repetitions(self):
        self._repetitions = randint(int(self.min), int(self.max))

    def _random(self):
        """
        Generates random number of repetitions in range
        if not already generated
        """
        if not self._repetitions:
            self._regenerate_repetitions()
        return self._repetitions

    def _repeat(self):
        """
        For reapeat --> x<Number>
        for seconds --> <number> sec
        """
        if self.measure == "repeat":
            return f"x{self._random()}"
        if self.measure == "hold":
            return f"{self._random()} sec"

    def __str__(self):
        return f"{self.name} {self._repeat()}"