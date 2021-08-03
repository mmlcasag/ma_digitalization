import os
import re
import utils.os as os_utils

from PIL import Image
from services.base.logger import Logger
from services.base.images_handler import ImageHandler

logger = Logger.__call__().get_logger()


def convert_to_jpg(image_name, image_extension, output_folder, keep_original=True):
    if os_utils.get_file_extension(image_name) == "jpg":
        logger.warning("A imagem já possui extensão JPG")
        return

    if os_utils.get_file_extension(image_name) == "wmf":
        logger.warning("O programa não consegue converter imagens com extensão WMF")
        return

    jpg_file_name = image_name.replace(image_extension, "jpg")

    image_file = Image.open(image_name)
    jpg_image = image_file.convert("RGB")
    jpg_image.save(jpg_file_name)

    if not keep_original:
        os.remove(image_name)


def resize_by_height(image, height):
    img_width = image.size[0]
    img_height = image.size[1]

    height_percent = height / float(img_height)
    width_size = int((float(img_width) * float(height_percent)))

    return image.resize((width_size, height), Image.NEAREST)


def resize_by_width(image, width):
    img_width = image.size[0]
    img_height = image.size[1]

    width_percent = width / float(img_width)
    height_size = int((float(img_height) * float(width_percent)))

    return image.resize((width, height_size), Image.NEAREST)


def resize_image(img_src):
    image = Image.open(img_src)
    base_width = 400
    base_height = 300
    max_long_side = 800

    logger.info('Verificando dimensões da imagem "{}"'.format(img_src))
    img_width = image.size[0]
    img_height = image.size[1]

    if img_width < base_width:
        image = resize_by_width(image, base_width)
        logger.info('Redimensionada largura da imagem "{}"'.format(img_src))
        img_width = image.size[0]
        img_height = image.size[1]

    if img_height < base_height:
        image = resize_by_height(image, base_height)
        logger.info('Redimensionada altura da imagem "{}"'.format(img_src))
        img_width = image.size[0]
        img_height = image.size[1]

    long_side = max(img_height, img_width)

    if long_side > max_long_side:
        logger.info("Maior lado da imagem supera o máximo permitido")

        if long_side == img_height:
            logger.info('Redimensionada altura da imagem "{}"'.format(img_src))
            image = resize_by_height(image, max_long_side)

        if long_side == img_width:
            logger.info('Redimensionada largura da imagem "{}"'.format(img_src))
            image = resize_by_width(image, max_long_side)

    image = image.convert("RGB")
    image.save(img_src)


def organize_images(input_folder, output_folder):
    img_handler = ImageHandler(input_folder, output_folder)

    # Pattern #1:
    # matches the following patterns:
    # 001a.jpg
    # 001b.jpg
    # 013f.jpg
    img_handler.move_images(
        lambda img_name: re.search(r"^(\d{3})(\w{1})\.", img_name),
        lambda img_name: re.search(r"^(\d{3})(\w{1})\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #2:
    # matches the following patterns:
    # LOTE 202279_f01_10174713.jpg
    # lote 202275_f01_10160074.jpg
    # Lote C200011_f01_11279515.jpg
    img_handler.move_images(
        lambda img_name: re.search(
            r"^[lL][oO][tT][eE]\s(\w+)_(f\d{2})_(\d+)\.", img_name
        ),
        lambda img_name: re.search(
            r"^[lL][oO][tT][eE]\s(\w+)_(f\d{2})_(\d+)\.", img_name
        )
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #3:
    # matches the following patterns:
    # Lote 23 - 01 (3).jpg
    # Lote 31 - 01 (1).jpg
    # Lote 2B - 01 (3).jpg
    img_handler.move_images(
        lambda img_name: re.search(
            r"^[lL][oO][tT][eE]\s(\w+)\s(-\s\d+\s)(\(\d*\))\.", img_name
        ),
        lambda img_name: re.search(
            r"^[lL][oO][tT][eE]\s(\w+)\s(-\s\d+\s)(\(\d*\))\.", img_name
        )
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #4:
    # matches the following patterns:
    # Lote 23 - 01.jpg
    # Lote 31 - 01.jpg
    # Lote 2B - 01.jpg
    img_handler.move_images(
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(-\s\d+)\.", img_name),
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(-\s\d+)\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #5:
    # matches the following patterns:
    # lote 28 - V.jpg
    # Lote 2B - XXIII.jpg
    # LOTE 32 - VIII.jpg
    img_handler.move_images(
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(-\s\D+)\.", img_name),
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(-\s\D+)\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #6:
    # matches the following patterns:
    # Lote 27 (1).jpg
    # LOTE 2A (2).jpg
    # lote B4 (1).jpg
    img_handler.move_images(
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(\(\d+\))\.", img_name),
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(\(\d+\))\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #7:
    # matches the following patterns:
    # Lote 27 (XII).jpg
    # LOTE 7G (DE).jpg
    # lote G1 (CA).jpg
    img_handler.move_images(
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(\(\D+\))\.", img_name),
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s(\(\D+\))\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #8:
    # matches the following patterns:
    # LOTE 31- XIII.jpg
    # LOTE 36- IV.jpg
    # Lote 8F- VII.jpg
    img_handler.move_images(
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)(-\s\D+)\.", img_name),
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)(-\s\D+)\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #9:
    # matches the following patterns:
    # Lote 28 X.jpg
    # LOTE 40 IV.jpg
    # loTe H0 III.jpg
    img_handler.move_images(
        lambda img_name: re.search(
            r"^[lL][oO][tT][eE]\s(\w+)\s[^-\(](\D*)\.", img_name
        ),
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s(\w+)\s[^-\(](\D*)\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #10:
    # matches the following patterns:
    # LOTE 35.jpg
    # Lote a5.jpg
    # LOTE XI.jpg
    img_handler.move_images(
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s([^\W_]+)\.", img_name),
        lambda img_name: re.search(r"^[lL][oO][tT][eE]\s([^\W_]+)\.", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )

    # Pattern #11:
    # matches the following patterns:
    # 10175654 lt34.jpg
    # 10407921 lt36 ii.jpg
    # 10407921 lt36.jpg
    img_handler.move_images(
        lambda img_name: re.search(r"[lL][tT](\d+)(\s)?(\w*)?", img_name),
        lambda img_name: re.search(r"[lL][tT](\d+)(\s)?(\w*)?", img_name)
        .group(1)
        .lstrip("0")
        .strip(),
    )
