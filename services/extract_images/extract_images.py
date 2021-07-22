import os
import re

import utils.os as os_utils
import utils.excel as excel_utils

from services.base.logger import Logger
from services.base.images_handler import ImageHandler

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
        excel_utils.extract_images(input_path, output_path)
        logger.info("Extração das imagens do arquivo finalizada")
    except Exception as error:
        logger.error("{} ao tentar processar o arquivo {}".format(error, file_name))

logger.info("PROCESSO DE SEPARAÇÃO DE IMAGENS EM PASTAS")
logger.info("Procurando por arquivos no diretório de imagens para iniciar a separação")

try:
    input_folder = os.path.join("input", "images")
    output_folder = os.path.join("output", "images")

    logger.info('Diretório de entrada "{}"'.format(input_path))
    logger.info('Diretório de saída "{}"'.format(output_path))

    img_handler = ImageHandler(input_folder, output_folder)

    logger.info("Iniciando a separação das imagens")

    img_handler.move_images(
        lambda img_name: img_name.find("Lote") != -1,
        lambda img_name: img_name.replace("Lote", "").strip().split("_")[0],
    )

    img_handler.move_images(
        lambda img_name: img_name.find("LOTE") != -1,
        lambda img_name: re.search(r"\d+", img_name)[0].lstrip("0"),
    )

    img_handler.move_images(
        lambda img_name: img_name.find("lt") != -1,
        lambda img_name: re.search(r"lt\s*\d+", img_name)[0].replace("lt", ""),
    )

    img_handler.move_images(
        lambda img_name: img_name.find("LT") != -1,
        lambda img_name: re.search(r"lt\s*\d+", img_name.lower())[0].replace("lt", ""),
    )

    img_handler.move_images(
        lambda img_name: img_name.find("L.") != -1,
        lambda img_name: re.search(r"lt\s*\d+", img_name.lower().replace("l.", "lt"))[
            0
        ].replace("lt", ""),
    )

    img_handler.move_images(
        lambda img_name: re.search(r"L\d+", img_name),
        lambda img_name: re.search(r"lt\s*\d+", img_name.lower().replace("l", "lt"))[
            0
        ].replace("lt", ""),
    )

    logger.info("Separação das imagens finalizada")
except Exception as error:
    logger.error("{} ao tentar separar as imagens".format(error))

logger.info("Processo finalizado com sucesso.")
done = str(input("Pressione ENTER para encerrar..."))
