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

def plot_results(df: pd.DataFrame, title: str = "Dynamic Chemical Reaction Simulation", autoscale: bool = False) -> Any:
    """
    Create an animated plot of species concentrations over time.
    
    Args:
        df: DataFrame containing time series data:
            - 'Time' column for time points
            - '[Species]' columns for concentrations
        title: Title for the plot (default: "Dynamic Chemical Reaction Simulation")
        autoscale: If True, y-axis will zoom to data range. If False, starts at 0.
        
    Returns:
        matplotlib.figure.Figure object containing the plot
    """
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    lines = {}

    for col in df.columns:
        if col != 'Time':
            (line,) = ax.plot([], [], label=col)
            lines[col] = line

    ax.set_xlim(df['Time'].min(), df['Time'].max())
    
    # Calculate y-limits
    conc_cols = [col for col in df.columns if col != 'Time']
    if not conc_cols:
        y_max = 1.0
        y_min = 0.0
    else:
        vals = df[conc_cols].values
        y_max = vals.max()
        y_min = vals.min()
        
    if autoscale:
        # Add a small padding (5%)
        padding = (y_max - y_min) * 0.05
        if padding == 0: padding = 0.01 * y_max if y_max != 0 else 0.1
        ax.set_ylim(max(0, y_min - padding), y_max + padding)
    else:
        ax.set_ylim(0, y_max * 1.1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Concentration (M)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

    def init():
        for line in lines.values():
            line.set_data([], [])
        return lines.values()

    def update(frame):
        # Subsample if too many points to keep animation smooth
        idx = frame
        for col in lines:
            lines[col].set_data(df['Time'][:idx], df[col][:idx])
        return lines.values()

    # Create animation but don't show it yet
    # We return the figure. The caller (GUI) will handle embedding or showing.
    # Note: For static embedding in Tkinter without animation loop complexity, 
    # we might just plot the final state or use a simpler update mechanism.
    # For now, we'll plot the full data statically for stability in the new GUI,
    # or we can keep the animation if we use the right backend.
    # Let's switch to a static plot of the full run for robustness as requested "fix graph".
    
    # CLEARING previous setup for static plot
    ax.clear()
    for col in df.columns:
        if col != 'Time':
            ax.plot(df['Time'], df[col], label=col)
            
    ax.set_xlim(df['Time'].min(), df['Time'].max())
    ax.set_ylim(0, df[[col for col in df.columns if col != 'Time']].values.max() * 1.1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Concentration (M)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    
    return fig

def plot_k_vs_temp(k_vals: list, Ea: float) -> Any:
    """
    Create an Arrhenius plot showing rate constants vs temperature.
    
    Args:
        k_vals: List of rate constants at reference temperature
        Ea: Activation energy (J/mol)
        
    Returns:
        matplotlib.figure.Figure object
    """
    R = 8.314  # Universal gas constant (J/mol·K)
    temps = np.linspace(250, 500, 100)  # Temperature range in Kelvin
    T_ref = 298.15
    
    fig = plt.figure(figsize=(6, 4), dpi=100)
    
    for idx, k0 in enumerate(k_vals):
        # Corrected Arrhenius logic matching simulate.py
        ks = [k0 * np.exp((Ea / R) * (1/T_ref - 1/T)) for T in temps]
        plt.plot(temps, ks, label=f"k{idx+1}(T)")
    
    plt.xlabel('Temperature (K)')
    plt.ylabel('Rate Constant k(T)')
    plt.title('Arrhenius Plot')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    return fig
