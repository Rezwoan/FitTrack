import customtkinter as ctk
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from services import auth_service


GOALS = ["Get Lean", "Build Muscle Mass", "Reduce Weight","Increase Strength", "Maintain Weight"]
MUSCLES = ["Back", "Shoulder", "Arm", "Chest", "Abs", "Glute", "Leg"]
GENDERS = ["Male", "Female"]


class ProfileSetupPage(ctk.CTkFrame):

    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.app = parent
        self.user_data = user_data
        self.muscle_vars = {}

        self.build_page()

    def build_page(self):
        # title at the top
        lbl_title = ctk.CTkLabel(self, text="Complete Your Profile", font=ctk.CTkFont(size=22, weight="bold"))
        lbl_title.pack(pady=(30, 4))

        lbl_sub = ctk.CTkLabel(self, text="Tell us a bit about yourself to get started", text_color="gray")
        lbl_sub.pack(pady=(0, 20))

        # two column layout
        pnl_columns = ctk.CTkFrame(self, fg_color="transparent")
        pnl_columns.pack(fill="both", expand=True, padx=80)
        pnl_columns.grid_columnconfigure((0, 1), weight=1, uniform="col")
        pnl_columns.grid_rowconfigure(0, weight=1)

        self.build_left_column(pnl_columns)
        self.build_right_column(pnl_columns)

        # error + save at the bottom
        self.lbl_error = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_error.pack(pady=(10, 4))

        self.btn_save = ctk.CTkButton(self, text="Save & Continue", command=self.handle_save)
        self.btn_save.pack(pady=(0, 30))

    def build_left_column(self, parent):
        pnl_left = ctk.CTkFrame(parent, fg_color="transparent")
        pnl_left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        pnl_left.grid_columnconfigure((0, 1), weight=1)

        # height and weight side by side
        ctk.CTkLabel(pnl_left, text="Height (cm)", anchor="w").grid(row=0, column=0, sticky="w", pady=(0, 4), padx=(0, 10))
        ctk.CTkLabel(pnl_left, text="Current Weight (kg)", anchor="w").grid(row=0, column=1, sticky="w", pady=(0, 4))

        self.ent_height = ctk.CTkEntry(pnl_left, placeholder_text="e.g. 175")
        self.ent_height.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 20))

        self.ent_weight = ctk.CTkEntry(pnl_left, placeholder_text="e.g. 70")
        self.ent_weight.grid(row=1, column=1, sticky="ew", pady=(0, 20))

        # gender
        ctk.CTkLabel(pnl_left, text="Gender", anchor="w").grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 4))
        self.opt_gender = ctk.CTkOptionMenu(pnl_left, values=GENDERS)
        self.opt_gender.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        # goal
        ctk.CTkLabel(pnl_left, text="Goal", anchor="w").grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 4))
        self.opt_goal = ctk.CTkOptionMenu(pnl_left, values=GOALS)
        self.opt_goal.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        # target weight
        ctk.CTkLabel(pnl_left, text="Target Weight (kg)", anchor="w").grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 4))
        self.ent_target_weight = ctk.CTkEntry(pnl_left, placeholder_text="e.g. 65")
        self.ent_target_weight.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(0, 20))

    def build_right_column(self, parent):
        pnl_right = ctk.CTkFrame(parent, fg_color="transparent")
        pnl_right.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        pnl_right.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(pnl_right, text="Target Muscles", anchor="w").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 12))

        for i, muscle in enumerate(MUSCLES):
            var = ctk.BooleanVar()
            self.muscle_vars[muscle] = var
            cb = ctk.CTkCheckBox(pnl_right, text=muscle, variable=var)
            cb.grid(row=(i // 4) + 1, column=i % 4, sticky="w", pady=10, padx=6)

        # optional 1RM below the checkboxes
        ctk.CTkLabel(pnl_right, text="1 Rep Max - optional", anchor="w", text_color="gray").grid(row=3, column=0, columnspan=4, sticky="w", pady=(24, 4))

        ctk.CTkLabel(pnl_right, text="Max Squat (kg)", anchor="w").grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 4))
        ctk.CTkLabel(pnl_right, text="Max Bench (kg)", anchor="w").grid(row=4, column=2, columnspan=2, sticky="w", pady=(0, 4))

        self.ent_squat = ctk.CTkEntry(pnl_right, placeholder_text="optional")
        self.ent_squat.grid(row=5, column=0, columnspan=2, sticky="ew", padx=(0, 10), pady=(0, 16))

        self.ent_bench = ctk.CTkEntry(pnl_right, placeholder_text="optional")
        self.ent_bench.grid(row=5, column=2, columnspan=2, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(pnl_right, text="Max Deadlift (kg)", anchor="w").grid(row=6, column=0, columnspan=2, sticky="w", pady=(0, 4))
        self.ent_deadlift = ctk.CTkEntry(pnl_right, placeholder_text="optional")
        self.ent_deadlift.grid(row=7, column=0, columnspan=2, sticky="ew", padx=(0, 10))

    def handle_save(self):
        height = self.ent_height.get().strip()
        weight = self.ent_weight.get().strip()
        target_weight = self.ent_target_weight.get().strip()

        if height == "" or weight == "" or target_weight == "":
            self.lbl_error.configure(text="Height, weight and target weight are required")
            return

        try:
            height = float(height)
            weight = float(weight)
            target_weight = float(target_weight)
        except ValueError:
            self.lbl_error.configure(text="Height, weight and target weight must be numbers")
            return

        selected_muscles = [m for m, var in self.muscle_vars.items() if var.get()]
        if len(selected_muscles) == 0:
            self.lbl_error.configure(text="Please select at least one target muscle")
            return

        squat = self.ent_squat.get().strip()
        bench = self.ent_bench.get().strip()
        deadlift = self.ent_deadlift.get().strip()

        profile_data = {
            "height": height,
            "weight": weight,
            "gender": self.opt_gender.get(),
            "target_weight": target_weight,
            "goal": self.opt_goal.get(),
            "target_muscles": selected_muscles,
            "max_squat": float(squat) if squat != "" else None,
            "max_bench": float(bench) if bench != "" else None,
            "max_deadlift": float(deadlift) if deadlift != "" else None
        }

        auth_service.save_profile(self.user_data["user_id"], profile_data)
        auth_service.mark_profile_complete(self.user_data["user_id"])
        self.user_data["profile_complete"] = True

        self.app.show_dashboard()
