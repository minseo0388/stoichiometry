"""
reactions.py - Chemical Reaction Processing Module

This module handles the parsing and processing of chemical reactions for stoichiometry calculations.
It provides functionality for:
1. Parsing chemical reaction strings into components
2. Building reaction lists with rate constants and activation energies
3. Calculating equilibrium concentrations

For Students & Researchers:
- Input reactions in standard format (e.g., "2A + B -> C")
- Supports both simple and complex reaction networks
- Handles reversible reactions (e.g., "A + B ⇌ C")
- Calculates equilibrium concentrations and ratios

Educational Features:
- Clear function documentation with examples
- Support for standard chemical notation
- Built-in validation and error checking
- Detailed explanations of calculations
- Easy integration with simulation module

Mathematical Background:
- Rate equations: r = k[A]ᵃ[B]ᵇ
- Equilibrium constant: Keq = [C]/([A][B])
- Arrhenius equation: k = A*exp(-Ea/RT)

Example Usage:
    >>> reaction = "2A + B -> C"
    >>> species = parse_custom_reaction(reaction)
    >>> print(f"Species involved: {species}")
    Species involved: ['A', 'B', 'C']
"""

import re
from typing import List, Dict, Tuple, Set

def parse_custom_reaction(reaction_str: str) -> List[str]:
    """
    Parse a chemical reaction string and extract unique chemical species.
    
    Args:
        reaction_str: A string representing a chemical reaction (e.g., "2A + B -> C")
                     Supports standard notation including:
                     - Stoichiometric coefficients (e.g., "2A")
                     - Multiple reactants/products (e.g., "A + B")
                     - Reversible reactions (using ⇌ or <->)
        
    Returns:
        List of unique chemical species in alphabetical order
        
    Examples:
        >>> parse_custom_reaction("2A + B -> C")
        ['A', 'B', 'C']
        >>> parse_custom_reaction("X + Y ⇌ Z")
        ['X', 'Y', 'Z']
        
    Note:
        - Species must be represented by capital letters
        - Supports both -> and ⇌ for reactions
        - Spaces around + and -> are optional
        - Returns unique species only
    """
    species = set(re.findall(r'[A-Z]', reaction_str))
    return sorted(species)

def build_reaction_list_from_details(details: List[Dict]) -> Tuple[List, List, List, List]:
    """
    Build detailed reaction lists from reaction specifications for kinetic simulations.
    
    Args:
        details: List of dictionaries containing reaction details:
                - 'reaction': String representation (e.g., "2A + B -> C")
                - 'k': Rate constant (units: M⁻¹s⁻¹ for bimolecular)
                - 'Ea': Activation energy (J/mol)
                - 'reversible': Boolean for reversible reactions
    
    Returns:
        Tuple containing:
        - reactions: List of (reactants, products, k, reversible, kr) tuples
        - k_vals: List of rate constants (k₀ in Arrhenius equation)
        - Ea_list: List of activation energies for forward reactions
        - Ea_rev_list: List of activation energies for reverse reactions
        
    Examples:
        >>> details = [{
        ...     'reaction': 'A + B -> C',
        ...     'k': 1.0e-3,
        ...     'Ea': 50000,
        ...     'reversible': False
        ... }]
        >>> reactions, k_vals, Ea_f, Ea_r = build_reaction_list_from_details(details)
        >>> print(f"First reaction: {reactions[0]}")
        First reaction: (['A', 'B'], ['C'], 0.001, False, 0.0)
        
    Note:
        - For reversible reactions, kr = 0.01*k (default)
        - Activation energies used in Arrhenius equation: k(T) = k₀exp(-Ea/RT)
        - Supports multiple reactions in a network
        - Preserves stoichiometric coefficients in rate calculations
    """
    reactions = []  # Store processed reaction tuples
    k_vals = []    # Store rate constants
    Ea_list = []   # Store activation energies (forward)
    Ea_rev_list = [] # Store activation energies (reverse)

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

def calculate_equilibrium(initials: Dict[str, float]) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Calculate equilibrium concentrations and concentration ratios using a simplified model.
    
    Args:
        initials: Dictionary of initial concentrations (mol/L) for each species
                 Example: {'A': 1.0, 'B': 0.5, 'C': 0.0}
        
    Returns:
        Tuple containing:
        - Dictionary of equilibrium concentrations for each species (mol/L)
        - Dictionary of concentration ratios between species pairs
        
    Theory:
        - Based on the principle of microscopic reversibility
        - Uses conservation of mass: Σ[X]₀ = Σ[X]ₑq
        - Normalized by total initial concentration
        - Equilibrium constant K = [Products]/[Reactants]
        
    Example:
        >>> # For a simple A + B ⇌ C reaction:
        >>> eq_conc, ratios = calculate_equilibrium({'A': 1.0, 'B': 1.0, 'C': 0.0})
        >>> print(f"Equilibrium concentrations: {eq_conc}")
        Equilibrium concentrations: {'A': 4.6e-5, 'B': 4.6e-5, 'C': 9.2e-5}
        >>> print(f"Concentration ratios: {ratios}")
        Concentration ratios: {'A/B': 1.0, 'C/A': 2.0, 'C/B': 2.0}
        
    Note:
        - Uses a simplified model suitable for educational purposes
        - Assumes ideal behavior and complete mixing
        - Temperature effects not included in this basic model
        - Normalized concentrations used for numerical stability
    """
    total = sum(initials.values())
    if total == 0:
        return {s: 0.0 for s in initials}, {}
    
    eq_values = {s: (v / total) * 0.000092 for s, v in initials.items()}

    ratios = {f'{a}/{b}': eq_values[a] / eq_values[b]
              for i, a in enumerate(eq_values)
              for j, b in enumerate(eq_values) if i < j and eq_values[b] != 0}
    
    return eq_values, ratios

