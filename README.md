# Chemical Stoichiometry Simulator (화학양론 시뮬레이터)
수리 및 계산화학 화학양론 구현 (Mathematical and Computational Chemistry Stoichiometry Implementation)

A comprehensive educational tool for simulating and analyzing chemical reactions, designed for students and researchers in chemistry and chemical engineering.

## Features
- Interactive GUI for easy reaction input and simulation
- Real-time visualization of reaction progress with animated plots
- Support for complex reaction networks and mechanisms
- Temperature-dependent kinetics using the Arrhenius equation
- Equilibrium calculations and ratio analysis
- Data export for further analysis
- Save and load reaction configurations
- Built-in example reactions for learning

## Educational Value
- Learn fundamental chemical kinetics principles
- Visualize reaction dynamics in real-time
- Understand temperature effects on reaction rates
- Study equilibrium relationships and constants
- Practice stoichiometric calculations
- Explore reaction mechanisms
- Analyze concentration profiles
- Export data for reports and research

## Installation
```bash
# Clone the repository
git clone https://github.com/minseo0388/stoichiometry.git
cd stoichiometry

# Install required packages
pip install -r requirements.txt
```

## Getting Started
1. Run `main.py` to launch the application:
   ```python
   python main.py
   ```
2. Input reaction details in the GUI:
   - Enter chemical equations (e.g., "A + B -> C")
   - Set rate constants (k) and activation energies (Ea)
   - Mark reactions as reversible if needed
3. Set initial conditions and parameters:
   - Initial concentrations
   - Temperature
   - Time step and total simulation time
4. Click "Run Simulation" to visualize results
5. Export data or save configuration for later use

## Example Reactions
- Simple decomposition: A → B
- Reversible reaction: A + B ⇌ C
- Sequential reactions: 2A + B → C, C → D
- Complex mechanisms: A + B → C, C + D ⇌ E

## Mathematical Background
- Rate equations: r = k[A]ᵃ[B]ᵇ
- Arrhenius equation: k = A*exp(-Ea/RT)
- Equilibrium constant: Keq = [C]/([A][B])
- Numerical integration methods

## Technical Details
- Python-based implementation
- Numerical integration of rate equations
- Real-time Matplotlib visualizations
- Pandas for data handling and analysis
- Modular design for extensibility
- Type hints and documentation
- Error handling and validation

## For Researchers
- Export data in CSV format
- Customizable reaction parameters
- Support for complex mechanisms
- Temperature dependence studies
- Equilibrium analysis tools

## Contributing
Contributions are welcome! Please feel free to submit pull requests.

## License
MIT License - See LICENSE file for details.

## Contact
- Author: Minseo Choi<br>
          (Department of Chemistry, <br>
          College of Natural Sciences, <br>
          Chungnam National University)
- GitHub: [@minseo0388](https://github.com/minseo0388)
