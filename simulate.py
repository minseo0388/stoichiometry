# simulate.py
# This module provides a function to simulate chemical reactions over time.
# It calculates the concentrations of species based on reaction kinetics and returns a DataFrame with the results.

import numpy as np
import pandas as pd
import math

def simulate_reactions(species, reactions, initials, dt, t_max, temperature=298.15, Ea_list=None, Ea_rev_list=None):
    R = 8.314

    def get_stoich(species_list):
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
