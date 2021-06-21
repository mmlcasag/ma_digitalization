import os
import csv

if os.name == "nt":
    import win32com.client as win32

import utils.os as os_utils
import utils.image as image_utils

from PIL import ImageGrab


def delete_until(sheet, target_value, column_index=1, row_index=1):
    while str(sheet.cell(row_index, column_index).value) != str(target_value):
        sheet.delete_rows(1, 1)


def export_to_csv(sheet, csv_file_name, delimiter=",", replacement="."):
    csv_file = open(csv_file_name, "w", newline="", encoding="utf-8")
    writer = csv.writer(csv_file, delimiter=delimiter)
    for row in sheet.rows:
        writer.writerow(
            [str(cell.value).replace(delimiter, replacement).strip() for cell in row]
        )
    csv_file.close()


def extract_images(file_name, output_folder):
    if os.name != "nt":
        print("INFO: Importação de imagem não implementada para ambientes linux")
        return

    excel = win32.gencache.EnsureDispatch("Excel.Application")
    workbook = excel.Workbooks.Open(file_name)
    os_utils.create_folder(output_folder)

    image_count = 0

    for sheet in workbook.Worksheets:
        for i, shape in enumerate(sheet.Shapes):
            if shape.Name.startswith("Picture") or shape.Name.startswith("Image"):
                image_count = image_count + 1
                image_name = os.path.join(
                    output_folder, "image_{}.png".format(image_count)
                )

                print('DEBUG: Extraindo a imagem "{}"'.format(image_name))
                shape.Copy()
                image = ImageGrab.grabclipboard()
                image.save(image_name, "png")

                print("DEBUG: Convertendo de PNG para JPG")
                image_utils.convert_from_png_to_jpg(image_name, output_folder, False)

    workbook.Close()
    excel.Quit()
