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
import itertools


class Loading:
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
                "result": "Resultat",
                "visualization_data": "VISUALISATION DES DONNEES",
                "simulate": "Simuler",
                "back": "Retour",
                "menu": [
                    ("PRÉTRAITEMENT", self.open_page1, "edit.png"),
                    ("ENTRAÎNEMENT", self.open_page2, "params.png"),
                    ("RESULTAT", self.open_page3, "result.png"),
                    ("VISUALISATION DES\nDONNÉES", self.open_page4, "visu.png")
                ]
            },
            "en": {
                "result": "Result",
                "visualization_data": "VISUALIZATION DATA",
                "simulate": "Simulate",
                "back": "Back",
                "menu": [
                    ("PREPROCESSING", self.open_page1, "edit.png"),
                    ("TRAINING", self.open_page2, "params.png"),
                    ("RESULT", self.open_page3, "result.png"),
                    ("DATA VISUALIZATION", self.open_page4, "visu.png")
                ]
            }
        }
        self.create_sidebar()
        self.root = root
        self.root.title("Loading Page")
        
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(main_frame, text=self.translations[self.language]["result"], font=("Arial", 20, "bold"), text_color="black")
        title_label.pack(pady=10)

        self.canvas = tk.Canvas(main_frame, width=300, height=300, bg="white", highlightthickness=0)
        self.canvas.pack(pady=50)
        
        self.arc = self.canvas.create_arc(30, 30, 270, 270, start=0, extent=30, outline="blue", width=5, style=tk.ARC)
        self.angle = itertools.cycle(range(0, 360, 10))
        self.animate()
        
        # Bouton retour
        button_back = ctk.CTkButton(main_frame, text=self.translations[self.language]["back"] , width=100, fg_color="#1C3A6B", command=self.retour)
        button_back.pack(pady=10, anchor="e")

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
        
        # FRAME DES GRAPHIQUES
        self.graph_frame = ctk.CTkFrame(main_frame, fg_color="white")
        self.graph_frame.pack(pady=10, padx=10, anchor="center")
        
        # Ajouter le graphique
        self.create_plot()
        
        # Bouton retour
        button_back = ctk.CTkButton(main_frame, text=self.translations[self.language]["back"], width=100, fg_color="#1C3A6B", command=self.retour)
        button_back.pack(pady=10)

    def animate(self):
        self.canvas.itemconfig(self.arc, start=next(self.angle))
        self.root.after(50, self.animate)

    def create_plot(self):
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(200)
        y_actual = np.cumsum(np.random.randn(200)) + 500000
        y_predicted = y_actual + np.random.normal(0, 50000, size=200)
        
        ax.plot(x, y_actual, label="actual", color='blue', linestyle='-', marker='o', markersize=2)
        ax.plot(x, y_predicted, label="prediction", color='red', linestyle='-')
        ax.set_xlabel("Time step", fontsize=14)
        ax.set_ylabel("Global_active_power", fontsize=14)
        ax.legend()
        ax.set_title(self.translations[self.language]["visualization_data"], fontsize=14, fontweight='bold')
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    
    
    
    def afficher_graphe(self):
        print("Afficher le graphe")
    
    def telecharger_csv(self):
        print("Télécharger le fichier CSV")
    
    def afficher_graphe_csv(self):
        print("Afficher le graphe et télécharger le CSV")
    
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
                writer = csv.writer(file)
                # Ajoute un en-tête des pour les colonnes
                writer.writerow(["Colonne 1", "Colonne 2", "Colonne 3"])
                # Écrit les données 
                for row in self.val:
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
