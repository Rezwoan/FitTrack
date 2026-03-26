import uuid


class ExerciseSet:
    def __init__(self, reps, weight):
        self.reps = reps
        self.weight = weight

    def to_dict(self):
        return {"reps": self.reps, "weight": self.weight}

    @staticmethod
    def from_dict(data):
        return ExerciseSet(data["reps"], data["weight"])


class PlanExercise:
    def __init__(self, exercise_id, exercise_name, sets=None):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.sets = sets if sets is not None else []

    def to_dict(self):
        sets_list = []
        for s in self.sets:
            sets_list.append(s.to_dict())
        return {
            "exercise_id": self.exercise_id,
            "exercise_name": self.exercise_name,
            "sets": sets_list
        }

    @staticmethod
    def from_dict(data):
        sets_data = data.get("sets", [])
        sets = []
        for s in sets_data:
            sets.append(ExerciseSet.from_dict(s))
        return PlanExercise(data["exercise_id"], data["exercise_name"], sets)


class WorkoutPlan:
    def __init__(self, plan_id, name, exercises=None):
        self.plan_id = plan_id
        self.name = name
        self.exercises = exercises if exercises is not None else []

    def to_dict(self):
        exercises_list = []
        for e in self.exercises:
            exercises_list.append(e.to_dict())
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "exercises": exercises_list
        }

    @staticmethod
    def from_dict(data):
        exercises_data = data.get("exercises", [])
        exercises = []
        for e in exercises_data:
            exercises.append(PlanExercise.from_dict(e))
        return WorkoutPlan(data["plan_id"], data["name"], exercises)

    @staticmethod
    def create_new(name):
        return WorkoutPlan(plan_id=str(uuid.uuid4()), name=name)
