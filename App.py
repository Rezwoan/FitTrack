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

        self.show_auth()

    def show_auth(self):
        """Clears the window and displays the auth (login/signup) page."""
        for widget in self.winfo_children():
            widget.destroy()
        AuthPage(self)

