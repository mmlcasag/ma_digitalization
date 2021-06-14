import os
import sys
import pandas

sys.path.append('..\..')

import utils.os as os_utils
import utils.csv as csv_utils
import utils.excel as excel_utils

absolute_path = os_utils.get_absolute_path()

input_folder = 'input'
output_folder = 'output'
csv_folder = 'csv'

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(os.path.join(output_folder, csv_folder))

allowed_extensions = ['xlsx','xlsb','xlsm']

for excel_file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    workbook = excel_utils.open_file(os.path.join(input_folder, excel_file_name))
    sheet = excel_utils.select_active_sheet(workbook)
    excel_utils.delete_until(sheet, 'NM')
    csv_file_name = os_utils.get_file_name(excel_file_name) + '.csv'
    csv_file = excel_utils.export_to_csv(sheet, os.path.join(output_folder, csv_folder, csv_file_name), ';', ',')
    csv_utils.close_file(csv_file)
    excel_utils.close_file(workbook)

    df = pandas.read_csv(os.path.join(output_folder, csv_folder, csv_file_name), sep=';')
    print(df.head())

print('Done')
