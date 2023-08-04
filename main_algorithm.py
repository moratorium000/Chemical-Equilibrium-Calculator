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
    leftvar = 1
    rightvar = 1
    if constspacepar['left'] == [] or constspacepar['right'] == []:
        if constspacepar['left'] == []:
            leftvar = 1
            for pright in constspacepar['left']:
                valueright = valuespacepar[pright]
                indexright = constspacepar['right'].index(pright)
                rightvar = rightvar * (valueright + xinput * constspacepar['metadata']['right'][indexright])
        else:
            rightvar = 1
            for pleft in constspacepar['left']:
                valueleft = valuespacepar[pleft]
                indexleft = constspacepar['left'].index(pleft)
                leftvar = leftvar * (valueleft - xinput * constspacepar['metadata']['left'][indexleft])



    else:
        for pleft in constspacepar['left']:
            valueleft = valuespacepar[pleft]
            indexleft = constspacepar['left'].index(pleft)
            leftvar = leftvar * (valueleft - xinput * constspacepar['metadata']['left'][indexleft])
        for pright in constspacepar['right']:
            valueright = valuespacepar[pright]
            indexright = constspacepar['right'].index(pright)
            rightvar = rightvar * (valueright + xinput * constspacepar['metadata']['right'][indexright])

    try:
        q = constspacepar['largek'] - (rightvar / leftvar)
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


def solving(constspacepar, valuespacepar):
    maxiter = 30
    tol = 1.00e-15
    if kfunction(constspacepar, 0, valuespacepar, 1) == None:
        print('none run')
        return 0
    else:
        if abs(kfunction(constspacepar, 0, valuespacepar, 1)) < tol:
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
                if kfunction(constspacepar, 0, valuespacepar, 1) > 0:
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
    valuespace_true["hp"] = inputphdata["hp"]
    valuespace_true["oh_"] = inputphdata["oh_"]
    for chemicals_input_ in inputvaluedata.keys():
        if chemicals_input_ == "hp" or chemicals_input_ == "oh_":
            pass
        else:
            valuespace_true[chemicals_input_] = inputvaluedata[chemicals_input_]

    for timer in range(10):
        for i in constspace_true:
            if valuespace_true['hp']/valuespace_true['oh_'] > 1e4 or valuespace_true['hp']/valuespace_true['oh_'] < 1e4:
                if valuespace_true['hp']/valuespace_true['oh_']:
                    valuespace_true['oh_'] = 1.0e-14/valuespace_true['hp']
                else:
                    valuespace_true['hp'] = 1.0e-14 / valuespace_true['oh_']
            variant_x = solving(i, valuespace_true)
            leftkeys_ = i['left']
            rightkeys_ = i['right']
            for pleft in leftkeys_:
                indexleft = i['left'].index(pleft)

                valuespace_true[pleft] = valuespace_true[pleft] - variant_x * i['metadata']['left'][indexleft]
            for pright in rightkeys_:
                indexright = i['right'].index(pright)
                valuespace_true[pright] = valuespace_true[pright] + variant_x * i['metadata']['right'][indexright]
    if valuespace_true['hp'] / valuespace_true['oh_'] > 1e4 or valuespace_true['hp'] / valuespace_true['oh_'] < 1e-4:
        if valuespace_true['hp'] / valuespace_true['oh_'] > 1e4:
            valuespace_true['oh_'] = 1.0e-14 / valuespace_true['hp']
        else:
            valuespace_true['hp'] = 1.0e-14 / valuespace_true['oh_']
    return valuespace_true





#finaldata = equilibriumcalc()
#print('\n\nfinal data : ', finaldata)
#fp = open('valuespace_output_1.txt', 'w')
#for s in finaldata:
#   print(s,' : ', finaldata[s])
#  fp.write(str(s) + ' : ' + str(finaldata[s]) + '\n')
#
#fp.close()