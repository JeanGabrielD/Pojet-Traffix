import customtkinter as ctk
#from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

x = np.linspace(0, 60, 100)
true_latitude = 30 + np.sin(x / 10) * 0.5
predicted_latitude = 30 + np.sin(x / 10) * 0.5 + np.random.normal(0, 0.05, len(x))
true_longitude = -97 + np.cos(x / 10) * 0.5
predicted_longitude = -97 + np.cos(x / 10) * 0.5 + np.random.normal(0, 0.05, len(x))

root = ctk.CTk()
root.title("Visualisation des Donnees")


frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20)


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


canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.draw()
canvas.get_tk_widget().pack()

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

back_button = ctk.CTkButton(button_frame, text="BACK")
back_button.pack(side="left", padx=10)

simulate_button = ctk.CTkButton(button_frame, text="SIMULATE")
simulate_button.pack(side="right", padx=10)

root.mainloop()
