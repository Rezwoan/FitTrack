import customtkinter as ctk
import os
import sys
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from services import data_service


class HomePage(ctk.CTkFrame):

    def __init__(self, parent, user_data, app):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.app = app
        self.user_data = user_data
        self.user_id = user_data["user_id"]
        self.today = str(date.today())

        self.build_page()

    def build_page(self):
        lbl_title = ctk.CTkLabel(self, text="Today", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_title.pack(anchor="w", pady=(0, 4))

        lbl_date = ctk.CTkLabel(self, text=self.today, text_color="gray")
        lbl_date.pack(anchor="w", pady=(0, 20))

        pnl_columns = ctk.CTkFrame(self, fg_color="transparent")
        pnl_columns.pack(fill="both", expand=True)
        pnl_columns.grid_columnconfigure(0, weight=1)
        pnl_columns.grid_columnconfigure(1, weight=1)
        pnl_columns.grid_rowconfigure(0, weight=1)

        self.build_weight_section(pnl_columns)
        self.build_workout_section(pnl_columns)

    def build_weight_section(self, parent):
        pnl = ctk.CTkFrame(parent)
        pnl.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=4)

        lbl = ctk.CTkLabel(pnl, text="Body Weight", font=ctk.CTkFont(size=16, weight="bold"))
        lbl.pack(anchor="w", padx=20, pady=(20, 10))

        today_log = data_service.load_log(self.user_id, self.today)

        if today_log is not None and today_log.body_weight is not None:
            lbl_logged = ctk.CTkLabel(pnl, text=f"Logged: {today_log.body_weight} kg", text_color="gray")
            lbl_logged.pack(anchor="w", padx=20)
        else:
            lbl_hint = ctk.CTkLabel(pnl, text="Log your weight for today (kg)", text_color="gray")
            lbl_hint.pack(anchor="w", padx=20, pady=(0, 8))

            self.ent_weight = ctk.CTkEntry(pnl, placeholder_text="e.g. 72.5")
            self.ent_weight.pack(fill="x", padx=20, pady=(0, 8))

            self.lbl_weight_msg = ctk.CTkLabel(pnl, text="")
            self.lbl_weight_msg.pack(padx=20)

            btn_save_weight = ctk.CTkButton(pnl, text="Save Weight", command=self.handle_save_weight)
            btn_save_weight.pack(fill="x", padx=20, pady=(8, 20))

    def build_workout_section(self, parent):
        pnl = ctk.CTkFrame(parent)
        pnl.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        lbl = ctk.CTkLabel(pnl, text="Workout", font=ctk.CTkFont(size=16, weight="bold"))
        lbl.pack(anchor="w", padx=20, pady=(20, 10))

        today_log = data_service.load_log(self.user_id, self.today)

        if today_log is not None and today_log.workout_id is not None:
            lbl_done = ctk.CTkLabel(pnl, text=f"Completed: {today_log.workout_name}", text_color="gray")
            lbl_done.pack(anchor="w", padx=20, pady=(0, 10))

            for ex in today_log.exercises:
                done_sets = 0
                for s in ex.sets:
                    if s.done:
                        done_sets = done_sets + 1
                lbl_ex = ctk.CTkLabel(pnl, text=f"  {ex.exercise_name}: {done_sets}/{len(ex.sets)} sets")
                lbl_ex.pack(anchor="w", padx=20)
        else:
            workouts = data_service.load_workouts(self.user_id)

            if len(workouts) == 0:
                lbl_no_plan = ctk.CTkLabel(pnl, text="No plans yet. Create one in Workout Plans.", text_color="gray")
                lbl_no_plan.pack(padx=20, pady=20)
            else:
                lbl_hint = ctk.CTkLabel(pnl, text="Select a plan to start", text_color="gray")
                lbl_hint.pack(anchor="w", padx=20, pady=(0, 8))

                plan_names = []
                self.workout_map = {}
                for w in workouts:
                    plan_names.append(w.name)
                    self.workout_map[w.name] = w

                self.opt_plan = ctk.CTkOptionMenu(pnl, values=plan_names)
                self.opt_plan.pack(fill="x", padx=20, pady=(0, 8))

                self.lbl_workout_msg = ctk.CTkLabel(pnl, text="")
                self.lbl_workout_msg.pack(padx=20)

                btn_start = ctk.CTkButton(pnl, text="Start Workout", command=self.handle_start_workout)
                btn_start.pack(fill="x", padx=20, pady=(8, 20))

    def handle_save_weight(self):
        weight_str = self.ent_weight.get().strip()
        if weight_str == "":
            self.lbl_weight_msg.configure(text="Please enter your weight", text_color="red")
            return

        try:
            weight = float(weight_str)
        except ValueError:
            self.lbl_weight_msg.configure(text="Must be a number", text_color="red")
            return

        today_log = data_service.load_log(self.user_id, self.today)
        if today_log is None:
            from models.workout_log import WorkoutLog
            today_log = WorkoutLog(self.user_id, None, None, self.today)

        today_log.body_weight = weight
        data_service.save_log(self.user_id, today_log)
        self.lbl_weight_msg.configure(text="Saved!", text_color="green")

    def handle_start_workout(self):
        selected_name = self.opt_plan.get()
        workout = self.workout_map[selected_name]
        self.app.show_workout_session(self.user_data, workout)
