import os
import utils.os as os_utils

from PIL import Image
from services.base.logger import Logger

logger = Logger.__call__().get_logger()


def convert_from_png_to_jpg(png_file_name, output_folder, keep_original=True):
    if os_utils.get_file_extension(png_file_name) != "png":
        raise ValueError("Only PNG images are supported by this function")

    jpg_file_name = png_file_name.replace("png", "jpg")

    png_image = Image.open(png_file_name)
    jpg_image = png_image.convert("RGB")
    jpg_image.save(jpg_file_name)

    if not keep_original:
        os.remove(png_file_name)


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
