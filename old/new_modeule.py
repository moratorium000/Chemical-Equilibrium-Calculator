import main_algorithm
import numpy as np
import os


def ph_checker(data, goal, tol):
    if abs(goal + np.log10(data["hp"])) < tol or abs(goal + np.log10(data["hp"])) == 0:
        flag = True
    else:
        flag = False
    return flag

def ratio_module(ph_goal_input, lower_limit, upper_limit, tol_input):
    if "ratio_data_new.csv" in os.listdir():
        os.remove("ratio_data_new.csv")
    data_sample = open("ratio_data_new.csv", 'w')
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
    lins_scale = np.linspace(-1, 1, 100)
    lins = [3.3e-5 * 10 ** x for x in lins_scale]
#    for scale in lins_scale:
#        print(scale)
    reader = open("total_chemical_input_data_str.txt", "r")
    alltext = reader.read()
    reader.close()

    pH_range = [x for x in np.linspace(lower_limit, upper_limit, 1000)]
    k = 1
    for br_conc in lins:
        brfullstr = br_data_front + str(br_conc) + br_data_back
        for acid_conc in pH_range:
            acid_data_front_open = open("hydrobromous_front.txt", "r")
            acid_data_front = acid_data_front_open.read()
            acid_data_back_open = open("hydrobromous_back.txt", "r")
            acid_data_back = acid_data_back_open.read()
            acid_data_front_open.close()
            acid_data_back_open.close()
            acstr = acid_data_front + str(acid_conc) + acid_data_back

            writer = open("chemical_input_data.txt", "w")
            writer.write(alltext + brfullstr + acstr)
            writer.close()
            data = {}
            data_raw = main_algorithm.equilibriumcalc()

            if ph_checker(data_raw, ph_goal_input, tol_input) == True:
                if data == {}:
                    data = data_raw
                    print("pH : ", -np.log10(data['hp']))
                    line = ""
                    for values in data.values():
                        if line == "":
                            line = str(values)
                        else:
                            line = line + ", " + str(values)
                    data_sample.write(line + "\n")
                    os.remove('chemical_input_data.txt')
                    break
                else:
                    continue
            else:
                continue


        print("sample %d done" % k)
        k = k + 1
    data_sample.close()
    return



#2.0e-4,5.0e-4
ratio_module(7,1.0e-6,1.0e-4, 1.0e-2)