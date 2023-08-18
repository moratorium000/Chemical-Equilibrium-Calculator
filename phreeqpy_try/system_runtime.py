import system_base
from data_pretreating import *
from output_post_treating import *


def main():
    freak_instance = system_base.freak_generator()
    system_base.database_transmitter(freak_instance=freak_instance, database_name="database.dat")
    output_raw = system_base.output_data_receiver(freak_instance)
    database_writer(output_raw)
    return


if __name__ == '__main__':
    main()

