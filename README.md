# Chemical Equilibrium Calculator

A computational framework for solving complex aqueous chemical equilibrium systems using iterative numerical methods. This implementation provides a modular approach to equilibrium calculations with particular emphasis on halogen chemistry applications in water treatment processes.

## Overview

This package implements a numerical solver for multi-component aqueous chemical equilibrium systems. The algorithm employs an iterative approach to solve coupled equilibrium equations using the bisection method for individual reaction equilibria and a global iteration scheme for system convergence.

### Computational Approach

The equilibrium calculation employs the following methodology:

1. **Initialization**: Species concentrations are initialized from chemical input data
2. **Iterative Solution**: Each equilibrium reaction is solved sequentially using numerical root-finding
3. **Concentration Update**: Species concentrations are updated based on reaction extents
4. **Convergence**: The process repeats until system equilibrium is achieved

### Mathematical Foundation

For each equilibrium reaction of the form:
```
aA + bB ⇌ cC + dD
```

The algorithm solves for the reaction extent ξ such that:
```
Q - K = 0
```

where Q is the reaction quotient and K is the equilibrium constant. The bisection method is employed to find the root of this function within physically meaningful bounds.

## Architecture

### Core Components

#### Species Management (`core/species.py`)
- `ChemicalSpecies`: Data structure for individual chemical species
- `SpeciesManager`: Concentration registry with automatic pH coupling for H⁺/OH⁻ species

#### Reaction Management (`core/reactions.py`)
- `EquilibriumReaction`: Reaction definition with stoichiometry and equilibrium constants
- `ReactionManager`: Reaction database with legacy format compatibility

#### Equilibrium Engine (`core/equilibrium.py`)
- `ChemicalInputProcessor`: Converts chemical additions to species concentrations
- `EquilibriumCalculator`: Main computational engine implementing the iterative solution algorithm

#### Numerical Solver (`solvers/bisection.py`)
- `BisectionSolver`: Root-finding algorithm for individual equilibrium equations

### Data Interface

#### Input/Output System (`io/loaders.py`)
JSON-based data loading system supporting:
- Species initial concentrations
- Equilibrium reaction definitions
- Chemical scenario specifications

### Algorithm Implementation

The core calculation follows this sequence:

```
1. Load system definition (species, reactions, chemicals)
2. Initialize concentration vector from chemical inputs
3. For each iteration:
   a. For each reaction:
      - Calculate reaction quotient Q
      - Solve Q - K = 0 for reaction extent
      - Update species concentrations
   b. Enforce charge neutrality constraints
   c. Update pH-coupled species (H⁺/OH⁻)
4. Return converged concentration vector
```

### Numerical Considerations

- **Convergence Tolerance**: Default 1×10⁻¹⁵ for function values
- **Maximum Iterations**: 1000 for global equilibrium loop, 100 for individual reactions
- **Bounds Determination**: Physical constraints ensure non-negative concentrations
- **pH Coupling**: Automatic enforcement of water autoionization equilibrium (Kw = 1×10⁻¹⁴)

## Usage

### Basic Equilibrium Calculation

```python
from chemical_equilibrium import EquilibriumCalculator
from chemical_equilibrium.io.loaders import (
    load_species_data, load_reactions_data, load_scenario,
    create_species_manager_from_data, create_reaction_manager_from_data
)

# Load system definition
species_data = load_species_data("data/species.json")
reactions_data = load_reactions_data("data/reactions.json")
scenario_data = load_scenario("scenarios/basic_scenario.json")

# Initialize calculator
calculator = EquilibriumCalculator()
calculator.species_manager = create_species_manager_from_data(species_data)
calculator.reaction_manager = create_reaction_manager_from_data(reactions_data)
calculator.chemical_processor.load_from_data(scenario_data["chemicals"])

# Execute calculation
result = calculator.calculate()

# Extract results
ph = -math.log10(result["hp"])
concentrations = result
```

### Command Line Interface

```bash
python scripts/run_equilibrium.py --mode single      # Single calculation
python scripts/run_equilibrium.py --mode titration   # Parameter sweep
```

## Data Format

### Species Definition (`data/species.json`)
```json
{
  "initial_concentrations": {
    "hp": 1.0e-7,
    "oh_": 1.0e-7,
    "hocl": 1.0e-14,
    "ocl_": 1.0e-14
  }
}
```

### Reaction Definition (`data/reactions.json`)
```json
{
  "reactions": [
    {
      "equation": "HOCl ⇌ OCl⁻ + H⁺",
      "equilibrium_constant": 3.388e-8,
      "reactants": {"hocl": 1},
      "products": {"ocl_": 1, "hp": 1}
    }
  ]
}
```

### Chemical Scenario (`scenarios/basic_scenario.json`)
```json
{
  "chemicals": [
    {
      "chemical": "sodium hypochlorite",
      "Ions": ["nap", "ocl_"],
      "concentration": 3.465e-5,
      "stoichiometry": {"nap": 1, "ocl_": 1}
    }
  ]
}
```

## Dependencies

- Python ≥ 3.7
- NumPy ≥ 1.21.0 (for numerical operations in visualization scripts)
