import customtkinter as ctk
import os
import sys
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from services import data_service
from models.workout import Workout, PlannedExercise
from models.set import Set


class PlansPage(ctk.CTkFrame):

    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.user_data = user_data
        self.user_id = user_data["user_id"]
        self.plan_exercises_in_form = []
        self.all_exercises = []

        self.build_page()

    def build_page(self):
        lbl_title = ctk.CTkLabel(self, text="Workout Plans", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_title.pack(anchor="w", pady=(0, 12))

        pnl_columns = ctk.CTkFrame(self, fg_color="transparent")
        pnl_columns.pack(fill="both", expand=True)
        pnl_columns.grid_columnconfigure(0, weight=1)
        pnl_columns.grid_columnconfigure(1, weight=2)
        pnl_columns.grid_rowconfigure(0, weight=1)

        self.build_left_panel(pnl_columns)
        self.build_right_panel(pnl_columns)

    def build_left_panel(self, parent):
        self.pnl_left = ctk.CTkFrame(parent)
        self.pnl_left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        btn_new = ctk.CTkButton(self.pnl_left, text="+ New Plan", command=self.show_create_form)
        btn_new.pack(fill="x", padx=10, pady=(10, 6))

        self.pnl_plan_list = ctk.CTkScrollableFrame(self.pnl_left)
        self.pnl_plan_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.refresh_plan_list()

    def refresh_plan_list(self):
        for w in self.pnl_plan_list.winfo_children():
            w.destroy()

        workouts = data_service.load_workouts(self.user_id)
        if len(workouts) == 0:
            lbl = ctk.CTkLabel(self.pnl_plan_list, text="No plans yet", text_color="gray")
            lbl.pack(pady=20)
        else:
            for workout in workouts:
                btn = ctk.CTkButton(self.pnl_plan_list, text=workout.name, anchor="w",
                                    fg_color="transparent",
                                    command=lambda w=workout: self.show_plan_details(w))
                btn.pack(fill="x", pady=2)

    def build_right_panel(self, parent):
        self.pnl_right = ctk.CTkFrame(parent)
        self.pnl_right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        lbl_hint = ctk.CTkLabel(self.pnl_right, text="Select a plan or create a new one", text_color="gray")
        lbl_hint.pack(expand=True)

    def clear_right(self):
        for w in self.pnl_right.winfo_children():
            w.destroy()

    def show_plan_details(self, workout):
        self.clear_right()

        lbl_name = ctk.CTkLabel(self.pnl_right, text=workout.name, font=ctk.CTkFont(size=18, weight="bold"))
        lbl_name.pack(anchor="w", padx=20, pady=(20, 10))

        pnl_btns = ctk.CTkFrame(self.pnl_right, fg_color="transparent")
        pnl_btns.pack(anchor="w", padx=20, pady=(0, 12))

        btn_edit = ctk.CTkButton(pnl_btns, text="Edit", command=lambda: self.show_edit_form(workout))
        btn_edit.pack(side="left", padx=(0, 8))

        btn_delete = ctk.CTkButton(pnl_btns, text="Delete", fg_color="transparent", border_width=1,
                                   command=lambda: self.handle_delete(workout))
        btn_delete.pack(side="left")

        pnl_exercises = ctk.CTkScrollableFrame(self.pnl_right)
        pnl_exercises.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        if len(workout.exercises) == 0:
            lbl = ctk.CTkLabel(pnl_exercises, text="No exercises added", text_color="gray")
            lbl.pack(pady=20)
        else:
            for ex in workout.exercises:
                lbl_ex = ctk.CTkLabel(pnl_exercises, text=ex.exercise_name, anchor="w",
                                      font=ctk.CTkFont(weight="bold"))
                lbl_ex.pack(anchor="w", pady=(10, 2))
                for i, s in enumerate(ex.sets):
                    lbl_set = ctk.CTkLabel(pnl_exercises,
                                           text=f"  Set {i+1}: {s.reps} reps @ {s.weight} kg",
                                           anchor="w")
                    lbl_set.pack(anchor="w")

    def show_create_form(self):
        self.plan_exercises_in_form = []
        self.show_plan_form(existing_workout=None)

    def show_edit_form(self, workout):
        self.plan_exercises_in_form = list(workout.exercises)
        self.show_plan_form(existing_workout=workout)

    def show_plan_form(self, existing_workout):
        self.clear_right()

        self.all_exercises = data_service.load_built_in_exercises()
        custom = data_service.load_custom_exercises(self.user_id)
        for c in custom:
            self.all_exercises.append(c)

        pnl_form = ctk.CTkScrollableFrame(self.pnl_right)
        pnl_form.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(pnl_form, text="Plan Name", anchor="w").pack(anchor="w", pady=(0, 4))
        self.ent_plan_name = ctk.CTkEntry(pnl_form, placeholder_text="e.g. Push Day")
        self.ent_plan_name.pack(fill="x", pady=(0, 16))
        if existing_workout is not None:
            self.ent_plan_name.insert(0, existing_workout.name)

        ctk.CTkLabel(pnl_form, text="Exercises in this plan", anchor="w").pack(anchor="w", pady=(0, 4))
        self.pnl_exercise_list = ctk.CTkFrame(pnl_form, fg_color="transparent")
        self.pnl_exercise_list.pack(fill="x", pady=(0, 12))
        self.refresh_exercise_list_in_form()

        ctk.CTkLabel(pnl_form, text="Add Exercise", anchor="w", text_color="gray").pack(anchor="w", pady=(8, 4))

        exercise_names = []
        for ex in self.all_exercises:
            exercise_names.append(ex.name)

        if len(exercise_names) == 0:
            exercise_names = ["No exercises available"]

        self.opt_exercise = ctk.CTkOptionMenu(pnl_form, values=exercise_names)
        self.opt_exercise.pack(fill="x", pady=(0, 8))

        pnl_sets_row = ctk.CTkFrame(pnl_form, fg_color="transparent")
        pnl_sets_row.pack(fill="x", pady=(0, 4))
        pnl_sets_row.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(pnl_sets_row, text="Sets", anchor="w").grid(row=0, column=0, sticky="w", padx=(0, 6))
        ctk.CTkLabel(pnl_sets_row, text="Reps", anchor="w").grid(row=0, column=1, sticky="w", padx=(0, 6))
        ctk.CTkLabel(pnl_sets_row, text="Weight (kg)", anchor="w").grid(row=0, column=2, sticky="w")

        self.ent_sets = ctk.CTkEntry(pnl_sets_row, placeholder_text="3")
        self.ent_sets.grid(row=1, column=0, sticky="ew", padx=(0, 6))

        self.ent_reps = ctk.CTkEntry(pnl_sets_row, placeholder_text="10")
        self.ent_reps.grid(row=1, column=1, sticky="ew", padx=(0, 6))

        self.ent_weight_per_set = ctk.CTkEntry(pnl_sets_row, placeholder_text="0")
        self.ent_weight_per_set.grid(row=1, column=2, sticky="ew")

        self.lbl_form_error = ctk.CTkLabel(pnl_form, text="")
        self.lbl_form_error.pack(pady=(8, 0))

        btn_add_ex = ctk.CTkButton(pnl_form, text="Add Exercise to Plan", command=self.handle_add_exercise)
        btn_add_ex.pack(fill="x", pady=(4, 0))

        btn_save_plan = ctk.CTkButton(pnl_form, text="Save Plan",
                                      command=lambda: self.handle_save_plan(existing_workout))
        btn_save_plan.pack(fill="x", pady=(8, 4))

    def refresh_exercise_list_in_form(self):
        for w in self.pnl_exercise_list.winfo_children():
            w.destroy()

        if len(self.plan_exercises_in_form) == 0:
            lbl = ctk.CTkLabel(self.pnl_exercise_list, text="No exercises added yet", text_color="gray")
            lbl.pack()
        else:
            for i, ex in enumerate(self.plan_exercises_in_form):
                pnl_row = ctk.CTkFrame(self.pnl_exercise_list, fg_color="transparent")
                pnl_row.pack(fill="x", pady=2)

                lbl_ex = ctk.CTkLabel(pnl_row, text=f"{ex.exercise_name} ({len(ex.sets)} sets)", anchor="w")
                lbl_ex.pack(side="left", expand=True)

                btn_remove = ctk.CTkButton(pnl_row, text="Remove", width=70, height=24,
                                           fg_color="transparent", border_width=1,
                                           command=lambda idx=i: self.handle_remove_exercise(idx))
                btn_remove.pack(side="right")

    def handle_add_exercise(self):
        selected_name = self.opt_exercise.get()
        sets_str = self.ent_sets.get().strip()
        reps_str = self.ent_reps.get().strip()
        weight_str = self.ent_weight_per_set.get().strip()

        if sets_str == "" or reps_str == "":
            self.lbl_form_error.configure(text="Sets and reps are required", text_color="red")
            return

        num_sets = int(sets_str)
        reps = int(reps_str)
        weight = float(weight_str) if weight_str != "" else 0

        selected_exercise = None
        for ex in self.all_exercises:
            if ex.name == selected_name:
                selected_exercise = ex
                break

        if selected_exercise is None:
            return

        planned_ex = PlannedExercise(selected_exercise.exercise_id, selected_exercise.name)
        for _ in range(num_sets):
            planned_ex.add_set(reps, weight)

        self.plan_exercises_in_form.append(planned_ex)
        self.lbl_form_error.configure(text="")
        self.refresh_exercise_list_in_form()

    def handle_remove_exercise(self, index):
        self.plan_exercises_in_form.pop(index)
        self.refresh_exercise_list_in_form()

    def handle_save_plan(self, existing_workout):
        name = self.ent_plan_name.get().strip()
        if name == "":
            self.lbl_form_error.configure(text="Plan name is required", text_color="red")
            return

        if len(self.plan_exercises_in_form) == 0:
            self.lbl_form_error.configure(text="Add at least one exercise", text_color="red")
            return

        workouts = data_service.load_workouts(self.user_id)

        if existing_workout is not None:
            for w in workouts:
                if w.workout_id == existing_workout.workout_id:
                    w.name = name
                    w.exercises = self.plan_exercises_in_form
                    break
        else:
            new_workout = Workout.create_new(name)
            new_workout.exercises = self.plan_exercises_in_form
            workouts.append(new_workout)

        data_service.save_workouts(self.user_id, workouts)
        self.plan_exercises_in_form = []
        self.refresh_plan_list()
        self.clear_right()

        lbl_saved = ctk.CTkLabel(self.pnl_right, text="Plan saved!", text_color="green")
        lbl_saved.pack(expand=True)

    def handle_delete(self, workout):
        workouts = data_service.load_workouts(self.user_id)
        updated = []
        for w in workouts:
            if w.workout_id != workout.workout_id:
                updated.append(w)

        data_service.save_workouts(self.user_id, updated)
        self.refresh_plan_list()
        self.clear_right()

        lbl = ctk.CTkLabel(self.pnl_right, text="Plan deleted", text_color="gray")
        lbl.pack(expand=True)
