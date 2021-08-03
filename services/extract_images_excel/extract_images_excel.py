import os

import utils.os as os_utils
import utils.excel as excel_utils
import utils.image as image_utils

from services.base.logger import Logger

logger = Logger.__call__().get_logger()

absolute_path = os.getcwd()

input_folder = "input"
output_folder = "output"
images_folder = "images"

os_utils.create_folder(input_folder)
os_utils.create_folder(input_folder, images_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(output_folder, images_folder)

allowed_extensions = ["xlsx", "xlsb", "xlsm", "xls"]

logger.info("PROCESSO DE EXTRAÇÃO DE IMAGENS EM ARQUIVOS EXCEL")
logger.info(
    "Procurando por arquivos Excel no diretório de entrada para iniciar a extração"
)

for file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        logger.info('Encontrado o arquivo "{}"'.format(file_name))

        input_path = os.path.join(absolute_path, input_folder, file_name)
        output_path = os.path.join(
            absolute_path,
            output_folder,
            images_folder,
            os_utils.get_file_name(file_name),
        )

        logger.info('Arquivo de entrada "{}"'.format(input_path))
        logger.info('Diretório de saída "{}"'.format(output_path))

        logger.info("Iniciando a extração das imagens do arquivo")
        excel_utils.extract_images_excel(input_path, output_path)
        logger.info("Extração das imagens do arquivo finalizada")
    except Exception as error:
        logger.error("{} ao tentar processar o arquivo {}".format(error, file_name))

logger.info("PROCESSO DE SEPARAÇÃO DE IMAGENS EM PASTAS")
logger.info("Procurando por arquivos no diretório de imagens para iniciar a separação")

try:
    logger.info("Iniciando o processo de separação das imagens")

    input_folder = os.path.join("input", "images")
    output_folder = os.path.join("output", "images")

    logger.info('Diretório de entrada "{}"'.format(input_folder))
    logger.info('Diretório de saída "{}"'.format(output_folder))

    image_utils.organize_images(input_folder, output_folder)

    logger.info("Processo de separação das imagens finalizado")
except Exception as error:
    logger.error("{} ao tentar separar as imagens".format(error))

logger.info("Processo finalizado com sucesso.")
done = str(input("Pressione ENTER para encerrar..."))
