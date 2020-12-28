
from src.gui.popup import Popup
from src.mobility.exercise_cache import ExerciseCache


def main():
    popup = Popup()
    popup.initialize()
    exercise_cache = ExerciseCache()
    exercise_cache.generate_exercise()
    popup.display(exercise_cache.current)


if __name__ == "__main__":
    main()
