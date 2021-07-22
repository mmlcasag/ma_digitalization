import os
import csv
import zipfile
import tempfile
import shutil
import subprocess
import random
import sys
import pathlib

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
    # If errors are found, do this
    # clear contents of C:\Users\<username>\AppData\Local\Temp\gen_py
    # that should fix it

    if "~$" in file_name:
        logger.warning("O programa encontrou um arquivo temporário e irá ignorá-lo")
        return

    if os.name != "nt":
        logger.warning(
            "A extração de imagens de planilhas Excel não foi implementada em ambientes Linux"
        )
        return

    image_count = 0
    close_excel = True
    os_utils.create_folder(output_folder)

    try:
        logger.info("Verificando a instância do Excel")
        try:
            excel = win32.GetActiveObject("Excel.Application")
            close_excel = False
            logger.info(
                "Já havia uma instância do Excel aberta. A mesma foi utilizada."
            )
        except Exception:
            excel = win32.gencache.EnsureDispatch("Excel.Application")
            close_excel = True
            logger.info(
                "Não havia nenhuma instância do Excel aberta. Uma nova foi iniciada."
            )

        logger.info("Abrindo o arquivo Excel")
        workbook = excel.Workbooks.Open(file_name)

        logger.info("Procurando por imagens em todas as abas do arquivo")
        for sheet in workbook.Worksheets:
            for i, shape in enumerate(sheet.Shapes):
                if shape.Name.startswith("Picture") or shape.Name.startswith("Image"):
                    image_count = image_count + 1
                    image_name = os.path.join(
                        output_folder, "image_{}.png".format(image_count)
                    )

                    try:
                        logger.info('Extraindo a imagem "{}"'.format(image_name))
                        shape.Copy()
                        image = ImageGrab.grabclipboard()
                        image.save(image_name, "png")
                    except Exception as error:
                        logger.error(
                            "{} ao tentar extrair a imagem {}".format(error, image_name)
                        )

                    try:
                        logger.info("Convertendo imagem de PNG para JPG")
                        image_utils.convert_from_png_to_jpg(
                            image_name, output_folder, False
                        )
                    except Exception as error:
                        logger.error(
                            "{} ao tentar converter a imagem {}".format(
                                error, image_name
                            )
                        )

                    try:
                        logger.info("Redimensionando imagem")
                        image_utils.resize_image(image_name.replace("png", "jpg"))
                    except Exception as error:
                        logger.error(
                            "{} ao tentar redimensionar a imagem {}".format(
                                error, image_name
                            )
                        )
    except Exception as error:
        logger.error(
            "{} ao tentar extrair imagens de planilha Excel {}".format(error, file_name)
        )
    finally:

        try:
            logger.info("Fechando o arquivo Excel")
            workbook.Close()
        except Exception as error:
            logger.error("{} ao tentar fechar workbook".format(error))

        if close_excel:
            logger.info(
                "Fechando a instância do Excel pois ela foi aberta unicamente para esse processo"
            )
            try:
                excel.Application.Quit()
            except Exception as error:
                logger.error("{} ao tentar fechar excel".format(error))
        else:
            logger.info(
                "Não irá fechar a instância do Excel pois ela já estava aberta antes desse processo"
            )


def extract_images_from_xlsx(file, output_folder):
    shutil.rmtree(output_folder, ignore_errors=True)
    tempdir = tempfile.mkdtemp()
    file_name = f"{random.randint(1, 10000)}.ods"

    if os.name == "nt":
        drive = pathlib.Path.home().drive
        unoconv = os.path.join(drive, os.sep, "utils", "unoconv")

        subprocess.call(
            [
                "python",
                unoconv,
                "-f",
                "ods",
                "-o",
                os.path.join(tempdir, file_name),
                file,
            ]
        )
    else:
        subprocess.call(
            ["unoconv", "-f", "ods", "-o", os.path.join(tempdir, file_name), file]
        )

    with zipfile.ZipFile(os.path.join(tempdir, file_name), "r") as zip_ref:
        zip_ref.extractall(tempdir)
        origin_folder = os.path.join(tempdir, "Pictures")
        files_from_xlsx = os_utils.get_files_list(origin_folder)
        os_utils.create_folder(output_folder)
        for idx, file in enumerate(files_from_xlsx):
            origin_file = os.path.join(origin_folder, file)
            destination_file = os.path.join(output_folder, f"imagem_{idx+1}")
            if not origin_file.endswith("emf") and not origin_file.endswith("wmf"):
                shutil.copy(origin_file, f"{destination_file}.jpg")
                image_utils.resize_image(f"{destination_file}.jpg")

    shutil.rmtree(tempdir)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
