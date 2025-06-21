# reactions.py
# This module provides functions to parse chemical reactions, build reaction lists from details, 
# and calculate equilibrium concentrations.

import re

def parse_custom_reaction(reaction_str):
    species = set(re.findall(r'[A-Z]', reaction_str))
    return sorted(species)

def build_reaction_list_from_details(details):
    reactions = []
    k_vals = []
    Ea_list = []
    Ea_rev_list = []

    for item in details:
        lhs, rhs = item['reaction'].split('->')
        lhs_parsed = re.findall(r'(\\d*)\\s*([A-Z])', lhs)
        rhs_parsed = re.findall(r'(\\d*)\\s*([A-Z])', rhs)

        reactants = []

        for count, sp in lhs_parsed:
            reactants.extend([sp] * (int(count) if count else 1))

        products = []

        for count, sp in rhs_parsed:
            products.extend([sp] * (int(count) if count else 1))
            
        reactions.append((reactants, products, item['k'], item['reversible'], 0.01 if item['reversible'] else 0.0))

        k_vals.append(item['k'])
        Ea_list.append(item['Ea'])
        Ea_rev_list.append(item['Ea'])  
        # could be separated
    return reactions, k_vals, Ea_list, Ea_rev_list

def calculate_equilibrium(initials):
    total = sum(initials.values())
    if total == 0:
        return {s: 0.0 for s in initials}, {}
    
    eq_values = {s: (v / total) * 0.000092 for s, v in initials.items()}

    ratios = {f'{a}/{b}': eq_values[a] / eq_values[b]
              for i, a in enumerate(eq_values)
              for j, b in enumerate(eq_values) if i < j and eq_values[b] != 0}
    
    return eq_values, ratios

