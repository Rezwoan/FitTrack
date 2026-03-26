import customtkinter as ctk
import os
import sys
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from services import data_service
from models.workout_log import WorkoutLog


class ActiveWorkoutPage(ctk.CTkFrame):

    def __init__(self, parent, user_data, workout):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.app = parent
        self.user_data = user_data
        self.user_id = user_data["user_id"]
        self.workout = workout
        self.today = str(date.today())

        self.log = WorkoutLog.start_new_session(self.user_id, workout, self.today)

        self.build_page()

    def build_page(self):
        pnl_top = ctk.CTkFrame(self, fg_color="transparent")
        pnl_top.pack(fill="x", padx=20, pady=(16, 0))

        lbl_title = ctk.CTkLabel(pnl_top, text=self.workout.name, font=ctk.CTkFont(size=20, weight="bold"))
        lbl_title.pack(side="left")

        btn_finish = ctk.CTkButton(pnl_top, text="Finish Workout", command=self.handle_finish)
        btn_finish.pack(side="right")

        pnl_bw = ctk.CTkFrame(self, fg_color="transparent")
        pnl_bw.pack(fill="x", padx=20, pady=(12, 0))

        lbl_bw = ctk.CTkLabel(pnl_bw, text="Body Weight (kg):", anchor="w")
        lbl_bw.pack(side="left", padx=(0, 10))

        self.ent_body_weight = ctk.CTkEntry(pnl_bw, placeholder_text="optional", width=120)
        self.ent_body_weight.pack(side="left")

        pnl_exercises = ctk.CTkScrollableFrame(self)
        pnl_exercises.pack(fill="both", expand=True, padx=20, pady=(12, 16))

        self.set_widgets = []

        for ex_index, performed_ex in enumerate(self.log.exercises):
            pnl_ex = ctk.CTkFrame(pnl_exercises)
            pnl_ex.pack(fill="x", pady=(0, 12))

            lbl_ex_name = ctk.CTkLabel(pnl_ex, text=performed_ex.exercise_name,
                                       font=ctk.CTkFont(size=15, weight="bold"), anchor="w")
            lbl_ex_name.pack(anchor="w", padx=16, pady=(12, 8))

            ex_set_widgets = []

            for set_index, s in enumerate(performed_ex.sets):
                pnl_set = ctk.CTkFrame(pnl_ex, fg_color="transparent")
                pnl_set.pack(fill="x", padx=16, pady=(0, 6))

                lbl_set_num = ctk.CTkLabel(pnl_set, text=f"Set {set_index + 1}", width=50, anchor="w")
                lbl_set_num.pack(side="left", padx=(0, 10))

                lbl_reps = ctk.CTkLabel(pnl_set, text="Reps:", anchor="w")
                lbl_reps.pack(side="left", padx=(0, 4))

                ent_reps = ctk.CTkEntry(pnl_set, width=60)
                ent_reps.insert(0, str(s.reps))
                ent_reps.pack(side="left", padx=(0, 12))

                lbl_weight = ctk.CTkLabel(pnl_set, text="Weight:", anchor="w")
                lbl_weight.pack(side="left", padx=(0, 4))

                ent_weight = ctk.CTkEntry(pnl_set, width=70)
                ent_weight.insert(0, str(s.weight))
                ent_weight.pack(side="left", padx=(0, 12))

                btn_done = ctk.CTkButton(pnl_set, text="Done", width=70,
                                         command=lambda ei=ex_index, si=set_index: self.toggle_set_done(ei, si))
                btn_done.pack(side="left")

                ex_set_widgets.append({
                    "ent_reps": ent_reps,
                    "ent_weight": ent_weight,
                    "btn_done": btn_done
                })

            self.set_widgets.append(ex_set_widgets)
            ctk.CTkLabel(pnl_ex, text="").pack(pady=4)

    def toggle_set_done(self, ex_index, set_index):
        s = self.log.exercises[ex_index].sets[set_index]
        widgets = self.set_widgets[ex_index][set_index]

        reps_str = widgets["ent_reps"].get().strip()
        weight_str = widgets["ent_weight"].get().strip()

        if reps_str != "":
            s.reps = int(reps_str)
        if weight_str != "":
            s.weight = float(weight_str)

        s.done = not s.done

        if s.done:
            widgets["btn_done"].configure(fg_color="green")
        else:
            widgets["btn_done"].configure(fg_color=None)

    def handle_finish(self):
        for ex_index, performed_ex in enumerate(self.log.exercises):
            for set_index, s in enumerate(performed_ex.sets):
                widgets = self.set_widgets[ex_index][set_index]
                reps_str = widgets["ent_reps"].get().strip()
                weight_str = widgets["ent_weight"].get().strip()

                if reps_str != "":
                    s.reps = int(reps_str)
                if weight_str != "":
                    s.weight = float(weight_str)

        bw_str = self.ent_body_weight.get().strip()
        if bw_str != "":
            self.log.body_weight = float(bw_str)

        data_service.save_log(self.user_id, self.log)
        self.app.show_dashboard()
