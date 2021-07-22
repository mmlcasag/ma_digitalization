import os
import utils.os as os_utils
import utils.excel as excel_utils
from services.base.logger import Logger

logger = Logger.__call__().get_logger()

absolute_path = os.getcwd()

input_folder = "input"
output_folder = "output"
images_folder = "images"

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(output_folder, images_folder)

allowed_extensions = ["xlsx", "xlsb", "xlsm", "xls"]

for file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        logger.info('PROCESSANDO O ARQUIVO "{}"'.format(file_name))

        input_path = os.path.join(absolute_path, input_folder, file_name)
        output_path = os.path.join(
            absolute_path,
            output_folder,
            images_folder,
            os_utils.get_file_name(file_name),
        )

        logger.info('Arquivo de entrada "{}"'.format(input_path))
        logger.info('Diretório de saída "{}"'.format(output_path))

        excel_utils.extract_images(input_path, output_path)

        logger.info("Arquivo {} processado com sucesso".format(file_name))
    except Exception as error:
        logger.error("{} ao tentar processar o arquivo {}".format(error, file_name))

logger.info("Processo finalizado com sucesso.")
done = str(input("Pressione ENTER para encerrar..."))
