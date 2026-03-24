import json
import os
import uuid
import bcrypt
from datetime import date


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
USERS_DIR = os.path.join(DATA_DIR, "users")


def load_users():
    with open(USERS_FILE, "r") as f:
        data = json.load(f)
    return data["users"]

def save_users(users_list):
    with open(USERS_FILE, "w") as f:
        json.dump({"users": users_list}, f, indent=4)

def setup_user_folder(user_id):
    # create all folders and empty files for a new user
    folder = os.path.join(USERS_DIR, user_id)
    os.makedirs(folder, exist_ok=True)
    os.makedirs(os.path.join(folder, "logs"), exist_ok=True)

    with open(os.path.join(folder, "profile.json"), "w") as f:
        json.dump({"height": None, "weight": None, "gender": None,
                   "target_weight": None, "goal": None, "target_muscles": [],
                   "max_squat": None, "max_bench": None, "max_deadlift": None}, f, indent=4)

    with open(os.path.join(folder, "custom_exercises.json"), "w") as f:
        json.dump({"exercises": []}, f, indent=4)

    with open(os.path.join(folder, "workout_plans.json"), "w") as f:
        json.dump({"plans": []}, f, indent=4)


def signup(name, email, password):
    users = load_users()
    for u in users:
        if u["email"] == email:
            return False, "Email already registered"

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user_id = str(uuid.uuid4())

    new_user = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "password_hash": hashed,
        "profile_complete": False,
        "created_at": str(date.today())
    }

    users.append(new_user)
    save_users(users)
    setup_user_folder(user_id)

    return True, new_user


def login(email, password):
    users = load_users()
    for u in users:
        if u["email"] == email:
            if bcrypt.checkpw(password.encode(), u["password_hash"].encode()):
                return True, u
            else:
                return False, "Wrong password"

    return False, "No account found with that email"


def save_profile(user_id, profile_data):
    path = os.path.join(USERS_DIR, user_id, "profile.json")
    with open(path, "w") as f:
        json.dump(profile_data, f, indent=4)

def mark_profile_complete(user_id):
    users = load_users()
    for u in users:
        if u["user_id"] == user_id:
            u["profile_complete"] = True
            break
    save_users(users)
