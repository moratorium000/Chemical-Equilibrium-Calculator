import array

import chempy.equilibria as cpeq
import chempy.chemistry as cpch
from chempy import Reaction
from collections import OrderedDict
from chempy import Equilibrium
from chempy.chemistry import Species
from collections import defaultdict
# 죽여줘

r1 = Equilibrium(reac={'HOBr': 1}, prod={'OBr-': 1, 'H+': 1}, param=2.00e-9, name='reaction1')
r2 = Equilibrium(reac={'Br2': 1, 'H2O': 1}, prod={'HOBr': 1, 'Br-': 1, 'H+': 1}, param=6.10e-9, name='reaction2')
r3 = Equilibrium(reac={'Br2': 1, 'Br-': 1}, prod={'Br3-': 1}, param=16.1, name='reaction3')
r4 = Equilibrium(reac={'HOBr': 2}, prod={'Br2O': 1, 'H2O': 1}, param=6.31, name='reaction4')
r5 = Equilibrium(reac={'H+': 1, 'OH-': 1}, prod={'H2O': 1}, param=1.0e+14, name='autoionization')
HOBr = Species.from_formula('HOBr(aq)', ['(aq)'])
OBr_ = Species.from_formula('OBr-1', ['(aq)'])
Br_ = Species.from_formula('Br-1',['(aq)'])
Br2 = Species.from_formula('Br2', ['(aq)'])
Br3_ = Species.from_formula('Br3-', ['(aq)'])
Br2O = Species.from_formula('Br2O', ['(aq)'])
Proton = Species.from_formula('H+',['(aq)'])
Hydroxide = Species.from_formula('OH-',['(aq)'])
Water = Species.from_formula('H2O',['(l)'])

subs_new = {'HOBr': HOBr, 'OBr-': OBr_,'Br-': Br_,'Br2': Br2,'Br3-': Br3_,'Br2O':Br2O, 'H+': Proton,'OH-':Hydroxide,'H2O':Water}
# substances={r1:' HOBr OBr- H+',r2:'Br2 H2O HOBr Br- H+',r3:'Br2 Br- Br3-',r4:'HOBr Br2O H2O',r5:'H+ OH- H2O'}

equil_1 = cpeq.EqSystem(rxns=[r1, r2, r3, r4, r5],
                        substances = subs_new, name='Br_eq_system',
                        checks=('balance', 'substance_keys', 'duplicate', 'duplicate_names'))

print('\n'.join(map(str, equil_1.rxns)))
init_ = defaultdict(float, {'HOBr': 1.25e-6, 'OBr-': 1.0e-20,'Br-': 1.0e-20,'Br2': 1.0e-20,'Br3-': 1.0e-20,'Br2O':1.0e-20, 'H+': 1.0e-7,'OH-': 1.0e-7,'H2O':55.6})
x, sol, sane = equil_1.roots(init_concs=init_,varied_data = 'none',varied='none')

print(sane)


print(sorted(sol.keys()))

print(', '.join('%.3g' % v for v in x))
