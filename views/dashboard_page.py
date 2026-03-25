import customtkinter as ctk


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, user_data):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.app = parent
        self.user_data = user_data

        self.pnl_sidebar = ctk.CTkFrame(self, width=200)
        self.pnl_sidebar.pack(side="left", fill="y", padx=(10, 0), pady=10)
        self.pnl_sidebar.pack_propagate(False)

        self.pnl_content = ctk.CTkFrame(self, fg_color="transparent")
        self.pnl_content.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.build_sidebar()
        self.show_home()

    def build_sidebar(self):
        lbl_app = ctk.CTkLabel(self.pnl_sidebar, text="FitTrack", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_app.pack(pady=(20, 4))

        lbl_user = ctk.CTkLabel(self.pnl_sidebar, text=self.user_data["name"], text_color="gray")
        lbl_user.pack(pady=(0, 20))

        ctk.CTkFrame(self.pnl_sidebar, height=1, fg_color="gray40").pack(fill="x", padx=16, pady=(0, 16))

        btn_home = ctk.CTkButton(self.pnl_sidebar, text="Home", anchor="w",
                                 command=self.show_home, fg_color="transparent")
        btn_home.pack(fill="x", padx=10, pady=4)

        btn_plans = ctk.CTkButton(self.pnl_sidebar, text="Workout Plans", anchor="w",
                                  command=self.show_plans, fg_color="transparent")
        btn_plans.pack(fill="x", padx=10, pady=4)

        btn_exercises = ctk.CTkButton(self.pnl_sidebar, text="Exercises", anchor="w",
                                      command=self.show_exercises, fg_color="transparent")
        btn_exercises.pack(fill="x", padx=10, pady=4)

        btn_history = ctk.CTkButton(self.pnl_sidebar, text="History", anchor="w",
                                    command=self.show_history, fg_color="transparent")
        btn_history.pack(fill="x", padx=10, pady=4)

        btn_profile = ctk.CTkButton(self.pnl_sidebar, text="Profile", anchor="w",
                                    command=self.show_profile, fg_color="transparent")
        btn_profile.pack(fill="x", padx=10, pady=4)

        btn_logout = ctk.CTkButton(self.pnl_sidebar, text="Logout", anchor="w",
                                   command=self.handle_logout, fg_color="transparent")
        btn_logout.pack(fill="x", padx=10, pady=(20, 10))

    def clear_content(self):
        for w in self.pnl_content.winfo_children():
            w.destroy()

    def show_home(self):
        from views.pages.home_page import HomePage
        self.clear_content()
        HomePage(self.pnl_content, self.user_data, self.app)

    def show_plans(self):
        from views.pages.plans_page import PlansPage
        self.clear_content()
        PlansPage(self.pnl_content, self.user_data)

    def show_exercises(self):
        from views.pages.exercises_page import ExercisesPage
        self.clear_content()
        ExercisesPage(self.pnl_content, self.user_data)

    def show_history(self):
        from views.pages.history_page import HistoryPage
        self.clear_content()
        HistoryPage(self.pnl_content, self.user_data)

    def show_profile(self):
        from views.pages.profile_page import ProfilePage
        self.clear_content()
        ProfilePage(self.pnl_content, self.user_data)

    def handle_logout(self):
        self.app.current_user = None
        self.app.show_auth()
