import customtkinter as ctk

class ConfigList(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = []
        self._create_headers()
        self._configure_columns()
        
        # Configuration de l'ancrage
        self.grid(sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

    def _create_headers(self):
        headers = [
            ("Type d'algo", 120),
            ("Cellules encodeur", 150),
            ("Cellules décodeur", 150),
            ("Époques", 80),
            ("Taille de lot", 100),
            ("Validation", 140),
            ("Actions", 160)  # Colonne combinée pour les boutons
        ]
        
        for col_idx, (header_text, width) in enumerate(headers):
            label = ctk.CTkLabel(
                self,
                text=header_text,
                width=width,
                fg_color=("gray70", "gray25"),
                corner_radius=6
            )
            label.grid(row=0, column=col_idx, padx=5, pady=5, sticky="ew")

    def _configure_columns(self):
        columns = [120, 150, 150, 80, 100, 140, 160]
        for col_idx, width in enumerate(columns):
            self.grid_columnconfigure(col_idx, minsize=width, weight=1)

    def add_row(self):
        row_idx = len(self.rows) + 1
        new_row = ListRow(self, row_idx)
        self.rows.append(new_row)

    def remove_row(self, row):
        if row in self.rows:
            row.destroy()
            self.rows.remove(row)
            self._reindex_rows()

    def _reindex_rows(self):
        for new_idx, row in enumerate(self.rows, start=1):
            row.update_row_index(new_idx)

    def get_configurations(self):
        return [row.get_values() for row in self.rows]

class ListRow:
    def __init__(self, parent, row_idx):
        self.parent = parent
        self.row_idx = row_idx
        self._create_widgets()
        self._add_action_buttons()

    def _create_widgets(self):
        self.widgets = {}
        
        # Widgets de configuration
        self.widgets['algo_type'] = ctk.CTkComboBox(
            self.parent,
            values=["LSTM", "GRU", "BiLSTM"],
            width=120
        )
        self.widgets['algo_type'].grid(row=self.row_idx, column=0, padx=5, pady=5, sticky="ew")
        
        entries_spec = [
            ('encoder_lstm_cells', 150),
            ('decoder_lstm_cells', 150),
            ('epochs', 80),
            ('batch_size', 100),
            ('validation_split', 140)
        ]
        
        for col_idx, (name, width) in enumerate(entries_spec, start=1):
            self.widgets[name] = ctk.CTkEntry(
                self.parent,
                width=width,
                placeholder_text=f"Entrez {name.replace('_', ' ')}"
            )
            self.widgets[name].grid(row=self.row_idx, column=col_idx, padx=5, pady=5, sticky="ew")

    def _add_action_buttons(self):
        # Frame pour regrouper les boutons
        self.btn_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.btn_frame.grid(row=self.row_idx, column=6, padx=5, pady=5, sticky="e")
        
        # Bouton Éditer
        self.edit_btn = ctk.CTkButton(
            self.btn_frame,
            text="✎ Éditer",
            width=75,
            fg_color="#2AA876",
            hover_color="#207A5A"
        )
        self.edit_btn.pack(side="left", padx=2)
        
        # Bouton Supprimer
        self.delete_btn = ctk.CTkButton(
            self.btn_frame,
            text="🗑 Supprimer",
            width=75,
            fg_color="#C74B4B",
            hover_color="#8A3535"
        )
        self.delete_btn.pack(side="left", padx=2)

    def update_row_index(self, new_idx):
        self.row_idx = new_idx
        for widget in self.widgets.values():
            widget.grid(row=new_idx, column=widget.grid_info()['column'])
        self.btn_frame.grid(row=new_idx, column=6)

    def get_values(self):
        return {key: widget.get() for key, widget in self.widgets.items()}

    def destroy(self):
        for widget in self.widgets.values():
            widget.destroy()
        self.btn_frame.destroy()

class ConfigListApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des Configurations")
        self.geometry("1200x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Configuration du thème
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Création de la liste
        self.config_list = ConfigList(
            self,
            label_text="Liste des Configurations",
            scrollbar_button_hover_color="gray"
        )
        
        # Panneau de contrôle
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(
            control_frame,
            text="+ Ajouter Configuration",
            command=self.config_list.add_row
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            control_frame,
            text="Exécuter Toutes",
            command=self._executer_toutes
        ).pack(side="right", padx=5)

    def _executer_toutes(self):
        configurations = self.config_list.get_configurations()
        print(f"Exécution de {len(configurations)} configurations...")
        for idx, config in enumerate(configurations, 1):
            print(f"Configuration {idx}: {config}")

if __name__ == "__main__":
    app = ConfigListApp()
    app.mainloop()