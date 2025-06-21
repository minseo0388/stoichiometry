# visualize.py
# This module provides functions to visualize the results of chemical reaction simulations.
# It includes plotting the concentration changes over time and the Arrhenius plot for rate constants.

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plot_results(df, title="Dynamic Chemical Reaction Simulation"):
    fig, ax = plt.subplots(figsize=(10, 6))
    lines = {}

    for col in df.columns:
        if col != 'Time':
            (line,) = ax.plot([], [], label=col)
            lines[col] = line

    ax.set_xlim(df['Time'].min(), df['Time'].max())
    ax.set_ylim(0, df[[col for col in df.columns if col != 'Time']].values.max() * 1.1)
    ax.set_xlabel('Time')
    ax.set_ylabel('Concentration')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    def init():
        for line in lines.values():
            line.set_data([], [])
        return lines.values()

    def update(frame):
        for col in lines:
            lines[col].set_data(df['Time'][:frame], df[col][:frame])
        return lines.values()

    ani = animation.FuncAnimation(fig, update, frames=len(df), init_func=init, blit=True, interval=50, repeat=False)
    plt.tight_layout()
    plt.show()

def plot_k_vs_temp(k_vals, Ea):
    R = 8.314
    temps = np.linspace(250, 500, 100)
    plt.figure()

    for idx, k0 in enumerate(k_vals):
        ks = [k0 * np.exp(-Ea / (R * T)) for T in temps]
        plt.plot(temps, ks, label=f"k{idx+1}(T)")
    
    plt.xlabel('Temperature (K)')
    plt.ylabel('Rate Constant k(T)')
    plt.title('Arrhenius Plot of Rate Constant(s) vs Temperature')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
