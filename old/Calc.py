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
        if ion != "hp" and ion != "oh_":
            datadict[ion] = 0
        else:
            datadict[ion] = 1.0e-7
    for cheminfo in infoscript:
        for ion in cheminfo["Ions"]:
            datadict[ion] = datadict[ion] + cheminfo["concentration"] * cheminfo["stoichiometry"][ion]
            if ion == "hp" or ion == "oh_":
                if ion == "hp":
                    datadict["oh_"] = 1.0e-14 / datadict["hp"]
                else:
                    datadict["hp"] = 1.0e-14 / datadict["oh_"]

    hpfinal = datadict["hp"]
    ohfinal = datadict["oh_"]

    phdata = {"hp": hpfinal, "oh_": ohfinal}
    data = [datadict, phdata]
    return data
