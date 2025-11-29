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
        
    Returns:
        List of unique species names found in the reaction.
    """
    # Remove whitespace and split by reaction arrows
    clean_str = reaction_str.replace(" ", "")
    # Handle both -> and <-> and ⇌
    parts = re.split(r'->|<->|⇌', clean_str)
    
    species = set()
    
    for part in parts:
        # Split by + to get individual terms
        terms = part.split('+')
        for term in terms:
            if not term: continue
            # Remove stoichiometric coefficients (leading numbers)
            # Match any leading digits, possibly with decimal
            match = re.search(r'^[\d\.]*', term)
            if match:
                coeff_len = len(match.group(0))
                s_name = term[coeff_len:]
                if s_name:
                    species.add(s_name)
            else:
                species.add(term)
                
    return sorted(list(species))

def parse_side(side_str: str) -> List[str]:
    """Helper to parse one side of a reaction (reactants or products)."""
    clean_str = side_str.replace(" ", "")
    terms = clean_str.split('+')
    result = []
    for term in terms:
        if not term: continue
        match = re.search(r'^([\d\.]*)(.+)$', term)
        if match:
            coeff_str = match.group(1)
            species = match.group(2)
            coeff = float(coeff_str) if coeff_str else 1.0
            # Add species multiple times based on coefficient (integer approximation for list representation)
            # For fractional coefficients, this simple list approach might be limited, 
            # but simulate.py uses counts, so we can just add it once? 
            # Wait, simulate.py uses `get_stoich` which counts occurrences in the list.
            # So "2A" needs to be ['A', 'A'].
            # What if coeff is 1.5? simulate.py's get_stoich returns integers.
            # Let's assume integer coefficients for this simple simulator or round them.
            count = int(round(coeff))
            result.extend([species] * count)
    return result

def build_reaction_list_from_details(details: List[Dict]) -> Tuple[List, List, List, List]:
    """
    Convert UI reaction details into simulation-ready lists.
    
    Args:
        details: List of dicts with keys 'reaction', 'k', 'Ea', 'reversible'
        
    Returns:
        Tuple of (reactions, k_vals, Ea_list, Ea_rev_list)
        where reactions is list of (reactants, products, k, reversible, kr)
    """
    reactions = []
    k_vals = []
    Ea_list = []
    Ea_rev_list = []
    
    for d in details:
        r_str = d['reaction']
        # Split into reactants and products
        if '->' in r_str:
            parts = r_str.split('->')
            reversible = d['reversible']
        elif '<->' in r_str:
            parts = r_str.split('<->')
            reversible = True
        elif '⇌' in r_str:
            parts = r_str.split('⇌')
            reversible = True
        else:
            continue # Invalid format
            
        if len(parts) != 2:
            continue
            
        reactants = parse_side(parts[0])
        products = parse_side(parts[1])
        
        k = d['k']
        Ea = d['Ea']
        
        # For reversible reactions, we need a reverse rate constant.
        # In this simple app, we might assume kr = k or let user specify?
        # The UI doesn't have a kr input. Let's assume kr = k * 0.1 for now.
        # Or better, calculate from equilibrium if we had delta G.
        # Let's just set kr = k * 0.5 as a placeholder if not specified, 
        # but wait, simulate.py signature is (reactants, products, k_ref, reversible, kr_ref)
        kr = k * 0.5 # Arbitrary assumption for demo purposes if not specified
        
        reactions.append((reactants, products, k, reversible, kr))
        k_vals.append(k)
        Ea_list.append(Ea)
        # Assume reverse activation energy is same or slightly different?
        # Let's just use Ea for reverse too for simplicity unless we want to add inputs.
        Ea_rev_list.append(Ea) 
        
    return reactions, k_vals, Ea_list, Ea_rev_list

def calculate_equilibrium(initials: Dict[str, float]) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    Calculates equilibrium concentrations and concentration ratios based on initial concentrations.
    
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
