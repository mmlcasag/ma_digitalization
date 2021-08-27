import os
import shutil
import utils.os as os_utils
import utils.image as image_utils
from services.base.logger import Logger

logger = Logger.__call__().get_logger()

image_extensions = ["jpg", "jpeg", "jfif", "gif", "png"]
input_folder = "input"
output_folder = "output"


def validade_input(input):
    if not input.isnumeric():
        print("Número inválido")
        exit()


print("Digite o número para criação da primeira pasta: ")
initial_number = input()
validade_input(initial_number)

print("Digite o número da última pasta para ser criada")
last_number = input()
validade_input(last_number)

list_files = os_utils.get_files_list(input_folder)

logger.info(f"{len(list_files)} Arquivo(s) encontrado(s) na pasta de input")
logger.info(f"Criando pastas iniciando em {initial_number} até {last_number}")
for i in range(int(initial_number), int(last_number) + 1):
    folder_name = os.path.join(output_folder, f"{i}")
    logger.info(f"Criando pasta de destino {folder_name}")
    os_utils.create_folder(folder_name)

    for file in list_files:
        file_name = file
        file_origin = os.path.join(input_folder, file_name)
        logger.info(f"Copiando o arquivo {file_name} para pasta de destino")
        shutil.copy(file_origin, folder_name)

        image_info = os.path.splitext(file_name)
        extension = image_info[1].replace(".", "")

        if any(extension.lower() in s for s in image_extensions):
            image_destination = os.path.join(folder_name, file_name)
            image_utils.convert_to_jpg(
                image_destination, extension, output_folder, False
            )

            image_utils.resize_image(image_destination.replace(extension, "jpg"))
