import copy
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
def kfunction(constspacepar, xinput, valuespacepar):
    leftvar = 1
    rightvar = 1

    for pleft in constspacepar['left']:
        valueleft = valuespacepar[pleft]
        indexleft = constspacepar['left'].index(pleft)
        leftvar = leftvar * (valueleft - xinput * constspacepar['metadata']['left'][indexleft])
    for pright in constspacepar['right']:
        valueright = valuespacepar[pright]
        indexright = constspacepar['right'].index(pright)
        rightvar = rightvar * (valueright + xinput * constspacepar['metadata']['right'][indexright])


    try:
        q = 1 - rightvar/(leftvar*constspacepar['largek'])
        return q
    except ZeroDivisionError:
        return -10000000000
def solving(constspacepar, valuespacepar):
    maxiter = 50
    tol = 1.00e-8
    if kfunction(constspacepar, 0, valuespacepar) > 0:
        xminima = 0
        leftvalue = []
        for keyleft in constspacepar['left']:
            leftindex = constspacepar['left'].index(keyleft)
            leftvalue.append(valuespacepar[keyleft]/constspacepar['metadata']['left'][leftindex])

        xmaxima = min(leftvalue)
    else:
        if kfunction(constspacepar, 0, valuespacepar) == constspacepar['largek']:
            return 0
        else:
            xmaxima = 0
            rightvalue = []
            for keyright in constspacepar['right']:
                rightindex = constspacepar['right'].index(keyright)
                rightvalue.append(valuespacepar[keyright] / constspacepar['metadata']['right'][rightindex])
            xminima = - min(rightvalue)

    for counter in range(maxiter):

        fminima = kfunction(constspacepar, xminima, valuespacepar)
        xm = (xminima+xmaxima)/2

        value_xm = kfunction(constspacepar, xm, valuespacepar)
        err = (xmaxima-xminima)/2
        if abs(value_xm) < tol and abs(err) < tol:
            x = xm
            return x
        else:
            if value_xm * fminima > 0:

                xminima = xm
            else:
                if value_xm * fminima == 0:

                    return xm
                else:

                    xmaxima = xm

    return xm

def main():
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

    for timer in range(1000):
        for i in constspace_true:
            variant_x = solving(i, valuespace_true)
            leftkeys_ = i['left']
            rightkeys_ = i['right']
            for pleft in leftkeys_:
                indexleft = i['left'].index(pleft)

                valuespace_true[pleft] = valuespace_true[pleft] - variant_x * i['metadata']['left'][indexleft]
            for pright in rightkeys_:
                indexright = i['right'].index(pright)
                valuespace_true[pright] = valuespace_true[pright] + variant_x * i['metadata']['right'][indexright]

            valuespace_true["oh_"] = (1.00e-14) / valuespace_true["hp"]
        print('trial no.%d :' % timer, valuespace_true)


# 값호출, 값공간, 변수공간, 상수공간


    return valuespace_true





finaldata = main()
print('\n\nfinal data : ', finaldata)
fp = open('valuespace_output.txt', 'w')
for s in finaldata:
    print(s,' : ', finaldata[s])
    fp.write(str(s) + ' : ' + str(finaldata[s]) + '\n')

fp.close()