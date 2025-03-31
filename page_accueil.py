import customtkinter
import tkinter
from PIL import Image

customtkinter.set_appearance_mode("system")

app = customtkinter.CTk()
app.title("Traffix")
app.geometry("1200x700")
app.configure(fg_color="#E7E7E7")

# Obtenir les images
image_drapeau_en = Image.open("drapeau-anglais.png")
image_drapeau_fr = Image.open("drapeau-francais.png")
image_logo = Image.open("logo_LSTM.png")

# Convertir les images
image_drapeau_en = customtkinter.CTkImage(light_image=image_drapeau_en, dark_image=image_drapeau_en, size=(100, 100))
image_drapeau_fr = customtkinter.CTkImage(light_image=image_drapeau_fr, dark_image=image_drapeau_fr, size=(100, 100))
image_logo = customtkinter.CTkImage(light_image=image_logo, dark_image=image_logo, size=(250, 250))

translations = {
    "fr": {
        "title": "Prédiction de la\ncongestion routière",
    },
    "en": {
        "title": "Traffic Congestion\nPrediction",
    },
}

# Variable globale pour la langue actuelle
current_language = "fr"

def update_language(lang):
    global current_language
    current_language = lang
    label_titre.configure(text=translations[lang]["title"])

# Logo
label_logo = customtkinter.CTkLabel(app, image=image_logo, text="")
label_logo.place(relx=0.15, rely=0.1, anchor=tkinter.CENTER)

# Titre principal
frame_titre = customtkinter.CTkFrame(app, fg_color="transparent", width=400, height=150)
frame_titre.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
label_titre = customtkinter.CTkLabel(frame_titre, text="Prédiction de la\ncongestion routière", font=("Arial", 70, "bold"), text_color="black", anchor=tkinter.CENTER)
label_titre.pack(expand=True, fill="both")

# Bouton START
def on_click_start():
    print("Click start")

button_start = customtkinter.CTkButton(app, text="START", font=("Arial", 40, "bold"), fg_color="#014F86", width=200, height=100, corner_radius=25, command=on_click_start)
button_start.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

# Drapeau anglais
def on_click_en(event):
    update_language("en")
    print("Click anglais")

frame_en = customtkinter.CTkFrame(app, fg_color="transparent")
frame_en.place(relx=0.55, rely=0.8, anchor=tkinter.CENTER)

image_label_en = customtkinter.CTkLabel(frame_en, image=image_drapeau_en, text="")
image_label_en.pack()
image_label_en.bind("<Button-1>", on_click_en)

text_label_en = customtkinter.CTkLabel(frame_en, text="English", font=("Arial", 20), text_color="black")
text_label_en.pack()  

# Drapeau français
def on_click_fr(event):
    update_language("fr")
    print("Click français")

frame_fr = customtkinter.CTkFrame(app, fg_color="transparent")
frame_fr.place(relx=0.45, rely=0.8, anchor=tkinter.CENTER)

image_label_fr = customtkinter.CTkLabel(frame_fr, image=image_drapeau_fr, text="")
image_label_fr.pack()
image_label_fr.bind("<Button-1>", on_click_fr)

text_label_fr = customtkinter.CTkLabel(frame_fr, text="Français", font=("Arial", 20), text_color="black")
text_label_fr.pack()

app.mainloop()
