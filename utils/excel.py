import os
import csv
import openpyxl
import win32com.client as win32
import utils.os as os_utils
import utils.csv as csv_utils
import utils.image as image_utils

from PIL import ImageGrab

def open_file(file_name):
    return openpyxl.load_workbook(file_name, data_only=True)

def get_sheets_list(workbook):
    return workbook.worksheets

def select_active_sheet(workbook):
    return workbook.active

def select_sheet_by_name(workbook, sheet_name):
    return workbook[sheet_name]

def get_cell_value(sheet, row_number, col_number):
    return sheet.cell(row_number, col_number).value

def get_first_cell(sheet):
    return get_cell_value(sheet, 1, 1)

def delete_rows(sheet, initial_row, how_many_rows):
    sheet.delete_rows(initial_row, how_many_rows)

def delete_until(sheet, target_value):
    while str(get_first_cell(sheet)) != str(target_value):
        delete_rows(sheet, 1, 1)

def export_to_csv(sheet, csv_file_name, delimiter=',', replacer='.'):
    csv_file = csv_utils.create_file(csv_file_name)
    writer = csv.writer(csv_file, delimiter=delimiter)
    for row in sheet.rows:
        writer.writerow([ str(cell.value).replace(delimiter,replacer).strip() for cell in row ])
    return csv_file

def close_file(workbook):
    workbook.close()

def extract_images(file_name, output_folder):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    workbook = excel.Workbooks.Open(file_name)
    os_utils.create_folder(output_folder)
    
    for sheet in workbook.Worksheets:
        for i, shape in enumerate(sheet.Shapes):
            image_name = os.path.join(output_folder, 'image_{}.png'.format(i + 1))

            if shape.Name.startswith('Picture'):
                shape.Copy()
                image = ImageGrab.grabclipboard()
                image.save(image_name, 'png')
                image_utils.from_png_to_jpg(image_name, output_folder)
            
            if shape.Name.startswith('Image'):
                shape.Copy()
                image = ImageGrab.grabclipboard()
                image.save(image_name, 'png')
                image_utils.from_png_to_jpg(image_name, output_folder)

    workbook.Close()
    excel.Quit()