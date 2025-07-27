"""
gui.py - Chemical Reaction Simulator Interface

A user-friendly graphical interface designed for students and researchers in chemistry.
This module provides:
1. Interactive input of reaction parameters
2. Real-time visualization of reaction progress
3. Data export capabilities
4. Support for saving and loading reaction setups

Educational Features:
- Predefined example reactions
- Clear parameter explanations
- Error checking and validation
- Visual feedback on simulation progress
- Helpful tooltips and guidance

Usage:
    Run main.py to start the application
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkinter.scrolledtext import ScrolledText
from simulate import simulate_reactions
from reactions import parse_custom_reaction, build_reaction_list_from_details, calculate_equilibrium
from visualize import plot_results, plot_k_vs_temp
import pandas as pd
import numpy as np
import json

def run_gui():
    """
    Launch the main GUI window for chemical reaction simulation.
    
    Features:
    - Input fields for reaction parameters
    - Real-time visualization
    - Data export options
    - Save/load functionality
    
    The GUI provides a user-friendly interface for:
    1. Entering chemical reactions
    2. Setting rate constants and activation energies
    3. Specifying initial concentrations
    4. Running simulations
    5. Visualizing results
    """
    
    # Example reactions for educational purposes
    predefined_reactions = {
        "A + B → C": "A+B->C",        # Simple bimolecular reaction
        "A → B": "A->B",              # First-order decay
        "2A + B → C": "2A+B->C",      # Higher-order reaction
        "A + B → C, C → D": "A+B->C, C->D",  # Sequential reactions
        "X + Y ⇌ Z": "X+Y->Z, Z->X+Y"  # Reversible reaction
    }

    reaction_entries = []

    def add_reaction_field():
        """Add a new reaction input row with labels and entry fields."""
        # Create a frame for the reaction entry row
        frame = ttk.Frame(root)
        frame.pack(pady=2, padx=5)
        
        # Tooltip texts for educational guidance
        tooltips = {
            "reaction": "Enter reaction (e.g., 'A + B -> C' or '2A + B -> C')",
            "k": "Rate constant (e.g., 0.001 for slow, 1.0 for fast)",
            "Ea": "Activation energy in J/mol (e.g., 50000)",
            "reversible": "Check for reversible reactions (e.g., A + B ⇌ C)"
        }
        
        ttk.Label(frame, text="Reaction:").pack(side=tk.LEFT)

        rxn_entry = tk.Entry(frame, width=20)
        rxn_entry.pack(side=tk.LEFT)
        tk.Label(frame, text="k:").pack(side=tk.LEFT)

        k_entry = tk.Entry(frame, width=6)
        k_entry.pack(side=tk.LEFT)
        tk.Label(frame, text="Ea:").pack(side=tk.LEFT)

        ea_entry = tk.Entry(frame, width=8)
        ea_entry.pack(side=tk.LEFT)

        reversible_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Reversible", variable=reversible_var).pack(side=tk.LEFT)

        reaction_entries.append((rxn_entry, k_entry, ea_entry, reversible_var))

    def save_reactions():
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            data = []
            for rxn, k, ea, rev in reaction_entries:
                data.append({
                    "reaction": rxn.get(),
                    "k": k.get(),
                    "Ea": ea.get(),
                    "reversible": rev.get()
                })
            with open(filename, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo("Saved", f"Saved reaction details to {filename}")

    def load_reactions():
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    add_reaction_field()
                    reaction_entries[-1][0].insert(0, item['reaction'])
                    reaction_entries[-1][1].insert(0, item['k'])
                    reaction_entries[-1][2].insert(0, item['Ea'])
                    reaction_entries[-1][3].set(item['reversible'])

    def on_run():
        try:
            initials = dict((s.strip(), float(v)) for s, v in (x.split('=') for x in initials_entry.get().split(',')))
            dt = float(dt_entry.get())
            t_max = float(tmax_entry.get())
            temp = float(temp_entry.get())

            reaction_details = []

            for rxn, k, ea, rev in reaction_entries:
                if rxn.get():
                    reaction_details.append({
                        "reaction": rxn.get(),
                        "k": float(k.get()),
                        "Ea": float(ea.get()),
                        "reversible": rev.get()
                    })

            species = sorted(set(s for d in reaction_details for s in parse_custom_reaction(d['reaction'])))
            reactions, k_vals, Ea_list, Ea_rev_list = build_reaction_list_from_details(reaction_details)
            df = simulate_reactions(species, reactions, initials, dt, t_max, temperature=temp, Ea_list=Ea_list, Ea_rev_list=Ea_rev_list)
            plot_results(df)
            plot_k_vs_temp(k_vals, Ea_list[0])
            eq_vals, ratios = calculate_equilibrium(initials)
            
            msg = "Equilibrium concentrations:\n" + "\n".join(f"{s}: {v:.6f}" for s, v in eq_vals.items())
            msg += "\n\nRatios:\n" + "\n".join(f"{r}: {v:.6f}" for r, v in ratios.items())
            messagebox.showinfo("Equilibrium Info", msg)

            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                df.to_csv(filename, index=False)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Chemical Reaction Simulator")

    tk.Label(root, text="Initial Concentrations (e.g., A=1,B=0.5,C=0):").pack()
    initials_entry = tk.Entry(root)
    initials_entry.insert(0, "A=1,B=1,C=0")
    initials_entry.pack()

    for label, default in [("Temperature (K)", "298.15"), ("Time Step (dt)", "1.0"), ("Total Time (t_max)", "50")]:
        tk.Label(root, text=label).pack()
        entry = tk.Entry(root)
        entry.insert(0, default)
        entry.pack()
        if "Temp" in label:
            temp_entry = entry
        elif "dt" in label:
            dt_entry = entry
        elif "t_max" in label:
            tmax_entry = entry

    tk.Label(root, text="Reactions:").pack()
    add_reaction_field()
    tk.Button(root, text="Add Reaction", command=add_reaction_field).pack()
    tk.Button(root, text="Run Simulation", command=on_run).pack(pady=10)
    tk.Button(root, text="Save Reactions", command=save_reactions).pack(pady=2)
    tk.Button(root, text="Load Reactions", command=load_reactions).pack(pady=2)
    tk.Button(root, text="Load from Excel", command=lambda: messagebox.showinfo("Info", "Feature retained: Implement Excel parsing as needed")).pack(pady=2)
    root.mainloop()
