import customtkinter as ctk
from PIL import Image, ImageDraw
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from services import auth_service


class AuthPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.app = parent
        self.current_tab = "login"

        # main card in the center
        self.pnl_card = ctk.CTkFrame(self)
        self.pnl_card.place(relx=0.5, rely=0.5, anchor="center")
        self.pnl_card.grid_columnconfigure(0, weight=1)

        self.show_logo()
        self.show_tabs()

        # this frame will hold the form fields
        self.pnl_form = ctk.CTkFrame(self.pnl_card, fg_color="transparent")
        self.pnl_form.grid(row=2, column=0, sticky="ew", padx=40, pady=(10, 10))
        self.pnl_form.grid_columnconfigure(0, weight=1)

        # error label at the bottom of the card
        self.lbl_error = ctk.CTkLabel(self.pnl_card, text="", text_color="red")
        self.lbl_error.grid(row=3, column=0, pady=(0, 20))

        # show login by default
        self.show_login_form()

    def show_logo(self):
        logo_path = os.path.join(os.path.dirname(__file__), "..", "images", "logo.png")

        img = Image.open(logo_path).convert("RGBA")
        img = img.resize((150, 150), Image.LANCZOS)

        # make a rounded mask
        mask = Image.new("L", (150, 150), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, 150, 150), radius=28, fill=255)
        img.putalpha(mask)

        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
        self.lbl_logo = ctk.CTkLabel(self.pnl_card, image=ctk_img, text="")
        self.lbl_logo.grid(row=0, column=0, pady=(36, 12))

    def show_tabs(self):
        # tab buttons row
        self.pnl_tabs = ctk.CTkFrame(self.pnl_card, fg_color="transparent")
        self.pnl_tabs.grid(row=1, column=0, sticky="ew", padx=40, pady=(0, 4))
        self.pnl_tabs.grid_columnconfigure((0, 1), weight=1)

        self.btn_login_tab = ctk.CTkButton(self.pnl_tabs, text="Login", height=36,
                                           command=self.show_login_form)
        self.btn_login_tab.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self.btn_signup_tab = ctk.CTkButton(self.pnl_tabs, text="Sign Up", height=36,
                                            command=self.show_signup_form)
        self.btn_signup_tab.grid(row=0, column=1, sticky="ew", padx=(4, 0))

        self.update_tab_colors()

    def update_tab_colors(self):
        # dim the inactive tab button
        if self.current_tab == "login":
            self.btn_login_tab.configure(fg_color=("gray30", "gray30"))
            self.btn_signup_tab.configure(fg_color="transparent")
        else:
            self.btn_signup_tab.configure(fg_color=("gray30", "gray30"))
            self.btn_login_tab.configure(fg_color="transparent")

    def clear_form(self):
        # remove all widgets from the form area
        for w in self.pnl_form.winfo_children():
            w.destroy()
        self.lbl_error.configure(text="")

    def show_login_form(self):
        self.current_tab = "login"
        self.update_tab_colors()
        self.clear_form()

        self.lbl_email = ctk.CTkLabel(self.pnl_form, text="Email", anchor="w")
        self.lbl_email.grid(row=0, column=0, sticky="w", pady=(16, 4))

        self.ent_login_email = ctk.CTkEntry(self.pnl_form, placeholder_text="you@example.com", width=360)
        self.ent_login_email.grid(row=1, column=0, sticky="ew")

        self.lbl_password = ctk.CTkLabel(self.pnl_form, text="Password", anchor="w")
        self.lbl_password.grid(row=2, column=0, sticky="w", pady=(16, 4))

        self.ent_login_password = ctk.CTkEntry(self.pnl_form, placeholder_text="Password", show="•", width=360)
        self.ent_login_password.grid(row=3, column=0, sticky="ew")

        self.btn_login = ctk.CTkButton(self.pnl_form, text="Login", command=self.handle_login)
        self.btn_login.grid(row=4, column=0, sticky="ew", pady=(24, 0))

    def show_signup_form(self):
        self.current_tab = "signup"
        self.update_tab_colors()
        self.clear_form()

        self.lbl_name = ctk.CTkLabel(self.pnl_form, text="Full Name", anchor="w")
        self.lbl_name.grid(row=0, column=0, sticky="w", pady=(16, 4))

        self.ent_signup_name = ctk.CTkEntry(self.pnl_form, placeholder_text="John Doe", width=360)
        self.ent_signup_name.grid(row=1, column=0, sticky="ew")

        self.lbl_email = ctk.CTkLabel(self.pnl_form, text="Email", anchor="w")
        self.lbl_email.grid(row=2, column=0, sticky="w", pady=(16, 4))

        self.ent_signup_email = ctk.CTkEntry(self.pnl_form, placeholder_text="you@example.com", width=360)
        self.ent_signup_email.grid(row=3, column=0, sticky="ew")

        self.lbl_password = ctk.CTkLabel(self.pnl_form, text="Password", anchor="w")
        self.lbl_password.grid(row=4, column=0, sticky="w", pady=(16, 4))

        self.ent_signup_password = ctk.CTkEntry(self.pnl_form, placeholder_text="Password", show="•", width=360)
        self.ent_signup_password.grid(row=5, column=0, sticky="ew")

        self.btn_signup = ctk.CTkButton(self.pnl_form, text="Sign Up", command=self.handle_signup)
        self.btn_signup.grid(row=6, column=0, sticky="ew", pady=(24, 0))

    def handle_login(self):
        email = self.ent_login_email.get().strip()
        password = self.ent_login_password.get()

        if email == "" or password == "":
            self.lbl_error.configure(text="Please fill in all fields")
            return

        success, result = auth_service.login(email, password)
        if success:
            self.app.on_login_success(result)
        else:
            self.lbl_error.configure(text=result)

    def handle_signup(self):
        name = self.ent_signup_name.get().strip()
        email = self.ent_signup_email.get().strip()
        password = self.ent_signup_password.get()

        if name == "" or email == "" or password == "":
            self.lbl_error.configure(text="Please fill in all fields")
            return

        if len(password) < 6:
            self.lbl_error.configure(text="Password must be at least 6 characters")
            return

        success, result = auth_service.signup(name, email, password)
        if success:
            self.app.on_login_success(result)
        else:
            self.lbl_error.configure(text=result)
