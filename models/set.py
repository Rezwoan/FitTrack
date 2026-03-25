class Set:
    # a single set in a workout, planned or performed
    # done is False by default, becomes True when the user ticks it off during a session

    def __init__(self, reps, weight, done=False):
        self.reps = reps
        self.weight = weight
        self.done = done

    def to_dict(self):
        result = {}
        result["reps"] = self.reps
        result["weight"] = self.weight
        result["done"] = self.done
        return result

    @staticmethod
    def from_dict(data):
        reps = data["reps"]
        weight = data["weight"]

        if "done" in data:
            done = data["done"]
        else:
            done = False

        return Set(reps, weight, done)
