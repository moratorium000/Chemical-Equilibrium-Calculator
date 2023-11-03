import copy
from Calc import calculator
class valuespace_c:
    def __init__(self, valuespace, variantspace, constantspace):
        self.valuespace = valuespace
        self.variantspace = variantspace
        self.constantspace = constantspace
        
    def variant_fixer(self, variants):
        keys_ = variants.keys()
        for key in keys_:
            variants_input = variants[key]
            self.valuespace[key] = self.valuespace[key] + variants_input
        return
def kfunction(constspacepar, xinput, valuespacepar, index1_):
#   kfunction is a function to calculate Q, reaction coefficient, in manner of difference with K, equilibrium constant
#   zerodivision error of the fuction results in return value None, the
#
#
    leftvar = 1
    rightvar = 1
    if constspacepar['left'] == [] or constspacepar['right'] == []:
        if constspacepar['left'] == []:
            leftvar = 1
            for pright in constspacepar['left']:
                valueright = valuespacepar[pright]
                indexright = constspacepar['right'].index(pright)
                rightvar = rightvar * ((valueright + xinput * constspacepar['metadata']['right'][indexright])**constspacepar['metadata']['right'][indexright])
        else:
            rightvar = 1
            for pleft in constspacepar['left']:
                valueleft = valuespacepar[pleft]
                indexleft = constspacepar['left'].index(pleft)
                leftvar = leftvar * ((valueleft - xinput * constspacepar['metadata']['left'][indexleft])** constspacepar['metadata']['left'][indexleft])



    else:
        for pleft in constspacepar['left']:
            valueleft = valuespacepar[pleft]
            indexleft = constspacepar['left'].index(pleft)
            leftvar = leftvar * ((valueleft - xinput * constspacepar['metadata']['left'][indexleft])** constspacepar['metadata']['left'][indexleft])
        for pright in constspacepar['right']:
            valueright = valuespacepar[pright]
            indexright = constspacepar['right'].index(pright)
            rightvar = rightvar * ((valueright + xinput * constspacepar['metadata']['right'][indexright])** constspacepar['metadata']['right'][indexright])

    try:
        q = (constspacepar['largek'] - (rightvar / leftvar))/constspacepar['largek']
        return q
    except ZeroDivisionError:
        if index1_ == 1:
            return None
        else:
            hp = open("bug_report.txt",'w')
            bug_report = hp.write(str(valuespacepar))
            hp.close()
            print('WHAT THE')
            return 'wt'

def ph_calculator_(cohp,cxhp,cooh,cxoh):
#
#
#
#
    beta = cohp + cxhp + cooh + cxoh
    gamma = (cohp + cxhp) * (cooh + cxoh)- 1e-14
    root1 = (beta + (beta**2-4*gamma)**0.5)/2
    root2 = (beta - (beta**2-4*gamma)**0.5)/2
#    print("root1 :" , root1)
#    print("root2 :" , root2)
    if root1 - (cohp + cxhp) > 0 or root1 - (cooh + cxoh) > 0:
        true_root = root2
    else:
        true_root = root1
#    print("true_root : ", true_root)
    cfhp = cohp + cxhp - true_root
    cfoh = cooh + cxoh - true_root
    return [cfhp, cfoh]

def solving(constspacepar, valuespacepar):
# solver mechanism is consisted with three parts: pretreatment of the data, calling kfunction to calculate the value and iteration of bisection mechanism



    maxiter = 200
    tol = 1.00e-7
#    print("valuespace_true[hp]",valuespacepar["hp"])
    if kfunction(constspacepar, 0, valuespacepar, 1) == None:
        print('none run')
        return 0
    else:
        if abs(kfunction(constspacepar, 0, valuespacepar, 1))/constspacepar["largek"] < tol:
            return 0
        else:
            if constspacepar['left'] == [] or constspacepar['right'] == []:
                if constspacepar['left'] == []:
                    xmaxima = 0
                    rightvalue = []
                    for keyright in constspacepar['right']:
                        rightindex = constspacepar['right'].index(keyright)
                        rightvalue.append(
                            valuespacepar[keyright] / constspacepar['metadata']['right'][rightindex])
                    xminima = - min(rightvalue)


                else:
                    xminima = 0
                    leftvalue = []
                    for keyleft in constspacepar['left']:
                        leftindex = constspacepar['left'].index(keyleft)
                        leftvalue.append(valuespacepar[keyleft] / constspacepar['metadata']['left'][leftindex])

                    xmaxima = min(leftvalue)

            else:
                if kfunction(constspacepar, 0, valuespacepar, 1)/constspacepar["largek"] > 0:
                    xminima = 0
                    leftvalue = []
                    for keyleft in constspacepar['left']:
                        leftindex = constspacepar['left'].index(keyleft)
                        leftvalue.append(valuespacepar[keyleft] / constspacepar['metadata']['left'][leftindex])

                    xmaxima = min(leftvalue)

                else:
                    xmaxima = 0
                    rightvalue = []
                    for keyright in constspacepar['right']:
                        rightindex = constspacepar['right'].index(keyright)
                        rightvalue.append(valuespacepar[keyright] / constspacepar['metadata']['right'][rightindex])
                    xminima = - min(rightvalue)




    for counter in range(maxiter):
        fminima = kfunction(constspacepar, xminima, valuespacepar, 0)
        xm = (xminima+xmaxima)/2
        value_xm = kfunction(constspacepar, xm, valuespacepar, 0)

        err = abs(xmaxima-xminima)/2
        if abs(value_xm) < tol and abs(err) < tol:
            x = xm
            return x
        else:
            if value_xm * fminima > 0:
                xminima = xm

            else:
                if value_xm == 0:
                    return xm
                else:
                    xmaxima = xm
    return xm

def equilibriumcalc():
    fp = open('valuespace.txt', 'r')
    lines = fp.readline()
    valuespace_input = eval(lines)
    lines = fp.readline()
    variantspace_input = eval(lines)
    lines = fp.read()
    constantspace_input = eval(lines)
    
    valuespace_inst = valuespace_c(valuespace_input, variantspace_input, constantspace_input)
    valuespace_true = copy.deepcopy(valuespace_inst.valuespace)
    constspace_true = copy.deepcopy(valuespace_inst.constantspace)
    chemical_input = calculator()
    inputvaluedata = chemical_input[0]
    inputphdata = chemical_input[1]
    for chemicals_input_ in inputvaluedata.keys():
        if chemicals_input_ == "hp" or chemicals_input_ == "oh_":
            pass
        else:
            valuespace_true[chemicals_input_] = inputvaluedata[chemicals_input_]
    hp_new, oh_new = ph_calculator_(valuespace_true["hp"], inputphdata["hp"], valuespace_true["oh_"], inputphdata["oh_"])
    valuespace_true["hp"] = hp_new
    valuespace_true["oh_"] = oh_new
#    print("hp_new :",hp_new)
#    print("oh_new :",oh_new)
    for timer in range(500):
        for i in constspace_true:
#            print("valuespace_true hp :", valuespace_true["hp"])
#           if valuespace_true['hp']/valuespace_true['oh_'] > 1e4 or valuespace_true['hp']/valuespace_true['oh_'] < 1e4:
#                if valuespace_true['hp']/valuespace_true['oh_']:
#                    valuespace_true['oh_'] = 1.0e-14/valuespace_true['hp']
#                else:
#                    valuespace_true['hp'] = 1.0e-14 / valuespace_true['oh_']
            variant_x = solving(i, valuespace_true)
            leftkeys_ = i['left']
            rightkeys_ = i['right']
            for pleft in leftkeys_:

                indexleft = i['left'].index(pleft)
                valuespace_true[pleft] = valuespace_true[pleft] - variant_x * i['metadata']['left'][indexleft]
            for pright in rightkeys_:
                indexright = i['right'].index(pright)
                valuespace_true[pright] = valuespace_true[pright] + variant_x * i['metadata']['right'][indexright]
            valuespace_true["oh_"] = 1.0e-14 / valuespace_true["hp"]
#            print("valuespace_true[hp]",valuespace_true["hp"])
    print(valuespace_true)

    return valuespace_true

"""    if valuespace_true['hp'] / valuespace_true['oh_'] > 1e4 or valuespace_true['hp'] / valuespace_true['oh_'] < 1e-4:
        if valuespace_true['hp'] / valuespace_true['oh_'] > 1e4:
            valuespace_true['oh_'] = 1.0e-14 / valuespace_true['hp']
        else :
            valuespace_true['hp'] = 1.0e-14 / valuespace_true['oh_'] """





if __name__ == "__main__":
    finaldata = equilibriumcalc()
    print('\n\nfinal data : ', finaldata)
    fp = open('valuespace_output_1.txt', 'w')
    for s in finaldata:
        print(s,' : ', finaldata[s])
        fp.write(str(s) + ' : ' + str(finaldata[s]) + '\n')
    fp.close()