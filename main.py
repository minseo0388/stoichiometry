
"""
main.py - Chemical Stoichiometry Simulator

Entry point for the Chemical Stoichiometry Simulator application.
This application provides an interactive environment for studying chemical reactions,
designed specifically for students and researchers in chemistry.

Features:
- Interactive GUI for reaction input and simulation
- Real-time visualization of reaction progress
- Temperature-dependent kinetics (Arrhenius equation)
- Equilibrium calculations and analysis
- Data export capabilities

Usage:
    python main.py

Examples:
    Study simple reactions:    A → B
    Reversible reactions:     A + B ⇌ C
    Complex mechanisms:       2A + B → C, C → D

For detailed documentation and tutorials, see README.md
"""

import sys
from gui import run_gui

def main():
    """
    Launches the graphical user interface for stoichiometry simulations and analysis.
    
    The GUI provides:
    - Input fields for reaction equations
    - Parameter settings (rate constants, activation energies)
    - Initial concentration settings
    - Temperature and time controls
    - Real-time visualization
    - Data export options
    
    Returns:
        None
    """
    try:
        run_gui()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
