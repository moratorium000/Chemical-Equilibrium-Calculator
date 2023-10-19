import main_algorithm
import numpy as np
import os

def main():
    if "ratio_data.csv" in os.listdir():
        os.remove("ratio_data.csv")
    data_sample = open("ratio_data.csv", 'w')
    data_sample.write("\n")
    names_open = open("names.txt", "r")
    data_sample.write(names_open.read() + "\n")
    names_open.close()
    br_data_front_open = open("sodium_bromide_front.txt", "r")
    br_data_front = br_data_front_open.read()
    br_data_back_open = open("sodium_bromide_back.txt", "r")
    br_data_back = br_data_back_open.read()
    br_data_front_open.close()
    br_data_back_open.close()
#    lins = np.linspace(3.3e-6, 3.3e-4,100)
    lins_scale = np.linspace(-1, 1, 100)
    lins = [3.3e-5 * 10 ** x for x in lins_scale]
    for scale in lins_scale:
        print(scale)
    reader = open("br_chemical_input_data_str.txt", "r")
    alltext = reader.read()
    reader.close()
    k = 1
    for br_conc in lins:
        fullstr = br_data_front + str(br_conc) + br_data_back
        writer = open("chemical_input_data.txt", "w")
        writer.write(alltext + fullstr)
        writer.close()
        data = main_algorithm.equilibriumcalc()
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