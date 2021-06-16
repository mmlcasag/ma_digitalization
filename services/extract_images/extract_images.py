import os
import sys
import utils.os as os_utils
import utils.excel as excel_utils

sys.path.append("..\..")

absolute_path = os.getcwd()

input_folder = "input"
output_folder = "output"
images_folder = "images"

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(output_folder, images_folder)

allowed_extensions = ["xlsx", "xlsb", "xlsm"]

for file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        print('INFO: PROCESSANDO O ARQUIVO "{}"'.format(file_name))

        input_path = os.path.join(absolute_path, input_folder, file_name)
        output_path = os.path.join(
            absolute_path,
            output_folder,
            images_folder,
            os_utils.get_file_name(file_name),
        )

        print('DEBUG: Arquivo de entrada "{}"'.format(input_path))
        print('DEBUG: Diretório de saída "{}"'.format(output_path))

        excel_utils.extract_images(input_path, output_path)
    except Exception as error:
        print("ERROR: {}".format(error))

print("INFO: Processo finalizado com sucesso")
