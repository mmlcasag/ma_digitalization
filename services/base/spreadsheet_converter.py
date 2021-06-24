import abc
import os
import utils.os as os_utils
from .logger import Logger

logger = Logger.__call__().get_logger()


class SpreadsheetConverter:
    _name_input_folders = []
    _name_output_folders = []
    _input_folders = []
    _output_folders = []
    _allowed_extensions = ["xlsx", "xlsb"]

    def __init__(self, base_folder, name_input_folders, name_output_folders):
        self._base_folder = os.path.join(os.getcwd(), base_folder)
        self._name_input_folders = name_input_folders
        self._name_output_folders = name_output_folders

    def execute(self):
        self.create_input_folder()
        self.create_output_folder()
        list_files = self.get_file_list()
        logger.info(f"Encontrados {len(list_files)} arquivo(s) na pasta de entrada")
        for file in list_files:
            try:
                self.process_file(file)
            except Exception as error:
                logger.error(f"Erro no processamento do arquivo {file}")
                logger.exception(error)

    def create_input_folder(self):
        for folder_name in self._name_input_folders:
            folder_directory = os.path.join(self._base_folder, folder_name)
            os_utils.create_folder(folder_directory)
            self._input_folders.append(folder_directory)

    def create_output_folder(self):
        for folder_name in self._name_output_folders:
            folder_directory = os.path.join(self._base_folder, folder_name)
            os_utils.create_folder(folder_directory)
            self._output_folders.append(folder_directory)

    def get_file_list(self):
        file_list = []
        for folder in self._input_folders:
            for file in os_utils.get_files_list(folder):
                file_list.append(f"{folder}/{file}")

        return file_list

    def remove_prefix(self, text, prefix):
        if text.startswith(prefix):
            return text[len(prefix) :]
        return text

    @abc.abstractmethod
    def process_file(self, file):
        """Create process to convert file"""
