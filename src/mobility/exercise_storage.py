from src.config_loader import DynamicConfig, load_from_configuration
from src.mobility.exercises_provider import get_exercises, get_exercises_types, \
    get_exercise_metadata
from src.mobility.templates import exercise_templates


class ExerciseStorage:
    def __init__(self):
        self.template = None
        self._all_exercises = None
        self.sorted_exercises = DynamicConfig(**get_exercises_types())
        self.exercises_copy = None
        self._current = None
        self._initialize()

    def _initialize(self):
        settings = DynamicConfig(**load_from_configuration("settings.json"))
        equipments = DynamicConfig(**load_from_configuration("exercises.json", "equipment"))

        self._all_exercises = get_exercises(settings.equipment, equipments)
        for key, value in self.sorted_exercises.items():
            self.sorted_exercises[key] = [exercise for exercise in self._all_exercises 
                                            if key in exercise.type]

        # instantiate Template object 
        template_class = exercise_templates[settings.template]
        self.template = template_class(self.sorted_exercises)  
        self._current = []

    def reset(self):
        """
        Re-loads the configuration
        Each day built on-top of fresh new config, so the user doesn't need to
         reset the service to update it.
        """
        self._initialize()

    def clear(self):
        for exercise in self._current:
            exercise._regenerate_repetitions()
        self._current = []

    def add(self, exercises):
        self._current.extend(exercises)
        
    def generate_exercise(self):
        exercises = self.template.generate_exercises()
        self.add(exercises)

    def update(self, updated_current):
        self._current = [exercise for exercise in self._current 
                         if str(exercise) in updated_current]

    @property
    def current(self):
        return [str(exercise) for exercise in self._current]
