import numpy as np
import matplotlib.pyplot as plt
import materials


def calculate_bandgap(material, temperature):
    """Calculates the bandgap energy using the Varshni equation."""
    if material not in materials.materials:
        return None
    Eg0, alpha, beta = materials.materials[material]
    return Eg0 - (alpha * temperature**2) / (temperature + beta)

def plot_bandgap(material):
    """Plots bandgap energy vs. temperature for the selected material."""
    if material not in materials.materials:
        print("Error: Invalid material selected.")
        return
    
    temperatures = np.linspace(0, 600, 100)  # Temperature range from 0K to 600K
    bandgaps = [calculate_bandgap(material, T) for T in temperatures]
    plt.figure(figsize=(6, 4))
    plt.plot(temperatures, bandgaps, label=f"{material} Bandgap", color="blue")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Bandgap Energy (eV)")
    plt.title(f"Bandgap vs. Temperature for {material}")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    material = input("Enter material (Si, GaAs, Ge): ")
    plot_bandgap(material)