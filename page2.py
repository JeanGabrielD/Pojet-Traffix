import os
from tkinter import messagebox, ttk
import customtkinter as ctk
import tkinter as tk
from customtkinter import CTkImage
from PIL import Image, ImageTk
from PIL import Image
import csv
from models import main
textboxes = {} # Pour sauvegarder les champs de saisie
labels =  {} # Pour souvegarder les labels
encoder = "" #
all_rows = [] # Pour sauvegarder les lignes
chosen = []
algo_chosen = ""
rows = []

def clear_csv():
    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow("")

class Page2:
    def __init__(self, root, language):
        self.root = root
        self.language = language

        self.columns_dict = {
            "Encoder decoder model": ["encoder_lstm_cells", "decoder_lstm_cells", "epochs", "batch_size", "validation_split"],

            "Simple LSTM model": ["lstm_layers", "lstm_cells", "epochs", "batch_size", "validation_split"],
            
            "Encoder decoder bidirectional model": ["lstm_layers", "lstm_cells", "epochs", "batch_size", "validation_split"]
        }
         # Dictionnaire de traductions
        self.translations = {
            "fr": {
                "dataset_size": "Taille du dataset (Entre 0 et 1) :",
                "select_sequence": "Taille des séquences :",
                "variable_size": "Taille variable :",
                "fixed_size": "Taille fixe :",
                "no_data": "Pas de données",
                "validate": "Valider",
                "training": "ENTRAÎNEMENT",
                "choose_algo": "Choisir un algorithme :",
                "select_args": "Sélectionner les arguments :",
                "simulate": "Simuler",
                "simulation_progress": "Progression de la simulation",
                "back": "Retour",
                "menu": [
                    ("PRÉTRAITEMENT", self.open_page1, "edit.png"),
                    ("ENTRAÎNEMENT", self.open_page2, "params.png"),
                    ("RESULTAT", self.open_page3, "result.png"),
                    ("VISUALISATION DES\nDONNÉES", self.open_page4, "visu.png")
                ],
                "columns": {
                    "Encoder decoder model": ["Nb neurones encodeur", "Nb neurones décodeur", "Nb epochs", "Batch size", "Learning rate"],
                    "Simple LSTM model": ["Nb CONV1D neurones encodeur", "Nb LSTM neurones encodeur", "Nb CONV1D neurones décodeur", "Nb LSTM neurones décodeur", "Nb epochs", "Batch size", "Learning rate"],
                    "Encoder decoder bidirectional model": ["Nb neurones encodeur", "Nb neurones décodeur", "Nb epochs", "Batch size", "Learning rate"],
                },
                "infos": {
                    "Encoder decoder model": ["a faire, par defaut =64", "a faire, par defaut =64", "a faire, par defaut =50", "a faire, par defaut =64", "a faire, par defaut =0.1"],
                    "Simple LSTM model": ["a faire, par defaut =1", "a faire, par defaut =64", "a faire, par deafut =50", "a faire, par deafaut =64", "a faire, par defaut =0.1"],
                    "Encoder decoder bidirectional model": ["a faire, par defaut =64", "a faire, par defaut =64", "a faire, par defaut =50", "a faire, par defaut =64", "a faire, par defaut =0.1"],
                }
            },
            "en": {
                "dataset_size": "Dataset size (0 to 1):",
                "select_sequence": "Sequences length:",
                "variable_size": "Variable size:",
                "fixed_size": "Fixed size:",
                "no_data": "No data",
                "validate": "Validate",
                "training": "TRAINING",
                "choose_algo": "Choose an algorithm:",
                "select_args": "Select arguments:",
                "simulate": "Simulate",
                "simulation_progress": "Simulation progress",
                "back": "Back",
                "menu": [
                    ("PREPROCESSING", self.open_page1, "edit.png"),
                    ("TRAINING", self.open_page2, "params.png"),
                    ("RESULT", self.open_page3, "result.png"),
                    ("DATA VISUALIZATION", self.open_page4, "visu.png")
                ],
                "columns": {
                    "Encoder decoder model": ["encoder_lstm_cells", "decoder_lstm_cells", "epochs", "Batch size", "validation_split"],
                    "Simple LSTM model": ["Nb CONV1D encoder neurons", "Nb LSTM encoder neurons", "Nb CONV1D decoder neurons", "Nb LSTM decoder neurons", "Nb epochs", "Batch size", "Learning rate"],
                    "Encoder decoder bidirectional model": ["encoder_lstm_cells", "decoder_lstm_cells", "epochs", "Batch size", "validation_split"],
                },
                "infos": {
                    "Encoder decoder model": ["a faire, default =64", "a faire, default =64", "a faire, default =50", "a faire, default =64", "a faire, default =0.1"],
                    "Simple LSTM model": ["a faire, default =1", "a faire, default =64", "a faire, default =50", "a faire, default =64", "a faire, default =0.1"],
                    "Encoder decoder bidirectional model": ["a faire, default =64", "a faire, default =64", "a faire, default =50", "a faire, default =64", "a faire, default =0.1"],
                }
            }
        }


        self.create_sidebar()
        self.create_widgets()

    

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

    def create_widgets(self):            
        # FRAME PRINCIPAL
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        # Titre
        title_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["training"], font=("Arial", 28, "bold"), text_color="#ff5733")
        title_label.pack(padx=20, pady=20, anchor="center")

        # progress_label = ctk.CTkLabel(main_frame,  text=self.translations[self.language]["simulation_progress"], font=("Arial", 12, "bold"), text_color="black")
        # progress_label.pack(pady=(5, 2))
        # Bar de progression
        # self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        # self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))
        # self.progress_bar["value"] = 50

         # Liste déroulante pour choisir l'algorithme
        algo_frame = ctk.CTkFrame(main_frame, fg_color="white", width=500)
        algo_frame.pack(fill="x", padx=20, pady=20)
        algo_label = ctk.CTkLabel(algo_frame, text=self.translations[self.language]["choose_algo"], font=("Arial", 16, "bold"), text_color="black")
        algo_label.pack(pady=5, side="left")
        self.algo_dropdown = ctk.CTkComboBox(algo_frame, values=["Encoder decoder model", "Simple LSTM model", "Encoder decoder bidirectional model"], width=230)
        self.algo_dropdown.pack(padx=(10,0), pady=5, side="left")
        
        selection_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["select_args"], font=("Arial", 16, "bold"), text_color="black")
        selection_label.pack(padx=20, pady=5, anchor="w")
        
        # CHECHBOX
        self.checkbox_frame = ctk.CTkFrame(main_frame, fg_color="white", height=20)
        self.checkbox_frame.pack(padx=20, pady=5, anchor="w")
    
        image_path = "info.png"  
        image = Image.open(image_path)  
        image = image.resize((15, 15))  
        self.info_image = ImageTk.PhotoImage(image) 

         # FRAME LISTE (Taille réduite)
        self.list_frame = ctk.CTkFrame(main_frame, fg_color="white", height=250)  # Réduction de la hauteur
        self.list_frame.pack(fill="x", padx=20, pady=5)  # Ajustement du padding

        # ListView Columns
        columns = ["Model", "Encoder Layer/Cells", "Cells", "Epochs", "Batch Size", "Validation Split", "Actions"]

        # Table (Taille réduite)
        self.table = ctk.CTkFrame(self.list_frame, fg_color="#d1d1d1", height=200)  # Réduction de la hauteur
        self.table.pack(fill="x", expand=False, padx=5, pady=5)  # Ajustement des marges

        # Header Frame (Barre d'en-tête)
        header_frame = ctk.CTkFrame(self.table, fg_color="#d1d1d1", height=40)  # Hauteur plus compacte
        header_frame.pack(fill="x")

        
        for col in columns:
            label = ctk.CTkLabel(header_frame, text=col, font=("Arial", 14, "bold"), text_color="black")
            label.pack(side="left", padx=10, pady=5, expand=True)
        
          
        #global rows

         # Vérifier si le fichier CSV existe et contient des données
        file_path = "data.csv"
        file_exists = os.path.exists(file_path)
        has_data = False

        self.empty_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["no_data"], font=("Arial", 14, "bold"), text_color="gray")
        self.empty_label.pack(pady=20)

        if file_exists: 
            with open(file_path, "r", newline="") as file:
                reader = csv.reader(file)
                data = list(reader)
                has_data = len(data) > 1  # Vérifier s'il y a des lignes après l'en-tête

        if has_data:
            if self.empty_label != None:
                self.empty_label.pack_forget()
            # Affichage du tableau uniquement si le fichier contient des données
            if self.list_frame is None :
                self.list_frame = ctk.CTkFrame(main_frame, fg_color="white", height=250)
                self.list_frame.pack(fill="x", padx=20, pady=5)

                self.table = ctk.CTkFrame(self.list_frame, fg_color="#d1d1d1", height=200)
                self.table.pack(fill="x", expand=False, padx=5, pady=5)
                
                header_frame = ctk.CTkFrame(self.table, fg_color="#d1d1d1", height=40)
                header_frame.pack(fill="x")

                columns = ["Model", "Encoder Layer/Cells", "Cells", "Epochs", "Batch Size", "Validation Split", "Actions"]

                for col in columns:
                    label = ctk.CTkLabel(header_frame, text=col, font=("Arial", 14, "bold"), text_color="black")
                    label.pack(side="left", padx=10, pady=5, expand=True)

                global rows
            
            self.list_frame = ctk.CTkFrame(main_frame, fg_color="white", height=250)
            self.list_frame.pack(fill="x", padx=20, pady=5)
            # Lire les données du CSV et les afficher
            for row_data in data[1:]:  # Ignorer l'en-tête
                row_frame = ctk.CTkFrame(self.table, fg_color="white")
                row_frame.pack(fill="x", padx=5, pady=2)

                for val in row_data:
                    entry = ctk.CTkLabel(row_frame, text=val, font=("Arial", 12), text_color="black")
                    entry.pack(side="left", padx=10, pady=5, expand=True)

                action_frame = ctk.CTkFrame(row_frame, fg_color="white")
                action_frame.pack(side="left", padx=10, pady=10)

                delete_button = ctk.CTkButton(action_frame, text="Delete", fg_color="#D9534F", width=50,
                                            command=lambda rf=row_frame, rd=row_data: delete_row(rf, rd))
                delete_button.pack(side="left", padx=5)

                rows.append({"frame": row_frame, "data": row_data})

        else:
            # Afficher un message si le fichier est vide
            self.list_frame.pack_forget()
     

        def save_to_csv():
            global rows
            with open("data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(columns[:-1])
                for row in rows:
                    values = [child.cget("text") for child in row["frame"].winfo_children()[:-1]]
                    writer.writerow(values)
                    

        
            
        def add_row():
            global rows
            if self.empty_label:
                self.empty_label.pack_forget()
            self.list_frame.pack(fill="x", padx=20, pady=5)
            row_frame = ctk.CTkFrame(self.table, fg_color="white")
            row_frame.pack(fill="x", padx=5, pady=2)
            vals = []
            global chosen
            chosen = [float(textboxes[key].get()) for key in textboxes]
            print(chosen)
            global algo_chosen
            algo_chosen = self.algo_dropdown.get()
            print(algo_chosen)
            
            # Récupérer les valeurs des text boxes et des labels
            vals =[f"{labels[key].cget('text')} : {textboxes[key].get()}" for key in textboxes]
            vals.insert(0, self.algo_dropdown.get())

            row_data = []

            for val in vals:
                entry = ctk.CTkLabel(row_frame, text=val, font=("Arial", 12), text_color="black")
                entry.pack(side="left", padx=10, pady=5, expand=True)
                row_data.append(val)
            
            action_frame = ctk.CTkFrame(row_frame, fg_color="white")
            action_frame.pack(side="left", padx=10, pady=10)
            
            # edit_button = ctk.CTkButton(action_frame, text="Edit", fg_color="#1C3A6B", width=50, command=lambda: edit_row())
            # edit_button.pack(side="left", padx=5)
            
            delete_button = ctk.CTkButton(action_frame, text="Delete", fg_color="#D9534F", width=50, command=lambda: delete_row(row_frame, row_data))
            delete_button.pack(side="left", padx=5)
            
            rows.append({"frame": row_frame, "data": row_data})
          
            
            save_to_csv()
        
        def edit_row(values):
            print("Edit button clicked for:", values)
        
        def delete_row(row_frame, row_data):
            global rows
            row_frame.destroy()
            rows = [row for row in rows if row["data"] != row_data]  
            
            save_to_csv()
        
        # Insert example data

       # Fonction pour afficher un tooltip au survol
        def show_tooltip(event, text):
            if not hasattr(self, 'tooltip_window') or not self.tooltip_window.winfo_exists():
                x, y = event.x_root, event.y_root
                tooltip_window = tk.Toplevel(self.root)
                tooltip_window.wm_overrideredirect(True)
                tooltip_window.wm_geometry(f"+{x+30}+{y-10}")

                label = tk.Label(tooltip_window, text=text, background="#f0f0f0")
                label.pack(padx=10, pady=5)
                
                # Enregistrer la fenêtre tooltip dans un attribut pour pouvoir la gérer
                self.tooltip_window = tooltip_window

        # Validation des champs de saisie
        def validate_fields():
            missing_fields = []
            for key, entry in textboxes.items():
                if not entry.get().strip():
                    missing_fields.append(labels[key].cget("text"))

            if missing_fields:
                messagebox.showerror("Validation Error", f"Please fill in the following fields: {', '.join(missing_fields)}")
            else:
                add_row()

        # Fonction pour supprimer le tooltip lorsque la souris quitte l'icône
        def hide_tooltip(event):
            if hasattr(self, 'tooltip_window') and self.tooltip_window.winfo_exists():
                self.tooltip_window.destroy()
                del self.tooltip_window
              
        # Fonction pour mettre à jour les checkboxes en fonction de l'algorithme choisi
        def update_checkboxes(event=None):
            for widget in self.checkbox_frame.winfo_children():
                widget.destroy()

            # Récupérer l'algorithme sélectionné
            selected_algo = self.algo_dropdown.get()

            print(f"Algorithme sélectionné : {selected_algo}")
            columns = self.columns_dict.get(selected_algo, [])
        
            # Ajouter les checkboxes pour chaque colonne sur deux colonnes
            for i, column in enumerate(columns):
                row = i // 2 
                column_index = i % 2 
                # Saisie
                entry = self.float_entry()
                entry_label = ctk.CTkLabel(self.checkbox_frame, text=column, font=("Arial", 12), text_color="black")
                info_icon = ctk.CTkLabel(self.checkbox_frame, image=self.info_image, text="")
                textboxes[f"Textbox {i+1}"] = entry
                labels[f"Textbox {i+1}"] = entry_label
                if column_index == 1:
                    # Placement pour la deuxième colonne
                    entry.grid(row=row, column=column_index+2, pady=5, padx=(100, 10), sticky="w")
                    entry_label.grid(row=row, column=column_index+3, pady=5, padx=10, sticky="w")
                    info_icon.grid(row=row, column=column_index+4, padx=5, pady=5, sticky="w")
                else:
                    # Placement pour la première colonne
                    entry.grid(row=row, column=column_index, pady=5, padx=10, sticky="w")
                    entry_label.grid(row=row, column=column_index+1, pady=5, padx=10, sticky="w")
                    info_icon.grid(row=row, column=column_index+2, padx=5, pady=5, sticky="w")
                # Associer le survol de l'icône à l'affichage du tooltip
                info_icon.bind("<Enter>", lambda e, text=self.translations[self.language]["infos"].get(selected_algo, [])[i]: show_tooltip(e, text))
                info_icon.bind("<Leave>", hide_tooltip)
            # Bouton de validation
            validate_button = ctk.CTkButton(
                self.checkbox_frame, 
                text=self.translations[self.language]["validate"], 
                command=validate_fields, 
                fg_color="green", 
                hover_color="darkgreen"
            )
            validate_button.grid(row=len(columns)//2 + 4, column=2, columnspan=4, pady=10)

            size_label = ctk.CTkLabel(self.checkbox_frame, text=self.translations[self.language]["select_sequence"], font=("Arial", 12, "bold"), text_color="black")
            size_label.grid(row=len(columns)//2 +1, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="w")

            self.variable_size_checkbox = ctk.CTkCheckBox(self.checkbox_frame, text=self.translations[self.language]["variable_size"], text_color="black", command=self.toggle_variable_size)
            self.variable_size_checkbox.grid(row=len(columns)//2 + 2, column=0, pady=7, padx=10, sticky="w")

            self.fixed_size_checkbox = ctk.CTkCheckBox(self.checkbox_frame, text=self.translations[self.language]["fixed_size"], text_color="black", command=self.toggle_fixed_size)
            self.fixed_size_checkbox.grid(row=len(columns)//2 + 2, column=1, pady=7, padx=10, sticky="w")
            self.variable_size_checkbox.select()

            self.variable_size_entry = self.float_entry()
            self.variable_size_entry.grid(row=len(columns)//2 + 3, column=0, pady=7, padx=10, sticky="w")
            #self.variable_size_entry.grid_remove()

            self.dataset_size = ctk.CTkCheckBox(self.checkbox_frame, text=self.translations[self.language]["dataset_size"], text_color="black", command=self.toggle_fixed_size)
            self.dataset_size.grid(row=len(columns)//2 + 2, column=4, pady=7, padx=10, sticky="w")

            self.dataset_size_entry = self.float_entry()
            self.dataset_size_entry.grid(row=len(columns)//2 + 3, column=4, pady=7, padx=10, sticky="w")



        # Appeler update_checkboxes à chaque changement de sélection de l'algorithme
        self.algo_dropdown.configure(command=update_checkboxes)
        update_checkboxes()
        


        # Bouton simuler
        button_next = ctk.CTkButton(main_frame, text=self.translations[self.language]["simulate"], width=100, fg_color="#1C3A6B",command=self.simuler_bouton)
        button_next.place(relx=0.9, rely=0.95, anchor="center")
        
        # Bouton retour
        button_back = ctk.CTkButton(main_frame, text=self.translations[self.language]["back"], width=100, fg_color="#1C3A6B", command=self.open_page1)
        button_back.place(relx=0.75, rely=0.95, anchor="center")
    

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

    def update_progress(self, value):
        # Mise à jour de la barre de progression
        self.progress_bar["value"] = value
        self.root.update_idletasks()  # Refresh UI

    # Button customisé pour accepter uniquement les nombres
    def float_entry(self):
        def validate_float(new_text):
            if new_text in ["", ".", "-"]:
                return True
            try:
                float(new_text)
                return True
            except:
                return False
        
        vcmd = (self.root.register(validate_float), '%P')
        
        entry = ctk.CTkEntry(
                self.checkbox_frame,
                width=50,
                fg_color="white",
                text_color="black",
                validate="key",  
                validatecommand=vcmd
            )
            
        entry.configure(
                placeholder_text="0-9",
                justify="center",
                font=("Arial", 12)
            )
        
        return entry

    def open_main_window(self):
        from main_window import MainWindow
        self.clear_window()
        MainWindow(self.root)

    def open_page1(self):
        from page1 import Page1
        if not isinstance(self, Page1):
            self.clear_window()
            Page1(self.root, language=self.language)

    def open_page2(self):
        from page2 import Page2
        if not isinstance(self, Page2):
            self.clear_window()
            Page2(self.root)

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
    
    def simuler_bouton(self):
        global chosen
        global algo_chosen
        global rows
        print(chosen)
        print(algo_chosen)
        print(rows)
        if algo_chosen == "Encoder decoder model":
            main(1, int(chosen[0]), int(chosen[1]), int(chosen[2]), int(chosen[3]), chosen[4])
        elif algo_chosen == "Simple LSTM model":
            main(1, int(chosen[0]), int(chosen[1]), int(chosen[2]), int(chosen[3]), chosen[4])
        from loading import Loading
        global all_rows
        all_rows = [row["data"] for row in rows]
        rows.clear()
        self.clear_window()
        Loading(self.root, language=self.language)
        
            
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
