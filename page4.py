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

class Page4:
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
        # FRAME PRINCIPAL AVEC SCROLL
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=self.canvas.yview)
        scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Titre principal
        title_label = ctk.CTkLabel(scrollable_frame, 
                                 text=self.translations[self.language]["visualization_data"], 
                                 font=("Arial", 28, "bold"), 
                                 text_color="#ff5733")
        title_label.pack(padx=20, pady=20, anchor="center")
        
        # FRAME DES GRAPHIQUES
        self.graph_frame = ctk.CTkFrame(scrollable_frame, fg_color="white")
        self.graph_frame.pack(pady=10, padx=10, anchor="center")
        
        # Ajouter le graphique
        self.create_plot()
        
        # Bouton retour
        ctk.CTkButton(main_frame, text=self.translations[self.language]["back"], width=100, fg_color="#1C3A6B", command=self.open_page3).place(relx=0.9, rely=0.95, anchor="center")

        
        # Configuration du scroll avec la molette de la souris
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    def create_plot(self):
        with open('configuration.csv', 'r') as file:
            rows = len(list(csv.reader(file)))
            print(rows)
            with open('chosen.csv', 'r') as config:
                read = csv.reader(config)
                chosen_graph = list(read)[0][0]
                print(chosen_graph)

                if (chosen_graph == "graphe avec tous les points" or chosen_graph == "all points graph"):
                    for i in range(1, rows):

                        image = ctk.CTkImage(light_image=Image.open(f"images/{i}/predict_plot.png"), size=(400, 200))
                        label_logo = ctk.CTkLabel(self.graph_frame, image=image, text=f"modele {i}")
                        label_logo.pack(pady=(10, 20))
                elif (chosen_graph == "graphe par trajectoire" or chosen_graph == "trajectory graph"):
                    for i in range(1, rows):
                        for n in range (5):
                            image = ctk.CTkImage(light_image=Image.open(f"images/{i}/sequence_{n}.png"), size=(400, 200))
                            label_logo = ctk.CTkLabel(self.graph_frame, image=image, text=f"modele {i}")
                            label_logo.pack(pady=(10, 20))
        
    
    def afficher_graphe(self):
        print("Afficher le graphe")
        #self.create_plot()
    
    #def telecharger_csv(self):
    #   print("Télécharger le fichier CSV")
    
    def afficher_graphe_csv(self):
        print("Afficher le graphe et télécharger le CSV")
    
    def retour(self):
        self.open_page3()
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
