import uuid
from models.exercise import Exercise


class CustomExercise(Exercise):
    # user creates their own exercise, inherits everything from Exercise

    def __init__(self, exercise_id, name, target_muscle, image, created_by_user_id):
        super().__init__(exercise_id, name, target_muscle, image)
        self.is_custom = True
        self.created_by_user_id = created_by_user_id

    def to_dict(self):
        result = super().to_dict()
        result["created_by_user_id"] = self.created_by_user_id
        return result

    @staticmethod
    def create_new(name, target_muscle, image, user_id):
        new_id = str(uuid.uuid4())
        return CustomExercise(new_id, name, target_muscle, image, user_id)

    @staticmethod
    def from_dict(data):
        return CustomExercise(
            data["exercise_id"],
            data["name"],
            data["target_muscle"],
            data["image"],
            data["created_by_user_id"]
        )
