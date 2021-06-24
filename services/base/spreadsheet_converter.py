import abc
import os
import utils.os as os_utils


class SpreadsheetConverter:
    _name_input_folders = []
    _name_output_folders = []
    _input_folders = []
    _output_folders = []
    _allowed_extensions = ["xlsx", "xlsb"]

    def __init__(self, base_folder, name_input_folders, name_output_folders):
        self._base_folder = f"{os.getcwd()}/{base_folder}"
        self._name_input_folders = name_input_folders
        self._name_output_folders = name_output_folders

    def execute(self):
        self.createInputFolders()
        self.createOutputFolders()
        list_files = self.getFileList()
        for file in list_files:
            self.processFile(file)

    def createInputFolders(self):
        for folder_name in self._name_input_folders:
            folder_directory = f"{self._base_folder}/{folder_name}"
            os_utils.create_folder(folder_directory)
            self._input_folders.append(folder_directory)

    def createOutputFolders(self):
        for folder_name in self._name_output_folders:
            folder_directory = f"{self._base_folder}/{folder_name}"
            os_utils.create_folder(folder_directory)
            self._output_folders.append(folder_directory)

    def getFileList(self):
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
    def processFile(self, file):
        """Create process to convert file"""
