from system_runtime import *
from data_pretreating import *
import numpy as np
from output_post_treating import *

def ph_generator(starting=7., end=7., scale=100):
    space_project = np.linspace(starting, end, scale)
    count =0
    while count < scale:
        count += 1
        yield space_project[count-1]

def input_str_generator(adress="input_freak.txt", phdata=7.):
    reading_opener_front = open("input_freak_front.txt", 'r')
    reading_opener_back = open("input_freak_back.txt", 'r')
    str_front = reading_opener_front.read()
    str_back = reading_opener_back.read()
    str_input = str_front + str(phdata) + str_back
    reading_opener_front.close()
    reading_opener_back.close()
    str_writer = open(adress, 'w')
    str_writer.write(str_input)
    str_writer.close()
    return


def object_creator(key_list):

    return data_object


def ph_main(starting, end, scale):
    gen_x = ph_generator(starting=starting,end=end,scale=scale)
    #keys_list 는 사실
    keys_list = []
    data_object = {}
    freak_data_output = {}

    for index1 in gen_x:
        input_str_generator(adress='input_freak.txt', phdata=index1)
        freak_instance = system_base.freak_generator()
        system_base.database_transmitter(freak_instance=freak_instance,database_name="phreeqc.dat")
        reader = open('input_freak.txt','r')
        texts = reader.read()
        system_base.input_data_transmitter(texts,freak_instance=freak_instance)
        for key in keys_list:
            if data_object.get(key,-1) is -1:
                data_object[key] = [freak_data_output[key]]
            else:
                data_object[key] = data_object[key] + [freak_data_output[key]]
    output_finaldata = data_object
    alpha = True
    for key in keys_list:
        alpha = alpha and (len(data_object[key]) == scale)
    if alpha is not True:
        Exception("""LengthError""")

    dataframe1 = database_creator(output_finaldata)
    database_writer(dataframe=dataframe1)

    return


if __name__ == '__main__':
    ph_main(4,12,400)

