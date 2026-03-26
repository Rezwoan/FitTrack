import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from models.exercise import Exercise
from models.custom_exercise import CustomExercise
from models.workout import Workout
from models.workout_log import WorkoutLog


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
USERS_DIR = os.path.join(DATA_DIR, "users")


def get_user_folder(user_id):
    return os.path.join(USERS_DIR, user_id)


def load_built_in_exercises():
    path = os.path.join(DATA_DIR, "exercises.json")
    with open(path, "r") as f:
        data = json.load(f)

    exercises = []
    for item in data["exercises"]:
        ex = Exercise.from_dict(item)
        exercises.append(ex)
    return exercises


def load_custom_exercises(user_id):
    path = os.path.join(get_user_folder(user_id), "custom_exercises.json")
    with open(path, "r") as f:
        data = json.load(f)

    exercises = []
    for item in data["exercises"]:
        ex = CustomExercise.from_dict(item)
        exercises.append(ex)
    return exercises


def save_custom_exercises(user_id, exercises):
    path = os.path.join(get_user_folder(user_id), "custom_exercises.json")
    exercises_list = []
    for ex in exercises:
        exercises_list.append(ex.to_dict())

    with open(path, "w") as f:
        json.dump({"exercises": exercises_list}, f, indent=4)


def load_workouts(user_id):
    path = os.path.join(get_user_folder(user_id), "workout_plans.json")
    with open(path, "r") as f:
        data = json.load(f)

    workouts = []
    for item in data["plans"]:
        w = Workout.from_dict(item)
        workouts.append(w)
    return workouts


def save_workouts(user_id, workouts):
    path = os.path.join(get_user_folder(user_id), "workout_plans.json")
    plans_list = []
    for w in workouts:
        plans_list.append(w.to_dict())

    with open(path, "w") as f:
        json.dump({"plans": plans_list}, f, indent=4)


def load_log(user_id, date_str):
    path = os.path.join(get_user_folder(user_id), "logs", date_str + ".json")
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        data = json.load(f)

    return WorkoutLog.load_from_dict(data)


def save_log(user_id, log):
    path = os.path.join(get_user_folder(user_id), "logs", log.date + ".json")
    with open(path, "w") as f:
        json.dump(log.to_dict(), f, indent=4)


def get_all_log_dates(user_id):
    logs_folder = os.path.join(get_user_folder(user_id), "logs")
    dates = []
    for filename in os.listdir(logs_folder):
        if filename.endswith(".json"):
            date_str = filename.replace(".json", "")
            dates.append(date_str)
    dates.sort(reverse=True)
    return dates


def load_profile(user_id):
    path = os.path.join(get_user_folder(user_id), "profile.json")
    with open(path, "r") as f:
        return json.load(f)
