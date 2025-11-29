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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulate import simulate_reactions
from reactions import parse_custom_reaction, build_reaction_list_from_details, calculate_equilibrium
from visualize import plot_results, plot_k_vs_temp
import pandas as pd
import numpy as np
import json

def run_gui():
    """
    Launch the main GUI window for chemical reaction simulation.
    """
    root = tk.Tk()
    root.title("Chemical Reaction Simulator")
    root.geometry("1000x800")

    # Use Notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Tabs
    config_tab = ttk.Frame(notebook)
    results_tab = ttk.Frame(notebook)
    
    notebook.add(config_tab, text="Configuration")
    notebook.add(results_tab, text="Results")

    # --- Configuration Tab ---
    
    # Reaction Input Section
    reaction_frame = ttk.LabelFrame(config_tab, text="Reactions")
    reaction_frame.pack(fill=tk.X, padx=10, pady=5)

    reaction_entries = []

    def add_reaction_field():
        frame = ttk.Frame(reaction_frame)
        frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame, text="Reaction:").pack(side=tk.LEFT)
        rxn_entry = ttk.Entry(frame, width=30)
        rxn_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame, text="k (def:0.1):").pack(side=tk.LEFT)
        k_entry = ttk.Entry(frame, width=10)
        k_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame, text="Ea (def:50k):").pack(side=tk.LEFT)
        ea_entry = ttk.Entry(frame, width=10)
        ea_entry.pack(side=tk.LEFT, padx=5)
        
        rev_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Reversible", variable=rev_var).pack(side=tk.LEFT, padx=5)
        
        # Delete button
        def delete_row():
            frame.destroy()
            reaction_entries.remove((rxn_entry, k_entry, ea_entry, rev_var))
            update_species_inputs()
            
        ttk.Button(frame, text="X", width=3, command=delete_row).pack(side=tk.LEFT, padx=5)
        
        reaction_entries.append((rxn_entry, k_entry, ea_entry, rev_var))
        
        # Bind events to update species list
        rxn_entry.bind("<FocusOut>", lambda e: update_species_inputs())

    ttk.Button(reaction_frame, text="Add Reaction", command=add_reaction_field).pack(pady=5)

    # Simulation Parameters Section
    param_frame = ttk.LabelFrame(config_tab, text="Simulation Parameters")
    param_frame.pack(fill=tk.X, padx=10, pady=5)
    
    ttk.Label(param_frame, text="Temperature (K):").grid(row=0, column=0, padx=5, pady=5)
    temp_entry = ttk.Entry(param_frame)
    temp_entry.insert(0, "298.15")
    temp_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(param_frame, text="Time Step (dt):").grid(row=0, column=2, padx=5, pady=5)
    dt_entry = ttk.Entry(param_frame)
    dt_entry.insert(0, "0.1")
    dt_entry.grid(row=0, column=3, padx=5, pady=5)
    
    ttk.Label(param_frame, text="Total Time (t_max):").grid(row=0, column=4, padx=5, pady=5)
    tmax_entry = ttk.Entry(param_frame)
    tmax_entry.insert(0, "50")
    tmax_entry.grid(row=0, column=5, padx=5, pady=5)

    # Initial Concentrations Section (Dynamic)
    species_frame = ttk.LabelFrame(config_tab, text="Initial Concentrations")
    species_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    species_entries = {} # Map species name to entry widget

    def update_species_inputs():
        # Gather all species from reactions
        all_species = set()
        for rxn, _, _, _ in reaction_entries:
            text = rxn.get().strip()
            if text:
                try:
                    sps = parse_custom_reaction(text)
                    all_species.update(sps)
                except:
                    pass
        
        # Remove old entries
        for widget in species_frame.winfo_children():
            widget.destroy()
        species_entries.clear()
        
        # Create new entries
        for i, sp in enumerate(sorted(all_species)):
            f = ttk.Frame(species_frame)
            f.grid(row=i//4, column=i%4, padx=10, pady=5, sticky="w")
            ttk.Label(f, text=f"[{sp}]0:").pack(side=tk.LEFT)
            e = ttk.Entry(f, width=8)
            # e.insert(0, "0.0") # Don't default to 0, let it be empty
            e.pack(side=tk.LEFT)
            species_entries[sp] = e

    # Add label explaining blank inputs
    ttk.Label(species_frame, text="Note: Blank fields are treated as 0.0", font=("Arial", 8, "italic")).pack(anchor="w", padx=10)

    # Control Buttons
    btn_frame = ttk.Frame(config_tab)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)
    
    def on_run():
        try:
            # 1. Parse Parameters
            temp = float(temp_entry.get())
            dt = float(dt_entry.get())
            t_max = float(tmax_entry.get())
            
            # 2. Parse Reactions
            reaction_details = []
            for rxn, k, ea, rev in reaction_entries:
                r_text = rxn.get().strip()
                if not r_text: continue
                
                k_val = float(k.get()) if k.get() else 0.1
                ea_val = float(ea.get()) if ea.get() else 50000.0
                
                reaction_details.append({
                    "reaction": r_text,
                    "k": k_val,
                    "Ea": ea_val,
                    "reversible": rev.get()
                })
            
            if not reaction_details:
                messagebox.showwarning("Warning", "No valid reactions entered.")
                return

            # 3. Parse Initials
            initials = {}
            for sp, entry in species_entries.items():
                val_str = entry.get().strip()
                if not val_str:
                    val = 0.0
                else:
                    try:
                        val = float(val_str)
                    except ValueError:
                        val = 0.0 # Default to 0 on error too, or could warn
                initials[sp] = val
                
            # 4. Run Simulation
            species = sorted(initials.keys())
            reactions, k_vals, Ea_list, Ea_rev_list = build_reaction_list_from_details(reaction_details)
            
            df = simulate_reactions(species, reactions, initials, dt, t_max, temperature=temp, Ea_list=Ea_list, Ea_rev_list=Ea_rev_list)
            
            # 5. Display Results
            display_results(df, k_vals, Ea_list[0] if Ea_list else 0)
            
            # Switch to results tab
            notebook.select(results_tab)
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation failed: {str(e)}")

    ttk.Button(btn_frame, text="Run Simulation", command=on_run).pack(side=tk.RIGHT, padx=5)
    ttk.Button(btn_frame, text="Update Species", command=update_species_inputs).pack(side=tk.RIGHT, padx=5)

    # --- Results Tab ---
    
    plot_frame = ttk.Frame(results_tab)
    plot_frame.pack(fill=tk.BOTH, expand=True)
    
    def display_results(df, k_vals, Ea):
        # Clear previous plots
        for widget in plot_frame.winfo_children():
            widget.destroy()
            
        if df.empty or 'Time' not in df.columns:
             ttk.Label(plot_frame, text="No data to display").pack()
             return
            
        # Controls Frame
        ctrl_frame = ttk.Frame(plot_frame)
        ctrl_frame.pack(side=tk.TOP, fill=tk.X)
        
        autoscale_var = tk.BooleanVar(value=False)
        
        def refresh_plot():
            # Re-draw plot with current settings
            for widget in canvas_frame.winfo_children():
                widget.destroy()
            
            fig_conc = plot_results(df, title=f"Concentrations (T={temp_entry.get()}K)", autoscale=autoscale_var.get())
            canvas_conc = FigureCanvasTkAgg(fig_conc, master=canvas_frame)
            canvas_conc.draw()
            canvas_conc.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ttk.Checkbutton(ctrl_frame, text="Auto-scale Y-axis", variable=autoscale_var, command=refresh_plot).pack(side=tk.LEFT, padx=5)
        
        # Canvas Frame
        canvas_frame = ttk.Frame(plot_frame)
        canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Initial Draw
        refresh_plot()
        
        # 2. Arrhenius Plot (Optional, maybe in a popup or side-by-side)
        # For now, let's put it below if there's space, or just skip it to keep UI clean
        # Or add a button to show it
        
        btn_arrhenius = ttk.Button(plot_frame, text="Show Arrhenius Plot", 
                                   command=lambda: show_arrhenius(k_vals, Ea))
        btn_arrhenius.pack(pady=5)
        
        # Export Button
        btn_export = ttk.Button(plot_frame, text="Export CSV", 
                                command=lambda: export_csv(df))
        btn_export.pack(pady=5)

    def show_arrhenius(k_vals, Ea):
        top = tk.Toplevel(root)
        top.title("Arrhenius Plot")
        fig = plot_k_vs_temp(k_vals, Ea)
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def export_csv(df):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            df.to_csv(filename, index=False)
            messagebox.showinfo("Export", f"Data saved to {filename}")

    # Add one default reaction row
    add_reaction_field()
    
    root.mainloop()

if __name__ == "__main__":
    run_gui()
