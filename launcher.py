import customtkinter as ctk
from main_window import MainWindow
from tkinterdnd2 import TkinterDnD

class Launcher:
    def __init__(self):
        ctk.set_appearance_mode("system")
        self.app = TkinterDnD.Tk()
        self.app.title("Traffix")
        self.app.geometry("1000x600")
        self.app.configure(bg="#E7E7E7")
        self.app.resizable(True, True)
        self.main_window = MainWindow(self.app)

    def run(self):

        self.app.mainloop()