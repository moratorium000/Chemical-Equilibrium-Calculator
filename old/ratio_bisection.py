import main_algorithm
import numpy as np
import os
import copy


def ph_checker(data, goal, tol):
    if abs(goal + np.log10(data["hp"])) < tol or abs(goal + np.log10(data["hp"])) == 0:
        flag = True
    else:
        flag = False
    return flag

def ratio_module(ph_goal_input, lower_limit, upper_limit, tol_input, iteration_for_ph):
    if "ratio_data_new.csv" in os.listdir():
        os.remove("ratio_data_new.csv")
    if 'chemical_input_data.txt' in os.listdir():
        os.remove('chemical_input_data.txt')
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
#    lins_scale = np.linspace(-1, 1, 21)
#    lins = [3.3e-5 * 10 ** x for x in lins_scale]
    lins = [3.3e-6 * x for x in range(0, 21, 1)]

#    for scale in lins_scale:
#        print(scale)
    reader = open("total_chemical_input_data_str.txt", "r")
    alltext = reader.read()
    reader.close()
    ph_minmax = [lower_limit, upper_limit]
    ph_minmax_initial = copy.deepcopy(ph_minmax)


    k = 1
    for br_conc in lins:
        brfullstr = br_data_front + str(br_conc) + br_data_back
        line = ""
        for counter in range(iteration_for_ph):
            xm = (ph_minmax[0] + ph_minmax[1]) / 2
            base_conc = 10**xm
            acid_conc = 1.0e-14 / base_conc
            print("xm", acid_conc)

            acid_data_front_open = open("hydrobromous_front.txt", "r")
            acid_data_front = acid_data_front_open.read()
            acid_data_back_open = open("hydrobromous_back.txt", "r")
            acid_data_back = acid_data_back_open.read()
            acid_data_front_open.close()
            acid_data_back_open.close()
            base_data_front_open = open("base_front.txt", "r")
            base_data_front = base_data_front_open.read()
            base_data_back_open = open("base_back.txt", "r")
            base_data_back = base_data_back_open.read()
            base_data_front_open.close()
            base_data_front_open.close()

            acstr = acid_data_front + str(acid_conc) + acid_data_back
            base_fullstr = base_data_front + str(base_conc) + base_data_back

            writer = open("chemical_input_data.txt", "w")
            writer.write("[" + alltext + brfullstr + acstr + base_fullstr + "]")
            writer.close()
            data_raw = main_algorithm.equilibriumcalc()

            if -np.log10(data_raw['hp']) == ph_goal_input:
                data_sample.write(data_raw)

                break
            else:
                if -np.log10(data_raw['hp']) > ph_goal_input:
                    if abs(np.log10(data_raw['hp']) + ph_goal_input) < tol_input:
                        data = data_raw.values()
                        for values in data:
                            if line == "":
                                line = str(values)
                            else:
                                line = line + ", " + str(values)
                        os.remove('chemical_input_data.txt')
                        data_sample.write(line + "\n")
                        print("sample done")
                        ph_minmax = [lower_limit, upper_limit]
                        break

                    else:
                        ph_minmax = [ph_minmax[0], xm]
                        print(ph_minmax)
                else:
                    if abs(np.log10(data_raw['hp']) + ph_goal_input) < tol_input:
                        data = data_raw.values()
                        for values in data:
                            if line == "":
                                line = str(values)
                            else:
                                line = line + ", " + str(values)
                        os.remove('chemical_input_data.txt')
                        data_sample.write(line + "\n")
                        print("sample done")
                        ph_minmax = [lower_limit, upper_limit]
                        break
                    else:
                        ph_minmax = [xm, ph_minmax[1]]
                        print(ph_minmax)
            if counter == iteration_for_ph - 1:
                data = data_raw.values()
                for values in data:
                    if line == "":
                        line = str(values)
                    else:
                        line = line + ", " + str(values)
                os.remove('chemical_input_data.txt')
                data_sample.write(line + "\n")
                ph_minmax = [lower_limit, upper_limit]
                print("sample done")


    data_sample.close()
    return



#2.0e-4,5.0e-4
ratio_module(10,-12.0, 0.0, 1.0e-3,500)