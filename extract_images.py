import os
import utils.os as os_utils
import utils.excel as excel_utils

absolute_path = os_utils.get_absolute_path()
input_folder = 'input'
output_folder = 'output'
allowed_extensions = ['xlsx','xlsb']

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(output_folder, 'images')

for file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    excel_utils.extract_images(os.path.join(absolute_path, input_folder, file_name), os.path.join(absolute_path, output_folder, 'images', os_utils.get_file_name(file_name)))

print('Done')