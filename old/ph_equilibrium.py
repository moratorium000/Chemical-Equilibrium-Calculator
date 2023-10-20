import main_algorithm
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

    base_data_front_open = open("base_front.txt", "r")
    base_data_front = base_data_front_open.read()
    base_data_back_open = open("base_back.txt", "r")
    base_data_back = base_data_back_open.read()
    base_data_front_open.close()
    base_data_front_open.close()

    lins_log = np.linspace(-5, -2, 10000)
    lins = (10** x for x in lins_log)
    reader = open("chemical_input_data_str.txt", "r")
    alltext = reader.read()
    reader.close()
    k = 1
    for acid_conc in lins:
        base_conc = 1.0e-14/acid_conc
        acid_fullstr = acid_data_front + str(acid_conc) + acid_data_back
        base_fullstr = base_data_front + str(base_conc) + base_data_back
        writer = open("chemical_input_data.txt", "w")
        writer.write("[" + alltext + acid_fullstr + base_fullstr + "]")
        writer.close()
        data = main_algorithm.equilibriumcalc()
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