# gui.py
# This file provides a graphical user interface (GUI) for simulating chemical reactions.
# It allows users to input reaction details, run simulations, and visualize results.

import tkinter as tk
from tkinter import messagebox, filedialog
from simulate import simulate_reactions
from reactions import parse_custom_reaction, build_reaction_list_from_details, calculate_equilibrium
from visualize import plot_results, plot_k_vs_temp
import pandas as pd
import numpy as np
import json

def run_gui():
    predefined_reactions = {
        "A + B → C": "A+B->C",
        "A → B": "A->B",
        "2A + B → C": "2A+B->C",
        "A + B → C, C → D": "A+B->C, C->D",
        "X + Y ⇌ Z": "X+Y->Z, Z->X+Y"
    }

    reaction_entries = []

    def add_reaction_field():
        frame = tk.Frame(root)
        frame.pack()
        tk.Label(frame, text="Reaction:").pack(side=tk.LEFT)

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
