class Exercise:
    def __init__(self, exercise_id, name, target_muscle, image):
        self.exercise_id = exercise_id
        self.name = name
        self.target_muscle = target_muscle
        self.image = image
        self.is_custom = False

    def to_dict(self):
        result = {}
        result["exercise_id"] = self.exercise_id
        result["name"] = self.name
        result["target_muscle"] = self.target_muscle
        result["image"] = self.image
        result["is_custom"] = self.is_custom
        return result

    @staticmethod
    def from_dict(data):
        return Exercise(
            data["exercise_id"],
            data["name"],
            data["target_muscle"],
            data["image"]
        )
