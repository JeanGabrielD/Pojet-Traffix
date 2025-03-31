import customtkinter as ctk
import tkinter
from PIL import Image
from page1 import Page1
from page2 import Page2
from page3 import Page3

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.current_language = "fr"

        # Charger les images
        self.image_drapeau_en = ctk.CTkImage(light_image=Image.open("drapeau-anglais.png"), size=(100, 100))
        self.image_drapeau_fr = ctk.CTkImage(light_image=Image.open("drapeau-francais.png"), size=(100, 100))
        self.image_logo = ctk.CTkImage(light_image=Image.open("logo_LSTM.png"), size=(250, 250))

        self.translations = {
            "fr": {"title": "Prédiction de la\ncongestion routière", "start": "Démarrer"},
            "en": {"title": "Traffic Congestion\nPrediction", "start": "Start"},
        }

        self.create_widgets()

    def create_widgets(self):
        # Logo
        label_logo = ctk.CTkLabel(self.root, image=self.image_logo, text="")
        label_logo.place(relx=0.15, rely=0.1, anchor=tkinter.CENTER)

        # Titre principal
        frame_titre = ctk.CTkFrame(self.root, fg_color="transparent", width=400, height=150)
        frame_titre.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.label_titre = ctk.CTkLabel(frame_titre, text=self.translations[self.current_language]["title"], font=("Arial", 60, "bold"), text_color="black")
        self.label_titre.pack(expand=True, fill="both")

        # Bouton START
        self.button_start = ctk.CTkButton(self.root, text=self.translations[self.current_language]["start"], font=("Arial", 30, "bold"), fg_color="#1C3A6B", width=175, height=75, corner_radius=25, command=self.open_page1)
        self.button_start.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        # Sélecteurs de langue
        self.create_language_buttons()

    def create_language_buttons(self):
        frame_en = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_en.place(relx=0.56, rely=0.8, anchor=tkinter.CENTER)
        image_label_en = ctk.CTkLabel(frame_en, image=self.image_drapeau_en, text="")
        image_label_en.pack()
        image_label_en.bind("<Button-1>", lambda e: self.update_language("en"))

        text_label_en = ctk.CTkLabel(frame_en, text="English", font=("Arial", 20), text_color="black")
        text_label_en.pack()

        frame_fr = ctk.CTkFrame(self.root, fg_color="transparent")
        frame_fr.place(relx=0.44, rely=0.8, anchor=tkinter.CENTER)
        image_label_fr = ctk.CTkLabel(frame_fr, image=self.image_drapeau_fr, text="")
        image_label_fr.pack()
        image_label_fr.bind("<Button-1>", lambda e: self.update_language("fr"))

        text_label_fr = ctk.CTkLabel(frame_fr, text="Français", font=("Arial", 20), text_color="black")
        text_label_fr.pack()

    def update_language(self, lang):
        self.current_language = lang
        self.label_titre.configure(text=self.translations[lang]["title"])
        self.button_start.configure(text=self.translations[lang]["start"])

    def open_page1(self):
        self.clear_window()
        Page1(self.root, language=self.current_language)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
