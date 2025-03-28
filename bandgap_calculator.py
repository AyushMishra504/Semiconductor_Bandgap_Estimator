import tkinter as tk
from tkinter import messagebox
from materials import materials, names
from plot_bandgap import plot_bandgap

# Function to show project information
def show_project_info():
    try:
        with open("project_info.txt", "r") as file:
            project_info = file.read()
        messagebox.showinfo("Project Information", project_info)
    except FileNotFoundError:
        messagebox.showerror("Error", "project_info.txt not found.")

class Tooltip:
    """Creates a hover tooltip for any Tkinter widget."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 10
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip_window, text=self.text, font=("Arial", 9), bg="yellow", relief="solid", borderwidth=1, padx=5, pady=2)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def calculate_bandgap(material, temperature):
    if material not in materials:
        return None
    Eg0, alpha, beta = materials[material]
    return Eg0 - (alpha * temperature**2) / (temperature + beta)

def on_calculate():
    try:
        material = material_var.get()
        temperature = float(temp_entry.get())
        Eg = calculate_bandgap(material, temperature)

        if Eg is None:
            messagebox.showerror("Error", "Invalid material selected.")
        else:
            material_name = names.get(material, material)
            info_label.config(text=f"At {temperature:.1f} K, the Eg for {material_name} will be:", font=("Arial", 10))
            result_label.config(text=f"{Eg:.4f} eV", font=("Arial", 14, "bold"))
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid temperature.")

def on_show_graph():
    material = material_var.get()
    plot_bandgap(material)

root = tk.Tk()
root.title("Semiconductor Bandgap Estimator")
root.geometry("460x350")
root.configure(bg="#f0f0f0")

# Title label
title_label = tk.Label(root, text="Semiconductor Bandgap Estimator", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# ℹ Info Icon (Next to Title)
info_icon = tk.Label(root, text="ⓘ", font=("Arial", 12, "bold"), fg="blue", bg="#f0f0f0", cursor="hand2")
info_icon.place(x=420, y=10)  # Top right corner
info_icon.bind("<Button-1>", lambda event: show_project_info())

Tooltip(info_icon, "Click to view project information.")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=5)

material_label = tk.Label(frame, text="Select Material:", font=("Arial", 11, "bold"), bg="#f0f0f0")
material_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

material_var = tk.StringVar(root)
material_var.set("Si")
material_menu = tk.OptionMenu(frame, material_var, *materials.keys())
material_menu.grid(row=0, column=2, padx=10, pady=5)

temp_label = tk.Label(frame, text="Enter Temperature (K):", font=("Arial", 11, "bold"), bg="#f0f0f0")
temp_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# Tooltip for temperature input
temp_info = tk.Label(frame, text="ℹ", font=("Arial", 10, "bold"), fg="blue", bg="#f0f0f0", cursor="hand2")
temp_info.grid(row=1, column=1, padx=2, pady=5, sticky="w")
Tooltip(temp_info, "Temperature in Kelvin (K). Higher temperature decreases Eg.")

default_temperature = 298
temp_entry = tk.Entry(frame, font=("Arial", 11), width=10)
temp_entry.insert(0, str(default_temperature))
temp_entry.grid(row=1, column=2, padx=10, pady=5)

calculate_btn = tk.Button(root, text="Calculate", font=("Arial", 11, "bold"), bg="#007acc", fg="white", command=on_calculate)
calculate_btn.pack(pady=10)

info_label = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#f0f0f0")
info_label.pack()
result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#f0f0f0")
result_label.pack()

# Tooltip for Eg explanation
bandgap_info = tk.Label(root, text="ℹ", font=("Arial", 10, "bold"), fg="blue", bg="#f0f0f0", cursor="hand2")
bandgap_info.pack()
Tooltip(bandgap_info, "Eg (Bandgap Energy) is the energy required for electron conduction.")

graph_btn = tk.Button(root, text="Show Graph", font=("Arial", 11, "bold"), bg="#009688", fg="white", command=on_show_graph)
graph_btn.pack(pady=5)

def display_default_bandgap():
    material = material_var.get()
    temperature = float(temp_entry.get())
    Eg = calculate_bandgap(material, temperature)

    if Eg is not None:
        material_name = names.get(material, material)
        info_label.config(text=f"At {temperature:.1f} K, the Eg for {material_name} will be:", font=("Arial", 10))
        result_label.config(text=f"{Eg:.4f} eV", font=("Arial", 14, "bold"))

# Show default Eg on startup
root.after(100, display_default_bandgap)

root.mainloop()
