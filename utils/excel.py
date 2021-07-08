import os
import csv
import zipfile
import tempfile
import shutil
from PIL import Image

if os.name == "nt":
    import win32com.client as win32

import utils.os as os_utils
import utils.image as image_utils

from PIL import ImageGrab
from services.base.logger import Logger


logger = Logger.__call__().get_logger()


def delete_until(sheet, target_value, column_index=1, row_index=1):
    while not str(sheet.cell(row_index, column_index).value) in target_value:
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
        logger.warning("Importação de imagem não implementada para ambientes linux")
        return

    image_count = 0
    os_utils.create_folder(output_folder)

    try:
        excel = win32.gencache.EnsureDispatch("Excel.Application")
        workbook = excel.Workbooks.Open(file_name)

        for sheet in workbook.Worksheets:
            for i, shape in enumerate(sheet.Shapes):
                if shape.Name.startswith("Picture") or shape.Name.startswith("Image"):
                    try:
                        image_count = image_count + 1
                        image_name = os.path.join(
                            output_folder, "image_{}.png".format(image_count)
                        )

                        logger.info('Extraindo a imagem "{}"'.format(image_name))
                        shape.Copy()
                        image = ImageGrab.grabclipboard()
                        image.save(image_name, "png")

                        logger.info("Convertendo de PNG para JPG")
                        image_utils.convert_from_png_to_jpg(
                            image_name, output_folder, False
                        )
                    except Exception as error:
                        logger.error(
                            "{} ao tentar extrair a imagem {}".format(error, image_name)
                        )
    except Exception as error:
        logger.error("{} ao tentar abrir o Excel {}".format(error, file_name))
    finally:
        workbook.Close()
        excel.Quit()


def resize_image(img_src):
    image = Image.open(img_src)
    base_width = 400
    base_height = 300

    if image.size[0] < base_width:
        wpercent = base_width / float(image.size[0])
        hsize = int((float(image.size[1]) * float(wpercent)))
        image = image.resize((base_width, hsize), Image.NEAREST)

    if image.size[1] < base_height:
        height_percent = base_height / float(image.size[1])
        width_size = int((float(image.size[0]) * float(height_percent)))
        image = image.resize((width_size, base_height), Image.NEAREST)

    image = image.convert("RGB")
    image.save(img_src)


def extract_images_from_xlsx(file, output_folder):
    with zipfile.ZipFile(file, "r") as zip_ref:
        shutil.rmtree(output_folder, ignore_errors=True)
        tempdir = tempfile.mkdtemp()
        zip_ref.extractall(tempdir)
        origin_folder = os.path.join(tempdir, "xl", "media")
        files_from_xlsx = os_utils.get_files_list(origin_folder)
        os_utils.create_folder(output_folder)
        for idx, file in enumerate(files_from_xlsx):
            origin_file = os.path.join(origin_folder, file)
            destination_file = os.path.join(output_folder, f"imagem_{idx+1}")

            if os.name == "nt":
                Image.open(origin_file).save(f"{destination_file}.jpg")
            else:
                ext = 'jpg'
                if os_utils.get_file_extension(origin_file) == 'emf':
                    ext = 'emf'
                shutil.copy(origin_file, f"{destination_file}.{ext}")

        shutil.rmtree(tempdir)
