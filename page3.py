import os
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from customtkinter import CTkImage
from PIL import Image
import page1
import page2
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

class Page3:
    def __init__(self, root, language):
        global selected_algorithm
        self.root = root
        self.language = language
        self.selected_algo = page1.selected_algorithm
        self.name_file = page1.name_file
        self.val = page2.all_rows
        print(f"Nom du fichier page 3 : {self.name_file}")
        print(f"Algorithme utilisé page 3 : {self.selected_algo}")
        self.translations = {
            "fr": {
                "visualization_data": "VISUALISATION DES DONNEES",
                "simulate": "Simuler",
                "back": "Retour",
                "show graph": "Afficher le graphe",
                "download csv": "Télécharger CSV",
                "show graph + csv": "Afficher le graphe + CSV",
                "graph types": "Types de graphe:",
                "trajectory graph": "graphe par trajectoire",
                "all points graph": "graphe avec tous les points",
                "result": "Resultat",
                "RMSE and train loss": "RMSE ET la COURBE D’apprentissage",
                "menu": [
                    ("PRÉTRAITEMENT", self.open_page1, "edit.png"),
                    ("ENTRAÎNEMENT", self.open_page2, "params.png"),
                    ("RESULTAT", self.open_page3, "result.png"),
                    ("VISUALISATION DES\nDONNÉES", self.open_page4, "visu.png")
                ]
            },
            "en": {
                "visualization_data": "VISUALIZATION DATA",
                "simulate": "Simulate",
                "back": "Back",
                "show graph": "Show graph",
                "download csv": "Download CSV",
                "show graph + csv": "Show graph + CSV",
                "graph types": "Graph types:",
                "trajectory graph": "trajectory graph",
                "all points graph": "all points graph",
                "result": "Result",
                "RMSE and train loss": "RMSE AND the LEARNING CURVE",
                "menu": [
                    ("PREPROCESSING", self.open_page1, "edit.png"),
                    ("TRAINING", self.open_page2, "params.png"),
                    ("RESULT", self.open_page3, "result.png"),
                    ("DATA VISUALIZATION", self.open_page4, "visu.png")
                ]
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
        title_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["result"], font=("Arial", 28, "bold"), text_color="black")
        title_label.pack(padx=20, pady=(20, 10), anchor="center")
        
        # Sous-titre
        subtitle_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["RMSE and train loss"], font=("Arial", 18, "italic"), text_color="black")
        subtitle_label.pack(anchor="center")
        
        # FRAME DES GRAPHIQUES
        self.graph_frame = ctk.CTkFrame(main_frame, fg_color="white")
        self.graph_frame.pack(pady=10, padx=10, anchor="center")
        
        # Ajouter le graphique
        #self.create_plot()
        image = ctk.CTkImage(light_image=Image.open("images/1/courbe_apprentissage.png"), size=(400, 200))
        label_logo = ctk.CTkLabel(self.graph_frame, image=image, text="")
        label_logo.pack(pady=(1, 2))

        with open("configuration.csv", "r", newline="") as file:
                #reader = csv.reader(file)
                rows = list(csv.reader(file))
                #nb_rows = sum(1 for line in file)
                MSE = rows[1][6]
                RMSE = rows[1][7]
                #print(MSE, RMSE)

        mse_label = types_label = ctk.CTkLabel(main_frame, text=f"Train MSE : {MSE}", font=("Arial", 16, "bold"), text_color="black")
        mse_label.pack(anchor="c", padx=20)
        rmse_label = types_label = ctk.CTkLabel(main_frame, text=f"Predict. RMSE : {RMSE}", font=("Arial", 16, "bold"), text_color="black")
        rmse_label.pack(anchor="c", padx=20)
        

        # Types de graphes
        types_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["graph types"], font=("Arial", 16, "bold"), text_color="black")
        types_label.pack(anchor="w", padx=20)
        
        graph_options = [self.translations[self.language]["trajectory graph"], self.translations[self.language]["all points graph"]]
        self.graph_listbox = ctk.CTkComboBox(main_frame, values=graph_options, width=250)
        self.graph_listbox.pack(padx=20, anchor="w")
        
        # BOUTONS
        button_frame = ctk.CTkFrame(main_frame, fg_color="white")
        button_frame.pack(pady=20)
        
        bouton_afficher = ctk.CTkButton(button_frame, text=self.translations[self.language]["show graph"], width=200, fg_color="#1C3A6B", command=self.afficher_graphe)
        bouton_afficher.pack(side="left", padx=10)
        
        bouton_csv = ctk.CTkButton(button_frame, text=self.translations[self.language]["download csv"], width=200, fg_color="#1C3A6B", command=self.telecharger_csv)
        bouton_csv.pack(side="left", padx=10)
        
        bouton_afficher_csv = ctk.CTkButton(button_frame, text=self.translations[self.language]["show graph + csv"], width=200, fg_color="#1C3A6B", command=self.afficher_graphe_csv)
        bouton_afficher_csv.pack(side="left", padx=10)
        
        # Bouton retour
        ctk.CTkButton(main_frame, text=self.translations[self.language]["back"], width=100, fg_color="#1C3A6B", command=self.open_page2).place(relx=0.9, rely=0.95, anchor="center")
        #button_back = ctk.CTkButton(main_frame, text=self.translations[self.language]["back"], width=100, fg_color="#1C3A6B", command=self.retour)
        #button_back.pack(pady=10, padx=20, anchor="e")
    
    def create_plot(self):
        image = ctk.CTkImage(light_image=Image.open("images/1/courbe_apprentissage.png"), size=(200, 200))
        label_logo = ctk.CTkLabel(self, image=image, text="")
        label_logo.pack(pady=(10, 20))
        '''
        self.fig, self.axs = plt.subplots(2, 1, figsize=(6, 4))
        x = np.linspace(0, 100, 100)
        y1_true = np.sin(x / 10) + 0.2
        y1_pred = y1_true + np.random.normal(0, 0.02, len(x))
        y2_true = np.cos(x / 10) + 0.5
        y2_pred = y2_true + np.random.normal(0, 0.02, len(x))
        
        self.axs[0].plot(x, y1_true, label="True Latitude")
        self.axs[0].plot(x, y1_pred, label="Predicted Latitude", linestyle="--")
        self.axs[0].legend()
        
        self.axs[1].plot(x, y2_true, label="True Longitude")
        self.axs[1].plot(x, y2_pred, label="Predicted Longitude", linestyle="--")
        self.axs[1].legend()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        '''
    def afficher_graphe(self):
        choice = self.graph_listbox.get()
        with open('chosen.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([choice])
        file_path = "configuration.csv"
        if os.path.exists(file_path): 
            with open(file_path, "r", newline="") as file:
                #reader = csv.reader(file)
                rows = list(csv.reader(file))
                #nb_rows = sum(1 for line in file)
                for i in range (1, len(rows)):
                    chosen_algo = rows[i][0]
                    chosen_parameters = rows[i][1:6]
                    print((chosen_algo, chosen_parameters))
                #data = list(reader)
                #has_data = len(data) > 1  # Vérifier s'il y a des lignes après l'en-tête
        self.open_page4()
        print("Afficher le graphe")
    
    def telecharger_csv(self):
        print("Télécharger le fichier CSV")
    
    def afficher_graphe_csv(self):
        choice = self.graph_listbox.get()
        with open('chosen.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([choice])
        # Ouvre le gestionnaire de fichier pour choisir où sauvegarder le fichier CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        
        if file_path:
            # Sauvegarde les données dans un fichier CSV
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                with open("configuration.csv", mode='r', newline='', encoding='utf-8') as read:
                    writer = csv.writer(file)
                    reader = csv.reader(read)
                    # Écrit les données 
                    for row in reader:
                        writer.writerow(row)
                print(f"Fichier CSV sauvegardé sous {file_path}")
        self.open_page4()
    
    def retour(self):
        print("Retour à la page précédente")
        
    def ouvrir_fenetre_courbe(self):
        curve_window = tk.Toplevel(self.root)
        curve_window.title("Courbes")
        curve_window.geometry("600x400")

    def telecharger_csv(self):
        # Ouvre le gestionnaire de fichier pour choisir où sauvegarder le fichier CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")])
        
        if file_path:
            # Sauvegarde les données dans un fichier CSV
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                with open("configuration.csv", mode='r', newline='', encoding='utf-8') as read:
                    writer = csv.writer(file)
                    reader = csv.reader(read)
                    # Écrit les données 
                    for row in reader:
                        writer.writerow(row)
                print(f"Fichier CSV sauvegardé sous {file_path}")


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
