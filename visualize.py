"""
visualize.py - Chemical Reaction Visualization Module

This module provides advanced visualization tools for chemical reaction simulations:
1. Dynamic concentration plots over time
2. Arrhenius plots for temperature dependence
3. Interactive animations of reaction progress

For Students & Researchers:
- Real-time visualization of reaction progress
- Clear representation of concentration changes
- Temperature-dependent rate constant analysis
- Publication-quality figures with proper labeling
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from typing import Dict, Any
import pandas as pd

def plot_results(df: pd.DataFrame, title: str = "Dynamic Chemical Reaction Simulation") -> None:
    """
    Create an animated plot of species concentrations over time.
    
    Args:
        df: DataFrame containing time series data:
            - 'Time' column for time points
            - '[Species]' columns for concentrations
        title: Title for the plot (default: "Dynamic Chemical Reaction Simulation")
        
    Note:
        - Creates an interactive animation
        - X-axis: Time
        - Y-axis: Concentration
        - Each species is plotted in a different color
        - Legend identifies each species
    """
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

def plot_k_vs_temp(k_vals: list, Ea: float) -> None:
    """
    Create an Arrhenius plot showing rate constants vs temperature.
    
    Args:
        k_vals: List of rate constants at reference temperature
        Ea: Activation energy (J/mol)
        
    Note:
        - Demonstrates temperature dependence of rate constants
        - Uses Arrhenius equation: k(T) = k₀exp(-Ea/RT)
        - Temperature range: 250-500K
        - Plots multiple rate constants if provided
        
    Educational Value:
        - Visualize how rate constants change with temperature
        - Understand the exponential nature of the Arrhenius equation
        - Compare different rate constants' temperature dependence
    """
    R = 8.314  # Universal gas constant (J/mol·K)
    temps = np.linspace(250, 500, 100)  # Temperature range in Kelvin
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
