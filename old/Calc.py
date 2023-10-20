def calculator():
    fp =open('chemical_input_data.txt', 'r')
    allscript = fp.read()
    infoscript = eval(allscript)
    ionlist = []
    datadict = {}
    for cheminfo in infoscript:
        ionlist_chems = cheminfo["Ions"]
        for ion in ionlist_chems:
            if ion in ionlist:
                pass
            else:
                ionlist.append(ion)
    for ion in ionlist:
        datadict[ion] = 1.0e-14
    for cheminfo in infoscript:
        for ion in cheminfo["Ions"]:
            datadict[ion] = datadict[ion] + cheminfo["concentration"] * cheminfo["stoichiometry"][ion]


    datadict["hp"] = infoscript[-2]["concentration"]
    datadict["oh_"] = infoscript[-1]["concentration"]

    hpfinal = datadict["hp"]
    ohfinal = datadict["oh_"]

    phdata = {"hp": hpfinal, "oh_": ohfinal}
    data = [datadict, phdata]
    return data
