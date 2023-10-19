import equil_test
import numpy as np
import os

def main():
    if "ph_data.csv" in os.listdir():
        os.remove("ph_data.csv")
    data_sample = open("ph_data.csv", 'w')
    data_sample.write("\n")
    names_open = open("names.txt", "r")
    data_sample.write(names_open.read() + "\n")
    names_open.close()
    acid_data_front_open = open("hydrobromous_front.txt", "r")
    acid_data_front = acid_data_front_open.read()
    acid_data_back_open = open("hydrobromous_back.txt", "r")
    acid_data_back = acid_data_back_open.read()
    acid_data_front_open.close()
    acid_data_front_open.close()
    lins = np.linspace(1.0e-5, 1.00e-4, 10)
    reader = open("chemical_input_data_str.txt", "r")
    alltext = reader.read()
    reader.close()
    k = 1
    for acid_conc in lins:
        fullstr = acid_data_front + str(acid_conc) + acid_data_back
        writer = open("chemical_input_data.txt", "w")
        writer.write(alltext+fullstr)
        writer.close()
        data = equil_test.equilibriumcalc()
        print("pH   : ", -np.log10(data["hp"]))
        line = ""
        for values in data.values():
            if line == "":
                line = str(values)
            else:
                line = line + ", " + str(values)
        data_sample.write(line + "\n")
        os.remove('chemical_input_data.txt')
        print("sample %d done" % k)
        k = k + 1
    data_sample.close()
    return

main()