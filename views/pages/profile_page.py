import customtkinter as ctk
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from services import data_service


class ProfilePage(ctk.CTkFrame):

    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.user_data = user_data
        self.user_id = user_data["user_id"]

        self.build_page()

    def build_page(self):
        lbl_title = ctk.CTkLabel(self, text="Profile", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_title.pack(anchor="w", pady=(0, 4))

        lbl_name = ctk.CTkLabel(self, text=self.user_data["name"], text_color="gray")
        lbl_name.pack(anchor="w", pady=(0, 20))

        profile = data_service.load_profile(self.user_id)

        pnl_stats = ctk.CTkFrame(self)
        pnl_stats.pack(fill="x", pady=(0, 12))
        pnl_stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.add_stat(pnl_stats, "Height", profile["height"], "cm", 0)
        self.add_stat(pnl_stats, "Weight", profile["weight"], "kg", 1)
        self.add_stat(pnl_stats, "Target Weight", profile["target_weight"], "kg", 2)
        self.add_stat(pnl_stats, "Gender", profile["gender"], "", 3)

        pnl_goal = ctk.CTkFrame(self)
        pnl_goal.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(pnl_goal, text="Goal", text_color="gray", anchor="w").pack(anchor="w", padx=20, pady=(16, 4))
        goal_text = profile["goal"] if profile["goal"] else "Not set"
        ctk.CTkLabel(pnl_goal, text=goal_text, anchor="w", font=ctk.CTkFont(size=15)).pack(anchor="w", padx=20,
                                                                                             pady=(0, 16))

        pnl_muscles = ctk.CTkFrame(self)
        pnl_muscles.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(pnl_muscles, text="Target Muscles", text_color="gray", anchor="w").pack(anchor="w", padx=20,
                                                                                               pady=(16, 4))
        muscles = profile["target_muscles"]
        if muscles and len(muscles) > 0:
            muscles_text = ",  ".join(muscles)
        else:
            muscles_text = "Not set"
        ctk.CTkLabel(pnl_muscles, text=muscles_text, anchor="w").pack(anchor="w", padx=20, pady=(0, 16))

        squat = profile["max_squat"]
        bench = profile["max_bench"]
        deadlift = profile["max_deadlift"]

        if squat is not None or bench is not None or deadlift is not None:
            pnl_orm = ctk.CTkFrame(self)
            pnl_orm.pack(fill="x")
            pnl_orm.grid_columnconfigure((0, 1, 2), weight=1)

            ctk.CTkLabel(pnl_orm, text="1 Rep Max", text_color="gray", anchor="w").grid(
                row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(16, 8))

            col = 0
            if squat is not None:
                self.add_stat(pnl_orm, "Squat", squat, "kg", col, row=1)
                col = col + 1
            if bench is not None:
                self.add_stat(pnl_orm, "Bench", bench, "kg", col, row=1)
                col = col + 1
            if deadlift is not None:
                self.add_stat(pnl_orm, "Deadlift", deadlift, "kg", col, row=1)

            ctk.CTkLabel(pnl_orm, text="").grid(row=2, column=0, pady=8)

    def add_stat(self, parent, label, value, unit, column, row=0):
        pnl = ctk.CTkFrame(parent, fg_color="transparent")
        pnl.grid(row=row, column=column, padx=20, pady=16, sticky="w")

        ctk.CTkLabel(pnl, text=label, text_color="gray").pack(anchor="w")

        if value is None:
            display = "Not set"
        elif unit != "":
            display = str(value) + " " + unit
        else:
            display = str(value)

        ctk.CTkLabel(pnl, text=display, font=ctk.CTkFont(size=15)).pack(anchor="w")
