import customtkinter as ctk
import tkinter as tk
from customtkinter import CTkImage
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES
from tkinter import filedialog
import os
from tkinter import messagebox
from cleandatasets import *

selected_algorithm = ""
name_file = ""

class Page1:
    def __init__(self, root, language):
        self.root = root
        self.language = language
        self.columns_dict = {
            "CSV": ["vehicle_id", "timestamp", "speed", "route_id", "trip_id", "latitude", "longitude", "trip_headsign"],
            "GPX": ["latitude", "longitude", "elevation", "time"]
        }

        self.file_dict = {
            "DPX": ["id-veh", "local_X", "local_Y", "latitude", "longitude"],
            "GPX": ["id-veh", "latitude", "longitude"]
        }

        self.translations = {
            "fr": {
                "preprocessing": "PRÉTRAITEMENT",
                "choose_algo": "Choisir un algorithme :",
                "choose_file": "Choisir un fichier :",
                "select_columns": "Sélectionner les colonnes :",
                "select_sequence": "Taille des séquences :",
                "drop_file": "Déposez un fichier ici (csv ou gpx)",
                "simulate": "Simuler",
                "next": "Suivant",
                "back": "Retour",
                "csv_file": "Fichiers CSV",
                "gpx_file": "Fichiers GPX",
                "error_title": "Traffix - Erreur",
                "invalid_file_type": "Type de fichier incorrect, veuillez choisir un fichier .gpx ou .csv",
                "menu": [
                    ("PRÉTRAITEMENT", self.open_page1, "edit.png"),
                    ("ENTRAÎNEMENT", self.open_page2, "params.png"),
                    ("RESULTAT", self.open_page3, "result.png"),
                    ("VISUALISATION DES\nDONNÉES", self.open_page4, "visu.png")
                ],
                "infos": {
                    "CSV": [
                        "ID unique du véhicule.",
                        "Date et heure.",
                        "Vitesse du véhicule.",
                        "ID de la route.",
                        "ID du trajet.",
                        "Latitude GPS du véhicule.",
                        "Longitude GPS du véhicule.",
                        "Destination du trajet."
                    ],
                    "GPX": [
                        "Latitude GPS du vehicle",
                        "Longitude GPS du vehicle",
                        "Altitude du vehicle",
                        "Temps de la mesure",
                    ]
                }
            },
            "en": {
                "preprocessing": "PREPROCESSING",
                "choose_algo": "Choose an algorithm:",
                "choose_file": "Choose a file :",
                "select_columns": "Sequences length:",
                "select_sequence": "Sequences length:",
                "drop_file": "Drop a file here",
                "simulate": "Simulate",
                "back": "Back",
                "next": "next",
                "csv_file": "CSV Files",
                "gpx_file": "GPX Files",
                "error_title": "Traffix - Error",
                "invalid_file_type": "Wrong file type, please select a .gpx or .csv file",
                "menu": [
                    ("PREPROCESSING", self.open_page1, "edit.png"),
                    ("TRAINING", self.open_page2, "params.png"),
                    ("RESULT", self.open_page3, "result.png"),
                    ("DATA VISUALIZATION", self.open_page4, "visu.png")
                ],
                "infos": {
                    "CSV": [
                        "Unique vehicle ID.",
                        "Date and hour.",
                        "Speed of vehicle.",
                        "Route ID.",
                        "Trip ID.",
                        "Vehicle GPS latitude.",
                        "Vehicle GPS longitude.",
                        "Trip destination."
                    ],
                    "GPX": [
                        "Vehicle GPS latitude.",
                        "Vehicle GPS longitude.",
                        "Vehicle altitude.",
                        "Date and hour."
                    ]
                }
            }
        }
        self.create_sidebar()
        self.create_main_frame()
      

    # Barre latérale (Menu de navigation)
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.root, width=300, corner_radius=0, fg_color="#1C3A6B")
        sidebar.pack(side="left", fill="y")

        # Logo
        logo = ctk.CTkImage(light_image=Image.open("logo_LSTM.png"), size=(200, 200))
        label_logo = ctk.CTkLabel(sidebar, image=logo, text="")
        label_logo.pack(pady=(10, 20))

        # Boutons de navigation
        for text, command, icon_path in self.translations[self.language]["menu"]:
            icon = CTkImage(light_image=Image.open(icon_path), size=(20, 20))
            button = ctk.CTkButton(
                sidebar, text=text, width=200, height=40, anchor="w",
                corner_radius=10, font=("Arial", 16, "bold"), fg_color="#1C3A6B",
                command=command, image=icon
            )
            button.pack(pady=15, padx=10)


    def toggle_variable_size(self):
        if self.variable_size_checkbox.get():
            self.fixed_size_checkbox.deselect()
            self.variable_size_entry.pack(pady=5)
        else:
            self.variable_size_entry.pack_forget()

    def toggle_fixed_size(self):
        if self.fixed_size_checkbox.get():
            self.variable_size_checkbox.deselect()
            self.variable_size_entry.pack_forget()
    # Contenu principal
    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Titre principal
        title_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["preprocessing"], font=("Arial", 28, "bold"), text_color="#ff5733")
        title_label.pack(padx=20, pady=20, anchor="center")
       
        # Sélection de l'algorithme
        algo_frame = ctk.CTkFrame(main_frame, fg_color="white", width=500)
        algo_frame.pack(fill="x", padx=20, pady=20)
        self.lbl = ctk.CTkLabel(algo_frame, text=self.translations[self.language]["choose_file"], font=("Arial", 16, "bold"), text_color="black").pack(pady=5, side="left")
        


        self.algo_dropdown = ctk.CTkComboBox(algo_frame, values=list(self.columns_dict.keys()), command=self.update_checkboxes)
        self.algo_dropdown.pack(padx=(10, 0), pady=5, side="left")
     


        # Sélection des colonnes
        ctk.CTkLabel(main_frame, text=self.translations[self.language]["select_columns"], font=("Arial", 16, "bold"), text_color="black").pack(padx=20, pady=5, anchor="w")

        self.checkbox_frame = ctk.CTkFrame(main_frame, fg_color="white")
        self.checkbox_frame.pack(padx=20, pady=10, anchor="w")

        # Icône info
        image = Image.open("info.png").resize((15, 15))
        self.info_image = ImageTk.PhotoImage(image)

        # Initialisation des checkboxes
        self.update_checkboxes()

        # Drag & Drop
        self.create_drag_drop(main_frame)

       

        # Boutons bas de page
        ctk.CTkButton(main_frame, text=self.translations[self.language]["next"], width=100, fg_color="#1C3A6B", command=self.open_page2).place(relx=0.9, rely=0.95, anchor="center")
        ctk.CTkButton(main_frame, text=self.translations[self.language]["back"], width=100, fg_color="#1C3A6B", command=self.open_main_window).place(relx=0.75, rely=0.95, anchor="center")


      
    # Mise à jour des checkboxes selon l'algorithme sélectionné
    def update_checkboxes(self, event=None):
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()

        selected_algo = self.algo_dropdown.get()
        columns = self.columns_dict.get(selected_algo, [])

        print(selected_algo)
        for i, column in enumerate(columns):
            row, column_index = divmod(i, 2)

            checkbox = ctk.CTkCheckBox(self.checkbox_frame, text=column, onvalue=column, offvalue="", font=("Arial", 12), text_color="black")
            info_icon = ctk.CTkLabel(self.checkbox_frame, image=self.info_image, text="")

            if column_index == 1:
                checkbox.grid(row=row, column=column_index+2, pady=5, padx=(200,30), sticky="w")
                info_icon.grid(row=row, column=column_index+4, padx=5, pady=5, sticky="w")
            else:
                checkbox.grid(row=row, column=column_index, pady=5, padx=10, sticky="w")
                info_icon.grid(row=row, column=column_index+1, padx=5, pady=5, sticky="w")
            info_icon.bind("<Enter>", lambda e, text=self.translations[self.language]["infos"].get(selected_algo, [])[i]: self.show_tooltip(e, text))
            info_icon.bind("<Leave>", self.hide_tooltip)
        
      
        """ size_label = ctk.CTkLabel(self.checkbox_frame, text=self.translations[self.language]["select_sequence"], font=("Arial", 12, "bold"), text_color="black")
        size_label.grid(row=len(columns)//2, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="w")

        self.variable_size_checkbox = ctk.CTkCheckBox(self.checkbox_frame, text="Taille variable", text_color="black", command=self.toggle_variable_size)
        self.variable_size_checkbox.grid(row=len(columns)//2 + 1, column=0, pady=7, padx=10, sticky="w")

        self.fixed_size_checkbox = ctk.CTkCheckBox(self.checkbox_frame, text="Taille fixe", text_color="black", command=self.toggle_fixed_size)
        self.fixed_size_checkbox.grid(row=len(columns)//2 + 1, column=1, pady=7, padx=10, sticky="w")

        self.variable_size_entry = ctk.CTkEntry(self.checkbox_frame)
        self.variable_size_entry.grid(row=len(columns)//2 + 2, column=0, pady=7, padx=10, sticky="w")
        self.variable_size_entry.grid_remove() """

    def toggle_variable_size(self):
        if self.variable_size_checkbox.get():
            self.fixed_size_checkbox.deselect()
            self.variable_size_entry.grid()
        else:
            self.variable_size_entry.grid_remove()

    def toggle_fixed_size(self):
        if self.fixed_size_checkbox.get():
            self.variable_size_checkbox.deselect()
            self.variable_size_entry.grid_remove()
   
    # Gestion des tooltips
    def show_tooltip(self, event, text):
        if not hasattr(self, 'tooltip_window') or not self.tooltip_window.winfo_exists():
            x, y = event.x_root, event.y_root
            self.tooltip_window = tk.Toplevel(self.root)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x+30}+{y-10}") 

            label = tk.Label(self.tooltip_window, text=text, background="#f0f0f0")
            label.pack(padx=10, pady=5)

    def hide_tooltip(self, event):
        if hasattr(self, 'tooltip_window') and self.tooltip_window.winfo_exists():
            self.tooltip_window.destroy()
            del self.tooltip_window

    # Drag & Drop
    def create_drag_drop(self, main_frame):
        canvas = tk.Canvas(main_frame, width=320, height=120, bg="white", highlightthickness=0)
        canvas.pack(pady=20)
        canvas.create_rectangle(5, 5, 315, 115, outline="black", width=2, dash=(5, 5))

        drop_frame = ctk.CTkFrame(main_frame, fg_color="#E0E0E0", corner_radius=10)
        drop_frame.configure(width=300, height=100)
        drop_frame.pack_propagate(False)
        drop_frame.place(in_=canvas, anchor="center", relx=0.5, rely=0.5)

        image_path = "upload.png" 
        image = Image.open(image_path)
        image = image.resize((24, 24))  
        self.logo_image = ctk.CTkImage(light_image=image, dark_image=image, size=(24, 24))

        self.drop_label = ctk.CTkLabel(
            drop_frame, 
            text=self.translations[self.language]["drop_file"], 
            font=("Arial", 14), 
            text_color="black",
            image=self.logo_image,  
            compound="bottom" # Position le text en dessus
        )

        self.drop_label.pack(expand=True)

        self.drop_label.bind("<Button-1>", self.on_label_click)  # Left mouse button click
        self.drop_label.configure(cursor="hand2")  # Change cursor on hover

        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', self.on_file_drop)
    
    def on_label_click(self, event):
        # Ajouter un filtre pour ouvrir uniquement les fichiers gpx et csv
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                (self.translations[self.language]["csv_file"], "*.csv"),
                (self.translations[self.language]["gpx_file"], "*.gpx")
            ]
        )
        
        if file_path:
            self.drop_label.configure(text=file_path)

    # Fonction qui s'execute quand on sauvegarde le fichier
    def on_file_drop(self, event):
        print(f"Fichier déposé : {event.data}")
        files = event.widget.tk.splitlist(event.data)
        if files:
            first_file = files[0]
            file_name = os.path.basename(first_file)
            print(f"Fichier déposé : {file_name}")
            # Récupérer l'extension du fichier
            file_ext = os.path.splitext(first_file)[1].lower()
            # Tester si l'extension du fichier est de type "GPX" ou "CSV"
            if file_ext in ('.gpx', '.csv'):
                self.drop_label.configure(text=first_file) #file_name si on vuet que le nom du fichier
            else:
                self.drop_label.configure(text=self.translations[self.language]["drop_file"])
                messagebox.showerror(
                    self.translations[self.language]["error_title"],
                    self.translations[self.language]["invalid_file_type"]
                )
         
    def open_main_window(self):
        from main_window import MainWindow
        self.clear_window()
        MainWindow(self.root)

    def open_page1(self):
        from page1 import Page1
        if not isinstance(self, Page1):
            self.clear_window()
            Page1(self.root)

    def open_page2(self):
        from page2 import Page2
        if not isinstance(self, Page2):
            global selected_algorithm, name_file
            name_file = os.path.basename(self.drop_label.cget("text"))
            selected_algorithm = self.algo_dropdown.get()
            if selected_algorithm == "CSV":
                print(selected_algorithm)
                csv_chosen()
            else:
                print(selected_algorithm)
                gpx_chosen()
            self.clear_window()
            Page2(self.root, language=self.language)

    def open_page3(self):
        from page3 import Page3
        if not isinstance(self, Page3):
            self.clear_window()
            Page3(self.root, language=self.language)

    def open_page4(self):
        from page4 import Page4
        if not isinstance(self, Page4):
            self.clear_window()
            Page4(self.root, language=self.language)

            
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

