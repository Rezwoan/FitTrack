import uuid
from models.set import Set


class PlannedExercise:
    # one exercise inside a workout, with its planned sets

    def __init__(self, exercise_id, exercise_name):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.sets = []

    def add_set(self, reps, weight):
        new_set = Set(reps, weight)
        self.sets.append(new_set)

    def to_dict(self):
        sets_list = []
        for s in self.sets:
            sets_list.append(s.to_dict())

        result = {}
        result["exercise_id"] = self.exercise_id
        result["exercise_name"] = self.exercise_name
        result["sets"] = sets_list
        return result

    @staticmethod
    def from_dict(data):
        entry = PlannedExercise(data["exercise_id"], data["exercise_name"])
        for s in data["sets"]:
            loaded_set = Set.from_dict(s)
            entry.sets.append(loaded_set)
        return entry


class Workout:
    # a workout plan, made up of multiple PlannedExercise entries

    def __init__(self, workout_id, name):
        self.workout_id = workout_id
        self.name = name
        self.exercises = []

    def add_exercise(self, exercise):
        # exercise is an Exercise or CustomExercise object
        entry = PlannedExercise(exercise.exercise_id, exercise.name)
        self.exercises.append(entry)

    def to_dict(self):
        exercises_list = []
        for e in self.exercises:
            exercises_list.append(e.to_dict())

        result = {}
        result["workout_id"] = self.workout_id
        result["name"] = self.name
        result["exercises"] = exercises_list
        return result

    @staticmethod
    def from_dict(data):
        workout = Workout(data["workout_id"], data["name"])
        for e in data["exercises"]:
            entry = PlannedExercise.from_dict(e)
            workout.exercises.append(entry)
        return workout

    @staticmethod
    def create_new(name):
        new_id = str(uuid.uuid4())
        return Workout(new_id, name)
