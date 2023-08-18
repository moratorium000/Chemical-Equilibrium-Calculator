import phreeqpy.iphreeqc.phreeqc_dll as phreeqc_mod


def freak_generator():
    freak_instance = phreeqc_mod.IPhreeqc()
    freak_instance.create_iphreeqc()
    return freak_instance


def database_transmitter(freak_instance, database_name="database.dat"):
    while True:
        try:
            freak_instance.load_database(database_name)
            print(freak_instance)
            break

        except phreeqc_mod.PhreeqcException:
            ''' System Access is not valid, please try again'''

    return


def input_data_transmitter(data, freak_instance):
    if isinstance(freak_instance, phreeqc_mod.IPhreeqc):
        print(True)
        freak_instance.create_iphreeqc()

    else:
        TypeError(""" is not Class \' Iphreeqc \' """)
    return


def output_data_receiver(freak_instance):
    results = freak_instance.get_selected_output_array()
    return results




