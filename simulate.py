"""
simulate.py - Chemical Reaction Kinetics Simulator

This module implements numerical simulation of chemical reactions using:
1. Rate equations for concentration changes
2. Arrhenius equation for temperature dependence
3. Mass action kinetics for reaction rates
4. Euler integration for time evolution

Educational Features:
- Clear implementation of chemical kinetics principles
- Step-by-step calculation of reaction rates
- Support for complex reaction networks
- Temperature-dependent rate constants

Theory Background:
- Rate Law: d[A]/dt = -k[A]ᵃ[B]ᵇ
- Arrhenius Equation: k = A*exp(-Ea/RT)
- Mass Action: rate = k∏[reactant]ⁿ
- Conservation of Mass

Author: minseo0388
License: MIT
"""

import numpy as np
import pandas as pd
import math
from typing import List, Dict, Tuple, Optional

def simulate_reactions(
    species: List[str],
    reactions: List[Tuple],
    initials: Dict[str, float],
    dt: float,
    t_max: float,
    temperature: float = 298.15,
    Ea_list: Optional[List[float]] = None,
    Ea_rev_list: Optional[List[float]] = None
) -> pd.DataFrame:
    """
    Simulate chemical reactions over time using numerical integration.
    
    Args:
        species: List of chemical species involved
        reactions: List of (reactants, products, k, reversible, kr) tuples
        initials: Initial concentrations (mol/L)
        dt: Time step for integration (s)
        t_max: Total simulation time (s)
        temperature: Reaction temperature (K)
        Ea_list: Activation energies for forward reactions (J/mol)
        Ea_rev_list: Activation energies for reverse reactions (J/mol)
    
    Returns:
        DataFrame with time series of concentrations
        
    Theory:
        - Uses Euler integration: [A]_new = [A]_old + (d[A]/dt)Δt
        - Rates from mass action: rate = k[A]ᵃ[B]ᵇ
        - Temperature dependence: k(T) = k₀exp(-Ea/RT)
        
    Example:
        >>> species = ['A', 'B', 'C']
        >>> reactions = [(['A', 'B'], ['C'], 0.001, True, 0.0001)]
        >>> initials = {'A': 1.0, 'B': 1.0, 'C': 0.0}
        >>> df = simulate_reactions(species, reactions, initials, 0.1, 10)
    """
    R = 8.314  # Universal gas constant (J/mol·K)

    def get_stoich(species_list: List[str]) -> Dict[str, int]:
        """Calculate stoichiometric coefficients for a list of species."""
        counts = {}
        for s in species_list:
            counts[s] = counts.get(s, 0) + 1
        return counts

    time = np.arange(0, t_max + dt, dt)
    data = {s: [initials.get(s, 0.0)] for s in species}

    for _ in time[1:]:
        delta = {s: 0.0 for s in species}
        for i, (reactants, products, k, reversible, kr) in enumerate(reactions):
            reactant_counts = get_stoich(reactants)
            product_counts = get_stoich(products)
            Ea_i = Ea_list[i] if Ea_list else 50000
            Ea_rev_i = Ea_rev_list[i] if Ea_rev_list else 50000

            k_T = k * math.exp(-Ea_i / (R * temperature))
            kr_T = kr * math.exp(-Ea_rev_i / (R * temperature)) if reversible else 0.0

            rate_fwd = k_T * np.prod([data[r][-1] ** reactant_counts[r] for r in reactant_counts])
            rate_rev = kr_T * np.prod([data[p][-1] ** product_counts[p] for p in product_counts]) if reversible else 0.0

            for r in reactants:
                delta[r] -= (rate_fwd - rate_rev)
            for p in products:
                delta[p] += (rate_fwd - rate_rev)
                
        for s in species:
            data[s].append(max(0.0, data[s][-1] + delta[s] * dt))

    df = pd.DataFrame({'Time': time})
    for s in species:
        df[f'[{s}]'] = data[s]
    return df
