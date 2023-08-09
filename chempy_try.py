import chempy.equilibria as cpeq
import chempy.chemistry as cpch
from chempy import Reaction
#죽여줘

r1 = Reaction({'HOBr':1}, {'OBr-':1,'H+':1})
r2 = Reaction({'Br2':1,'H2O':1}, {'HOBr':1,'Br-':1,'H+':1})
r3 = Reaction({'Br2':1,'Br-':1}, {'Br3-':1})
r4 = Reaction({'HOBr':2}, {'Br2O':1, 'H2O':1})
r5 = Reaction({'H+':1,'OH-':1}, {'H2O':1})

subsname = {r1:['HOBr', 'OBr-', 'H+'], r2:['Br2','H2O','HOBr','Br-','H+'], r3:['Br2', 'Br-', 'Br3-'], r4:['2HOBr', 'Br2O', 'H2O'], r5:['H+', 'OH-', 'H2O']}

data1 = cpch.Substance("Cl2", 0, 'Cl_2', composition = {17 : 2}, data = {'mass' : 70.906})

# checks=('balance', 'substance_keys', 'duplicate', 'duplicate_names')
equil_1 = cpeq.EqSystem(rxns=[r1,r2,r3,r4,r5], substances = subsname, name= 'Br_eq_system', checks= ('balance','substance_keys','duplicate','duplicate_names'))