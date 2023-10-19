def input_data_control(data_script):
    import os
    if not os.path.isdir('input_data'):
        os.mkdir('input_data')
    qpi_writer = open("/input_data/input_data.qpi", "w")
    qpi_writer.write(data_script)
    return None

