import customtkinter as ctk
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from services import data_service
from models.custom_exercise import CustomExercise

MUSCLES = ["All", "Back", "Shoulder", "Arm", "Chest", "Abs", "Glute", "Leg"]


class ExercisesPage(ctk.CTkFrame):

    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.user_data = user_data
        self.user_id = user_data["user_id"]
        self.selected_muscle = "All"

        self.build_page()

    def build_page(self):
        lbl_title = ctk.CTkLabel(self, text="Exercises", font=ctk.CTkFont(size=20, weight="bold"))
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

        lbl_filter = ctk.CTkLabel(pnl, text="Filter by Muscle", anchor="w")
        lbl_filter.pack(anchor="w", padx=10, pady=(10, 4))

        self.opt_muscle = ctk.CTkOptionMenu(pnl, values=MUSCLES, command=self.handle_filter_change)
        self.opt_muscle.pack(fill="x", padx=10, pady=(0, 10))

        self.pnl_list = ctk.CTkScrollableFrame(pnl)
        self.pnl_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh_exercise_list()

    def build_right_panel(self, parent):
        self.pnl_right = ctk.CTkFrame(parent)
        self.pnl_right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        btn_add_custom = ctk.CTkButton(self.pnl_right, text="+ Add Custom Exercise",
                                       command=self.show_add_custom_form)
        btn_add_custom.pack(anchor="e", padx=20, pady=(16, 0))

        lbl_hint = ctk.CTkLabel(self.pnl_right, text="Select an exercise to view details", text_color="gray")
        lbl_hint.pack(expand=True)

    def refresh_exercise_list(self):
        for w in self.pnl_list.winfo_children():
            w.destroy()

        built_in = data_service.load_built_in_exercises()
        custom = data_service.load_custom_exercises(self.user_id)
        all_exercises = built_in + custom

        for ex in all_exercises:
            if self.selected_muscle != "All" and ex.target_muscle != self.selected_muscle:
                continue

            label = ex.name
            if ex.is_custom:
                label = label + " (custom)"

            btn = ctk.CTkButton(self.pnl_list, text=label, anchor="w", fg_color="transparent",
                                command=lambda e=ex: self.show_exercise_details(e))
            btn.pack(fill="x", pady=2)

    def handle_filter_change(self, value):
        self.selected_muscle = value
        self.refresh_exercise_list()

    def show_exercise_details(self, exercise):
        self.clear_right()

        btn_add_custom = ctk.CTkButton(self.pnl_right, text="+ Add Custom Exercise",
                                       command=self.show_add_custom_form)
        btn_add_custom.pack(anchor="e", padx=20, pady=(16, 0))

        lbl_name = ctk.CTkLabel(self.pnl_right, text=exercise.name,
                                 font=ctk.CTkFont(size=18, weight="bold"))
        lbl_name.pack(anchor="w", padx=20, pady=(20, 4))

        lbl_muscle = ctk.CTkLabel(self.pnl_right, text=f"Target Muscle: {exercise.target_muscle}",
                                   text_color="gray")
        lbl_muscle.pack(anchor="w", padx=20)

        if exercise.is_custom:
            lbl_tag = ctk.CTkLabel(self.pnl_right, text="Custom exercise", text_color="gray")
            lbl_tag.pack(anchor="w", padx=20, pady=(4, 0))

            btn_delete = ctk.CTkButton(self.pnl_right, text="Delete", fg_color="transparent",
                                       border_width=1,
                                       command=lambda: self.handle_delete_custom(exercise))
            btn_delete.pack(anchor="w", padx=20, pady=(16, 0))

    def show_add_custom_form(self):
        self.clear_right()

        btn_add_custom = ctk.CTkButton(self.pnl_right, text="+ Add Custom Exercise",
                                       command=self.show_add_custom_form)
        btn_add_custom.pack(anchor="e", padx=20, pady=(16, 0))

        pnl_form = ctk.CTkFrame(self.pnl_right, fg_color="transparent")
        pnl_form.pack(fill="both", padx=20, pady=20)

        lbl_title = ctk.CTkLabel(pnl_form, text="New Custom Exercise",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        lbl_title.pack(anchor="w", pady=(0, 16))

        ctk.CTkLabel(pnl_form, text="Exercise Name", anchor="w").pack(anchor="w", pady=(0, 4))
        self.ent_custom_name = ctk.CTkEntry(pnl_form, placeholder_text="e.g. Cable Crunch")
        self.ent_custom_name.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(pnl_form, text="Target Muscle", anchor="w").pack(anchor="w", pady=(0, 4))
        muscle_options = MUSCLES[1:]
        self.opt_custom_muscle = ctk.CTkOptionMenu(pnl_form, values=muscle_options)
        self.opt_custom_muscle.pack(fill="x", pady=(0, 16))

        self.lbl_custom_msg = ctk.CTkLabel(pnl_form, text="")
        self.lbl_custom_msg.pack()

        btn_save = ctk.CTkButton(pnl_form, text="Save Custom Exercise", command=self.handle_save_custom)
        btn_save.pack(fill="x", pady=(8, 0))

    def handle_save_custom(self):
        name = self.ent_custom_name.get().strip()
        if name == "":
            self.lbl_custom_msg.configure(text="Name is required", text_color="red")
            return

        muscle = self.opt_custom_muscle.get()
        new_ex = CustomExercise.create_new(name, muscle, "", self.user_id)

        existing = data_service.load_custom_exercises(self.user_id)
        existing.append(new_ex)
        data_service.save_custom_exercises(self.user_id, existing)

        self.refresh_exercise_list()
        self.lbl_custom_msg.configure(text="Saved!", text_color="green")

    def handle_delete_custom(self, exercise):
        existing = data_service.load_custom_exercises(self.user_id)
        updated = []
        for ex in existing:
            if ex.exercise_id != exercise.exercise_id:
                updated.append(ex)

        data_service.save_custom_exercises(self.user_id, updated)
        self.refresh_exercise_list()
        self.clear_right()

        btn_add_custom = ctk.CTkButton(self.pnl_right, text="+ Add Custom Exercise",
                                       command=self.show_add_custom_form)
        btn_add_custom.pack(anchor="e", padx=20, pady=(16, 0))

        lbl = ctk.CTkLabel(self.pnl_right, text="Exercise deleted", text_color="gray")
        lbl.pack(expand=True)

    def clear_right(self):
        for w in self.pnl_right.winfo_children():
            w.destroy()
