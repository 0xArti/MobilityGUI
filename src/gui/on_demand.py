
from src.gui.popup import Popup
from src.mobility.exercise_storage import ExerciseStorage


def main():
    popup = Popup()
    popup.initialize()
    exercise_storage = ExerciseStorage()
    exercise_storage.generate_exercise()
    popup.display(exercise_storage.current)


if __name__ == "__main__":
    main()
