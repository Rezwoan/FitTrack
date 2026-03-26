import customtkinter as ctk
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from services import data_service


class HistoryPage(ctk.CTkFrame):

    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.user_data = user_data
        self.user_id = user_data["user_id"]

        self.build_page()

    def build_page(self):
        lbl_title = ctk.CTkLabel(self, text="Workout History", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_title.pack(anchor="w", pady=(0, 12))

        pnl_columns = ctk.CTkFrame(self, fg_color="transparent")
        pnl_columns.pack(fill="both", expand=True)
        pnl_columns.grid_columnconfigure(0, weight=1)
        pnl_columns.grid_columnconfigure(1, weight=2)
        pnl_columns.grid_rowconfigure(0, weight=1)

        self.build_left_panel(pnl_columns)
        self.build_right_panel(pnl_columns)

    def build_left_panel(self, parent):
        pnl = ctk.CTkFrame(parent)
        pnl.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        lbl = ctk.CTkLabel(pnl, text="Past Sessions", anchor="w")
        lbl.pack(anchor="w", padx=10, pady=(10, 6))

        pnl_list = ctk.CTkScrollableFrame(pnl)
        pnl_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        dates = data_service.get_all_log_dates(self.user_id)

        if len(dates) == 0:
            lbl_empty = ctk.CTkLabel(pnl_list, text="No sessions yet", text_color="gray")
            lbl_empty.pack(pady=20)
        else:
            for date_str in dates:
                btn = ctk.CTkButton(pnl_list, text=date_str, anchor="w", fg_color="transparent",
                                    command=lambda d=date_str: self.show_session_summary(d))
                btn.pack(fill="x", pady=2)

    def build_right_panel(self, parent):
        self.pnl_right = ctk.CTkFrame(parent)
        self.pnl_right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        lbl_hint = ctk.CTkLabel(self.pnl_right, text="Select a session to view details", text_color="gray")
        lbl_hint.pack(expand=True)

    def show_session_summary(self, date_str):
        for w in self.pnl_right.winfo_children():
            w.destroy()

        log = data_service.load_log(self.user_id, date_str)

        pnl_content = ctk.CTkScrollableFrame(self.pnl_right)
        pnl_content.pack(fill="both", expand=True, padx=20, pady=20)

        lbl_date = ctk.CTkLabel(pnl_content, text=date_str, font=ctk.CTkFont(size=18, weight="bold"))
        lbl_date.pack(anchor="w", pady=(0, 4))

        if log.workout_name is not None:
            lbl_workout = ctk.CTkLabel(pnl_content, text=f"Workout: {log.workout_name}", text_color="gray")
            lbl_workout.pack(anchor="w", pady=(0, 10))

        if log.body_weight is not None:
            lbl_bw = ctk.CTkLabel(pnl_content, text=f"Body Weight: {log.body_weight} kg")
            lbl_bw.pack(anchor="w", pady=(0, 16))

        for ex in log.exercises:
            lbl_ex = ctk.CTkLabel(pnl_content, text=ex.exercise_name, font=ctk.CTkFont(weight="bold"))
            lbl_ex.pack(anchor="w", pady=(8, 2))

            for i, s in enumerate(ex.sets):
                if s.done:
                    status = "done"
                else:
                    status = "skipped"
                lbl_set = ctk.CTkLabel(pnl_content,
                                       text=f"  Set {i+1}: {s.reps} reps @ {s.weight} kg  [{status}]",
                                       anchor="w")
                lbl_set.pack(anchor="w")
