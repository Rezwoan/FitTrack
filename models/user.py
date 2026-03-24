from typing import Optional


class User:
    def __init__(
        self,
        user_id: str,
        name: str,
        email: str,
        password_hash: str,
        profile_image: Optional[str] = None,
        height: Optional[float] = None,
        weight: Optional[float] = None,
        gender: Optional[str] = None,
        target_weight: Optional[float] = None,
        goal: Optional[str] = None,
        target_muscles: Optional[list] = None,
        max_squat: Optional[float] = None,
        max_bench: Optional[float] = None,
        max_deadlift: Optional[float] = None,
        created_at: Optional[str] = None,
        profile_complete: bool = False,
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.profile_image = profile_image
        self.height = height
        self.weight = weight
        self.gender = gender
        self.target_weight = target_weight
        self.goal = goal
        self.target_muscles = target_muscles if target_muscles is not None else []
        self.max_squat = max_squat
        self.max_bench = max_bench
        self.max_deadlift = max_deadlift
        self.created_at = created_at
        self.profile_complete = profile_complete
