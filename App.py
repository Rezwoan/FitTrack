import customtkinter as ctk
from views.auth_page import AuthPage


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("FitTrack")
        self.geometry("1200x800")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_user = None

        self.show_auth()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_auth(self):
        """Clears the window and displays the auth (login/signup) page."""
        self.clear_window()
        AuthPage(self)

    def on_login_success(self, user_data):
        # called from auth page once login or signup works
        self.current_user = user_data

        if user_data["profile_complete"] == False:
            self.show_profile_setup()
        else:
            self.show_dashboard()

    def show_profile_setup(self):
        # TODO: show profile setup page
        self.clear_window()
        lbl = ctk.CTkLabel(self, text=f"Welcome {self.current_user['name']}! Please set up your profile.")
        lbl.place(relx=0.5, rely=0.5, anchor="center")

    def show_dashboard(self):
        # TODO: show main dashboard
        self.clear_window()
        lbl = ctk.CTkLabel(self, text=f"Dashboard — logged in as {self.current_user['name']}")
        lbl.place(relx=0.5, rely=0.5, anchor="center")
