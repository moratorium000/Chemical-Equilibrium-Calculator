import sys
import os
import math
import time
from pathlib import Path


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from chemical_equilibrium import (
    EquilibriumCalculator,
    load_species_data,
    load_reactions_data, 
    load_scenario,
    create_species_manager_from_data,
    create_reaction_manager_from_data
)

def main():
    print("🧪 Chemical Equilibrium Calculator v1.0")
    print("=" * 50)
    
    data_dir = project_root / "data"
    scenarios_dir = project_root / "scenarios"
    
    species_file = data_dir / "species.json"
    reactions_file = data_dir / "reactions.json"
    scenario_file = scenarios_dir / "basic_scenario.json"
    
    try:
        print(" Loading data files...")
        species_data = load_species_data(str(species_file))
        reactions_data = load_reactions_data(str(reactions_file))
        scenario_data = load_scenario(str(scenario_file))
        
        print(f"   ✓ Species: {len(species_data['initial_concentrations'])} loaded")
        print(f"   ✓ Reactions: {len(reactions_data['reactions'])} loaded")
        print(f"   ✓ Chemicals: {len(scenario_data['chemicals'])} loaded")
        
    except FileNotFoundError as e:
        print(f" Error: {e}")
        print("\n Make sure you have created the following files:")
        print(f"   - {species_file}")
        print(f"   - {reactions_file}")
        print(f"   - {scenario_file}")
        return 1
    
    except Exception as e:
        print(f" Error loading data: {e}")
        return 1
    
    try:
        print("\n  Initializing calculator...")
        calculator = EquilibriumCalculator()
        
        species_manager = create_species_manager_from_data(species_data)
        calculator.species_manager = species_manager
        
        reaction_manager = create_reaction_manager_from_data(reactions_data)
        calculator.reaction_manager = reaction_manager
        
        calculator.chemical_processor.load_from_data(scenario_data["chemicals"])
        
        print(f"   ✓ System initialized with {len(species_manager)} species")
        print(f"   ✓ System initialized with {len(reaction_manager)} reactions")
        
        print("\n Running equilibrium calculation...")
        start_time = time.time()
        
        result = calculator.calculate()
        
        end_time = time.time()
        calculation_time = end_time - start_time
        
        print(f"\n Calculation completed in {calculation_time:.3f} seconds")
        print("\n Results:")
        print("-" * 30)
        
        hp_concentration = result.get("hp", 1e-14)
        oh_concentration = result.get("oh_", 1e-14)
        ph = -math.log10(hp_concentration) if hp_concentration > 0 else float('nan')
        poh = -math.log10(oh_concentration) if oh_concentration > 0 else float('nan')
        
        print(f" pH: {ph:.2f}")
        print(f" pOH: {poh:.2f}")
        print(f" [H⁺]: {hp_concentration:.2e} M")
        print(f" [OH⁻]: {oh_concentration:.2e} M")
        print(f"\n Major Species Concentrations:")
        major_species = [
            ('hocl', 'HOCl'),
            ('ocl_', 'OCl⁻'), 
            ('hobr', 'HOBr'),
            ('obr_', 'OBr⁻'),
            ('br_', 'Br⁻'),
            ('cl_', 'Cl⁻'),
            ('nap', 'Na⁺')
        ]
        
        for species_name, formula in major_species:
            if species_name in result:
                concentration = result[species_name]
                print(f"   {formula:>6}: {concentration:.2e} M")
        
        print(f"\n🔬 Minor Species (> 1e-12 M):")
        minor_species = [
            ('cl2', 'Cl₂'),
            ('br2', 'Br₂'),
            ('cl3_', 'Cl₃⁻'),
            ('br3_', 'Br₃⁻'),
            ('brcl', 'BrCl'),
            ('brcl2_', 'BrCl₂⁻'),
            ('br2cl_', 'Br₂Cl⁻'),
            ('cl2o', 'Cl₂O'),
            ('br2o', 'Br₂O'),
            ('brocl', 'BrOCl')
        ]
        
        minor_found = False
        for species_name, formula in minor_species:
            if species_name in result:
                concentration = result[species_name]
                if concentration > 1e-12:
                    print(f"   {formula:>8}: {concentration:.2e} M")
                    minor_found = True
        
        if not minor_found:
            print("   (No significant minor species)")
        

        print(f"\n  System Validation:")
        
        kw_product = hp_concentration * oh_concentration
        kw_error = abs(kw_product - 1e-14) / 1e-14
        print(f"   Kw constraint: {kw_product:.2e} (error: {kw_error:.1%})")
        
        positive_charge = (
            result.get("hp", 0) + 
            result.get("nap", 0)
        )
        negative_charge = (
            result.get("oh_", 0) + 
            result.get("cl_", 0) + 
            result.get("br_", 0) + 
            result.get("ocl_", 0) + 
            result.get("obr_", 0) + 
            result.get("cl3_", 0) + 
            result.get("br3_", 0) + 
            result.get("brcl2_", 0) + 
            result.get("br2cl_", 0)
        )
        charge_balance = abs(positive_charge - negative_charge)
        print(f"   Charge balance error: {charge_balance:.2e} M")
        
        print(f"\n Summary:")
        print(f"   • Final pH: {ph:.2f}")
        print(f"   • Dominant chlorine species: {'HOCl' if result.get('hocl', 0) > result.get('ocl_', 0) else 'OCl⁻'}")
        print(f"   • Dominant bromine species: {'HOBr' if result.get('hobr', 0) > result.get('obr_', 0) else 'OBr⁻'}")
        print(f"   • Calculation time: {calculation_time:.3f} s")
        
        return 0
        
    except Exception as e:
        print(f" Calculation error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_hbr_titration():
    print("\n" + "="*50)
    print(" HBr Titration Analysis")
    print("="*50)
    
    data_dir = project_root / "data"
    scenarios_dir = project_root / "scenarios"
    species_file = data_dir / "species.json"
    reactions_file = data_dir / "reactions.json"
    base_scenario_file = scenarios_dir / "basic_scenario.json"
    
    try:
        species_data = load_species_data(str(species_file))
        reactions_data = load_reactions_data(str(reactions_file))
        base_scenario = load_scenario(str(base_scenario_file))
        
        import numpy as np
        hbr_concentrations = np.linspace(2.0e-5, 1.4e-4, 10)
        
        print(f" Testing {len(hbr_concentrations)} HBr concentrations...")
        print(f"   Range: {hbr_concentrations[0]:.1e} to {hbr_concentrations[-1]:.1e} M")
        
        results = []
        
        for i, hbr_conc in enumerate(hbr_concentrations):
            scenario = base_scenario.copy()
            scenario["chemicals"] = base_scenario["chemicals"].copy()
            hbr_chemical = {
                "chemical": "hydrobromous acid",
                "Ions": ["hp", "br_"],
                "concentration": hbr_conc,
                "stoichiometry": {
                    "hp": 1,
                    "br_": 1
                }
            }
            scenario["chemicals"].append(hbr_chemical)
            calculator = EquilibriumCalculator()
            species_manager = create_species_manager_from_data(species_data)
            calculator.species_manager = species_manager
            reaction_manager = create_reaction_manager_from_data(reactions_data)
            calculator.reaction_manager = reaction_manager
            calculator.chemical_processor.load_from_data(scenario["chemicals"])
            result = calculator.calculate()
            
            ph = -math.log10(result.get("hp", 1e-14))
            results.append({
                'hbr_concentration': hbr_conc,
                'ph': ph,
                'hp': result.get("hp", 0),
                'oh_': result.get("oh_", 0),
                'hocl': result.get("hocl", 0),
                'ocl_': result.get("ocl_", 0),
                'hobr': result.get("hobr", 0),
                'br_': result.get("br_", 0)
            })
            
            print(f"   {i+1:2d}. [HBr] = {hbr_conc:.1e} M → pH = {ph:.2f}")
        

        output_file = project_root / "outputs" / "hbr_titration_results.csv"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write("HBr_concentration,pH,H+,OH-,HOCl,OCl-,HOBr,Br-\n")
            for result in results:
                f.write(f"{result['hbr_concentration']:.2e},")
                f.write(f"{result['ph']:.3f},")
                f.write(f"{result['hp']:.2e},")
                f.write(f"{result['oh_']:.2e},")
                f.write(f"{result['hocl']:.2e},")
                f.write(f"{result['ocl_']:.2e},")
                f.write(f"{result['hobr']:.2e},")
                f.write(f"{result['br_']:.2e}\n")
        
        print(f"\n Results saved to: {output_file}")
        print(f" pH range: {min(r['ph'] for r in results):.2f} - {max(r['ph'] for r in results):.2f}")
        
    except Exception as e:
        print(f" Titration error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chemical Equilibrium Calculator")
    parser.add_argument("--mode", choices=["single", "titration"], default="single",
                       help="Calculation mode")
    
    args = parser.parse_args()
    
    if args.mode == "single":
        exit_code = main()
        sys.exit(exit_code)
    elif args.mode == "titration":
        run_hbr_titration()
        sys.exit(0)