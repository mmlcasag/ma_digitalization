import os
import utils.os as os_utils
import shutil
from .logger import Logger

logger = Logger.__call__().get_logger()


class ImageHandler:
    _input_folder = ""
    _output_folder = ""

    def __init__(self, input_folder, output_folder):
        self._input_folder = input_folder
        self._output_folder = output_folder

    # should_move is a function to evaluate if image needs be moved
    # create_folder_name is a function to create name of destination image file
    def move_images(self, should_move, create_folder_name):
        file_list = os_utils.get_files_list(self._input_folder)

        if len(file_list) > 0:
            os_utils.create_folder(self._output_folder)

        file_list.sort()
        for img_name in file_list:
            if should_move(img_name):
                try:
                    destination_folder_name = create_folder_name(img_name).strip()
                    destination_folder = os.path.join(
                        self._output_folder, destination_folder_name
                    )
                    os_utils.create_folder(destination_folder)
                    origin_file_src = os.path.join(self._input_folder, img_name)
                    shutil.copy(origin_file_src, destination_folder)
                except Exception as error:
                    logger.error(
                        f'Erro "{error}" no processamento da imagem "{img_name}"'
                    )
