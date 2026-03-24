import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FitTrack")
        self.geometry("1200x800")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        label = ctk.CTkLabel(
            self,
            text="FitTrack",
            font=ctk.CTkFont(size=48, weight="bold"),
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
