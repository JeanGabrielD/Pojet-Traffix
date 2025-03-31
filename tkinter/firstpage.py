import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MainWindow")
        self.geometry("700x500")
        self.resizable(False, False)

        logo_label = ctk.CTkLabel(self, text="LOGO", font=("Helvetica", 20, "italic"), text_color="gray")
        logo_label.place(x=20, y=20)

        title_label = ctk.CTkLabel(self, text="Prédiction de la congestion routière", font=("Helvetica", 32, "bold"))
        title_label.pack(pady=80)

        start_button = ctk.CTkButton(self, text="START", width=100, height=40, fg_color="#1C3A6B", font=("Helvetica", 18))
        start_button.pack(pady=20)

        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.pack(pady=20)

        fr_image = Image.open("france_flag.png").resize((50, 50))
        fr_icon = ImageTk.PhotoImage(fr_image)

        en_image = Image.open("uk_flag.png").resize((50, 50))
        en_icon = ImageTk.PhotoImage(en_image)

        self.fr_button = ctk.CTkButton(lang_frame, image=fr_icon, text="FRANÇAIS", compound="top", width=80, height=80)
        self.fr_button.grid(row=0, column=0, padx=20)

        self.en_button = ctk.CTkButton(lang_frame, image=en_icon, text="ENGLISH", compound="top", width=80, height=80)
        self.en_button.grid(row=0, column=1, padx=20)

        self.fr_icon = fr_icon
        self.en_icon = en_icon

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
