import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import numpy as np

from customtkinter import CTkButton, CTkImage
from tkinter import PhotoImage

from translations import translations

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent

        self.frame_index = 0

        self.title("Traffix")
        self.geometry("1200x600")
        #self.state("zoomed")

        

        self.refresh()
        
    
    def remove_all_frames(self):
        """Remove all frames before refreshing the content."""
        for widget in self.winfo_children():
            if isinstance(widget, (tk.Frame, ctk.CTkFrame)):  # Destroy only frames
                widget.destroy()

    def refresh(self):
        self.remove_all_frames()
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1C3A6B")
        sidebar.pack(fill="y", side="left")


        logo_image = Image.open("logo_LSTM.png")
        logo_icon = ctk.CTkImage(logo_image, size=(150,150))
        logo_label = ctk.CTkLabel(sidebar, image=logo_icon, text="", fg_color="transparent", bg_color="transparent")
        logo_label.place(x=20, y=0)
        logo_label.pack(pady=10)
        #logo_label = ctk.CTkLabel(sidebar, text="LOGO", text_color="white", font=("Helvetica", 30, "bold"))
        #logo_label.pack(pady=(20, 40))

        menu_items = [self.parent.translate("preprocessing"), self.parent.translate("training"), self.parent.translate("visualization")]
        idx = 0
        images = [Image.open("edit.png"), Image.open("params.png"), Image.open("visu.png")]
     
        for item in menu_items:

            if idx == 0 :
                cmd = self.show_pretraitement
            elif idx == 1 :
                cmd = self.show_training
            else:
                cmd = self.show_visualizations
            icon = CTkImage(light_image=images[idx], size=(20, 20))
            idx = idx + 1
            button = ctk.CTkButton(
                sidebar, text=item, width=200, height=40, anchor="w", corner_radius=10, font=("Helvetica", 16, "bold"), fg_color="#1C3A6B",
                command=cmd, image=icon,
            )
            button.pack(pady=(0, 20), padx=10)
        if self.frame_index == 0:
            main_frame = ctk.CTkFrame(self, fg_color="white")
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            title_label = ctk.CTkLabel(main_frame, text=self.parent.translate("preprocessing"), font=("Helvetica", 28, "bold"))
            title_label.pack(padx=20, pady=20)

            columns = ["id-veh", "local_X", "local_Y", "latitude", "longitude"]
            infos = [
                "ID unique du véhicule.",
                "Position locale X du véhicule.",
                "Position locale Y du véhicule.",
                "Latitude GPS du véhicule.",
                "Longitude GPS du véhicule."
            ]
            y_positions = [90, 130, 170, 90, 130]
            x_positions = [200, 200, 200, 500, 500]

            self.info_labels = []
                
            for i, (col, info) in enumerate(zip(columns, infos)):
                # Checkbox
                checkbox = ctk.CTkCheckBox(main_frame, text=col)
                checkbox.place(x=x_positions[i], y=y_positions[i])

                # Icon I
                info_icon = ctk.CTkLabel(main_frame, text="ℹ", font=("Helvetica", 14, "bold"), text_color="blue", cursor="hand2")
                info_icon.place(x=x_positions[i] + 100, y=y_positions[i]) 

                # Affichage de l'information 
                tooltip = ctk.CTkLabel(main_frame, text=info, font=("Helvetica", 12), text_color="black", fg_color="#f0f0f0", padx=5, pady=5, wraplength=200)
                tooltip.place(x=x_positions[i] + 120, y=y_positions[i], anchor="w")
                tooltip.lower() 

                self.info_labels.append(tooltip)

                # Gérer les événements de survol
                def on_enter_tooltip(event, tooltip=tooltip):
                    tooltip.lift()  # Afficher

                def on_leave_tooltip(event, tooltip=tooltip):
                    tooltip.lower()  # Cacher 

                info_icon.bind("<Enter>", on_enter_tooltip)
                info_icon.bind("<Leave>", on_leave_tooltip)
                    
            select_label = ctk.CTkLabel(main_frame, text=self.parent.translate("select_file"), font=("Helvetica", 14))
            select_label.place(x=50, y=260)

            drop_frame = ctk.CTkFrame(main_frame, width=500, height=250, border_color="#d3d3d3", border_width=2, fg_color="white")
            drop_frame.place(x=300, y=260)

            drag_label = ctk.CTkLabel(drop_frame, text=self.parent.translate("drag_drop"), font=("Helvetica", 14))
            drag_label.pack(expand=True)

            browse_button = ctk.CTkButton(drop_frame, text="Browse Files", width=100)
            browse_button.pack(pady=(0, 10))

            back_button = ctk.CTkButton(main_frame, text=self.parent.translate("back"), width=100, fg_color="#1C3A6B", command=self.return_to_launcher)
            back_button.place(x=500, y=400)

            simulate_button = ctk.CTkButton(main_frame, text=self.parent.translate("simulate"), width=100, fg_color="#1C3A6B")
            simulate_button.place(x=650, y=400)

        elif self.frame_index == 1:
            main_frame = ctk.CTkFrame(self, fg_color="white")
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            title_label = ctk.CTkLabel(main_frame, text=self.parent.translate("training"), font=("Helvetica", 28, "italic"), text_color="black")
            title_label.pack(pady=10)

            # Algo Section Titles
            algo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            algo_frame.pack(pady=20, expand=True)

            algo1_label = ctk.CTkLabel(algo_frame, text="Algo 1", font=("Helvetica", 20, "bold"))
            algo1_label.grid(row=0, column=0, pady=10)

            algo2_label = ctk.CTkLabel(algo_frame, text="Algo 2", font=("Helvetica", 20, "bold"))
            algo2_label.grid(row=0, column=1, pady=10)

            """# Checkbox Labels
            algo1_options = [
                "nombre",
                "nombre LSTM",
                "nombre de alpha",
                "autre",
                "autre",
                "autre"
            ]

            algo2_options = [
                "nombre",
                "nombre LSTM",
                "nombre de alpha",
                "autre",
                "autre",
                "autre"
            ]"""
            
            algo1_options = [
                ("nombre", "Le nombre d'unités dans la couche."),
                ("nombre LSTM", "Le nombre de couches LSTM."),
                ("nombre de alpha", "Le paramètre alpha pour la régularisation."),
                ("autre", "Option supplémentaire pour Algo 1."),
                ("autre", "Option supplémentaire pour Algo 1."),
                ("autre", "Option supplémentaire pour Algo 1.")
            ]

            algo2_options = [
                ("nombre", "Le nombre d'unités dans la couche."),
                ("nombre LSTM", "Le nombre de couches LSTM."),
                ("nombre de alpha", "Le paramètre alpha pour la régularisation."),
                ("autre", "Option supplémentaire pour Algo 2."),
                ("autre", "Option supplémentaire pour Algo 2."),
                ("autre", "Option supplémentaire pour Algo 2.")
            ]
                    
            def show_tooltip(event, tooltip, icon):
                x = icon.winfo_rootx() - self.winfo_rootx() - 320  # Position relative à l'icône
                y = icon.winfo_rooty() - self.winfo_rooty() - 30
                tooltip.place(x=x, y=y)

            def hide_tooltip(tooltip):
                tooltip.place_forget()

            # Widgets for Algo 1
            for i, (option, info) in enumerate(algo1_options):
                if "nombre" in option.lower():
                    entry_label = ctk.CTkLabel(algo_frame, text=option, font=("Helvetica", 14))
                    entry_label.grid(row=i + 1, column=0, padx=110, pady=10, sticky="w")
                    entry = ctk.CTkEntry(algo_frame, width=50)
                    entry.grid(row=i + 1, column=0, padx=50, pady=10, sticky="w")
                else:
                    checkbox = ctk.CTkCheckBox(algo_frame, text=option)
                    checkbox.grid(row=i + 1, column=0, padx=50, pady=10, sticky="w")

                # Add info icon
                info_icon = ctk.CTkLabel(algo_frame, text="ℹ", font=("Helvetica", 14, "bold"), text_color="blue", cursor="hand2")
                info_icon.grid(row=i + 1, column=0, padx=(250 if "nombre" in option.lower() else 150, 0), pady=10, sticky="w")

                # Tooltip for info icon
                tooltip = ctk.CTkLabel(main_frame, text=info, font=("Helvetica", 12), text_color="black", fg_color="#f0f0f0", padx=5, pady=5, wraplength=200)
                tooltip.place_forget()  # Initially hidden

                info_icon.bind("<Enter>", lambda e, t=tooltip, i=info_icon: show_tooltip(e, t, i))
                info_icon.bind("<Leave>", lambda e, t=tooltip: hide_tooltip(t))

            # Widgets for Algo 2
            for i, (option, info) in enumerate(algo2_options):
                if "nombre" in option.lower():
                    entry_label = ctk.CTkLabel(algo_frame, text=option, font=("Helvetica", 14))
                    entry_label.grid(row=i + 1, column=1, padx=110, pady=10, sticky="w")
                    entry = ctk.CTkEntry(algo_frame, width=50)
                    entry.grid(row=i + 1, column=1, padx=50, pady=10, sticky="w")
                else:
                    checkbox = ctk.CTkCheckBox(algo_frame, text=option)
                    checkbox.grid(row=i + 1, column=1, padx=50, pady=10, sticky="w")

                # Add info icon
                info_icon = ctk.CTkLabel(algo_frame, text="ℹ", font=("Helvetica", 14, "bold"), text_color="blue", cursor="hand2")
                info_icon.grid(row=i + 1, column=1, padx=(250 if "nombre" in option.lower() else 150, 0), pady=10, sticky="w")

                # Tooltip for info icon
                tooltip = ctk.CTkLabel(main_frame, text=info, font=("Helvetica", 12), text_color="black", fg_color="#f0f0f0", padx=5, pady=5, wraplength=200)
                tooltip.place_forget()  # Initially hidden

                info_icon.bind("<Enter>", lambda e, t=tooltip, i=info_icon: show_tooltip(e, t, i))
                info_icon.bind("<Leave>", lambda e, t=tooltip: hide_tooltip(t))
                

            # Back and Simulate Buttons
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(pady=20)

            back_button = ctk.CTkButton(button_frame, text=self.parent.translate("back"), width=100, fg_color="#1C3A6B", command=self.show_pretraitement)
            back_button.grid(row=0, column=0, padx=20)

            simulate_button = ctk.CTkButton(button_frame, text=self.parent.translate("simulate"), width=100, fg_color="#1C3A6B")
            simulate_button.grid(row=0, column=1, padx=20)
        else:
            x = np.linspace(0, 60, 100)
            true_latitude = 30 + np.sin(x / 10) * 0.5
            predicted_latitude = 30 + np.sin(x / 10) * 0.5 + np.random.normal(0, 0.05, len(x))
            true_longitude = -97 + np.cos(x / 10) * 0.5
            predicted_longitude = -97 + np.cos(x / 10) * 0.5 + np.random.normal(0, 0.05, len(x))
            main_frame = ctk.CTkFrame(self, fg_color="white")
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            title_label = ctk.CTkLabel(main_frame, text=self.parent.translate("training"), font=("Helvetica", 28, "italic"), text_color="black")


            fig = Figure(figsize=(6, 4), dpi=100)
            ax1 = fig.add_subplot(211)
            ax2 = fig.add_subplot(212)

            ax1.plot(x, true_latitude, label="True Latitude", color='blue')
            ax1.plot(x, predicted_latitude, label="Predicted Latitude", color='orange')
            ax1.legend()
            ax1.set_title("True Latitude vs Predicted Latitude")

            ax2.plot(x, true_longitude, label="True Longitude", color='blue')
            ax2.plot(x, predicted_longitude, label="Predicted Longitude", color='orange')
            ax2.legend()
            ax2.set_title("True Longitude vs Predicted Longitude")


            canvas = FigureCanvasTkAgg(fig, master=main_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()

            button_frame = ctk.CTkFrame(main_frame)
            button_frame.pack(pady=10)

            back_button = ctk.CTkButton(button_frame, text=self.parent.translate("back"), command=self.show_training)
            back_button.pack(side="left", padx=10)

            simulate_button = ctk.CTkButton(button_frame, text=self.parent.translate("simulate"))
            simulate_button.pack(side="right", padx=10)
        
    def show_pretraitement(self):
        self.frame_index = 0
        self.refresh()

    def show_training(self):
        self.frame_index = 1
        self.refresh()
    
    def show_visualizations(self):
        self.frame_index = 2
        self.refresh()
        
    def return_to_launcher(self):
        self.destroy()  
        self.master.deiconify()



class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.language = "fr"

        self.title("Launcher")
        self.geometry("700x500")
        self.resizable(False, False)

        logo_image = Image.open("logo_LSTM.png")
        self.logo_icon = ctk.CTkImage(logo_image, size=(150,150))
        logo_label = ctk.CTkLabel(self, image=self.logo_icon, text="", fg_color="transparent", bg_color="transparent")
        logo_label.place(x=20, y=0)
        #logo_label = ctk.CTkLabel(self, text="LOGO", font=("Helvetica", 20, "italic"), text_color="gray")
        #logo_label.place(x=20, y=20)

        #title_label = ctk.CTkLabel(self, text="Prédiction de la congestion routière", font=("Helvetica", 32, "bold"))
        #title_label.pack(pady=80)
        self.title_label = ctk.CTkLabel(self, text=self.translate("title"), font=("Helvetica", 32, "bold"))
        self.title_label.pack(pady=(150,80))

        self.start_button = ctk.CTkButton(self, text=self.translate("start"), width=100, height=40, fg_color="#1C3A6B", font=("Helvetica", 18), command=self.open_main_window)
        self.start_button.pack(pady=20)

        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.pack(pady=20)

        fr_image = Image.open("france_flag.png").resize((50, 50))
        fr_icon = ImageTk.PhotoImage(fr_image)

        en_image = Image.open("uk_flag.png").resize((50, 50))
        en_icon = ImageTk.PhotoImage(en_image)

        self.fr_button = ctk.CTkButton(lang_frame, image=fr_icon, text="FRANÇAIS", compound="top", width=80, height=80, command=lambda: self.set_language("fr"))
        self.fr_button.grid(row=0, column=0, padx=20)

        self.en_button = ctk.CTkButton(lang_frame, image=en_icon, text="ENGLISH", compound="top", width=80, height=80, command=lambda: self.set_language("en"))
        self.en_button.grid(row=0, column=1, padx=20)

        self.fr_icon = fr_icon
        self.en_icon = en_icon

    def open_main_window(self):
        self.mainwindow = MainWindow(self)
        self.withdraw()
        
    def translate(self, key):
        return translations[self.language].get(key, key)
    
    def set_language(self, lang):
        self.language = lang
        self.title_label.configure(text=self.translate("title"))
        self.start_button.configure(text=self.translate("start"))
       
        


if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
