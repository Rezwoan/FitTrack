from models.set import Set


class PerformedExercise:

    def __init__(self, exercise_id, exercise_name):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.sets = []

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
        entry = PerformedExercise(data["exercise_id"], data["exercise_name"])
        for s in data["sets"]:
            loaded_set = Set.from_dict(s)
            entry.sets.append(loaded_set)
        return entry


class WorkoutLog:

    def __init__(self, user_id, workout_id, workout_name, date):
        self.user_id = user_id
        self.workout_id = workout_id
        self.workout_name = workout_name
        self.date = date
        self.body_weight = None
        self.exercises = []

    @staticmethod
    def start_new_session(user_id, workout, date):
        log = WorkoutLog(user_id, workout.workout_id, workout.name, date)

        for planned in workout.exercises:
            performed = PerformedExercise(planned.exercise_id, planned.exercise_name)
            for s in planned.sets:
                performed_set = Set(s.reps, s.weight, done=False)
                performed.sets.append(performed_set)
            log.exercises.append(performed)

        return log

    @staticmethod
    def load_from_dict(data):
        log = WorkoutLog(
            data["user_id"],
            data["workout_id"],
            data["workout_name"],
            data["date"]
        )
        log.body_weight = data["body_weight"]

        for e in data["exercises"]:
            entry = PerformedExercise.from_dict(e)
            log.exercises.append(entry)

        return log

    def to_dict(self):
        exercises_list = []
        for e in self.exercises:
            exercises_list.append(e.to_dict())

        result = {}
        result["user_id"] = self.user_id
        result["workout_id"] = self.workout_id
        result["workout_name"] = self.workout_name
        result["date"] = self.date
        result["body_weight"] = self.body_weight
        result["exercises"] = exercises_list
        return result
