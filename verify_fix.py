import unittest
from reactions import parse_custom_reaction, build_reaction_list_from_details
from simulate import simulate_reactions
import pandas as pd

class TestStoichiometry(unittest.TestCase):
    def test_parse_reaction(self):
        self.assertEqual(parse_custom_reaction("A -> B"), ['A', 'B'])
        self.assertEqual(parse_custom_reaction("2A + B -> C"), ['A', 'B', 'C'])
        self.assertEqual(parse_custom_reaction("A + B <-> C"), ['A', 'B', 'C'])
        
    def test_build_reaction_list(self):
        details = [{
            'reaction': '2A + B -> C',
            'k': 0.1,
            'Ea': 50000,
            'reversible': False
        }]
        reactions, k_vals, Ea_list, Ea_rev_list = build_reaction_list_from_details(details)
        self.assertEqual(len(reactions), 1)
        # Check reactants (2A + B) -> ['A', 'A', 'B'] or similar depending on implementation
        # My implementation returns list of species, so 2A -> A, A
        reactants, products, k, rev, kr = reactions[0]
        self.assertEqual(sorted(reactants), ['A', 'A', 'B'])
        self.assertEqual(products, ['C'])
        self.assertEqual(k, 0.1)
        self.assertFalse(rev)
        
    def test_simulation_run(self):
        species = ['A', 'B', 'C']
        reactions = [(['A'], ['B'], 0.1, False, 0.0)]
        initials = {'A': 1.0, 'B': 0.0, 'C': 0.0}
        df = simulate_reactions(species, reactions, initials, 0.1, 1.0)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn('[A]', df.columns)

if __name__ == '__main__':
    unittest.main()
