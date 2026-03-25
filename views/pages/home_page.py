import customtkinter as ctk
import os
import sys
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


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

        lbl_hint = ctk.CTkLabel(pnl, text="Log your weight for today (kg)", text_color="gray")
        lbl_hint.pack(anchor="w", padx=20, pady=(0, 8))

        self.ent_weight = ctk.CTkEntry(pnl, placeholder_text="e.g. 72.5")
        self.ent_weight.pack(fill="x", padx=20, pady=(0, 8))

        btn_save_weight = ctk.CTkButton(pnl, text="Save Weight", command=self.handle_save_weight)
        btn_save_weight.pack(fill="x", padx=20, pady=(8, 20))

    def build_workout_section(self, parent):
        pnl = ctk.CTkFrame(parent)
        pnl.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=4)

        lbl = ctk.CTkLabel(pnl, text="Workout", font=ctk.CTkFont(size=16, weight="bold"))
        lbl.pack(anchor="w", padx=20, pady=(20, 10))

        # TODO: load workouts from data and show dropdown to start
        lbl_hint = ctk.CTkLabel(pnl, text="No workout plans yet", text_color="gray")
        lbl_hint.pack(anchor="w", padx=20)

    def handle_save_weight(self):
        weight_str = self.ent_weight.get().strip()
        if weight_str == "":
            return
        # TODO: save to log file
        print("saving weight:", weight_str)
