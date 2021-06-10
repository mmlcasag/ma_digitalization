import os
import utils.os as os_utils

from PIL import Image

def from_png_to_jpg(png_file_name, output_folder):
    if os_utils.get_file_extension(png_file_name) != '.png':
        raise ValueError('Only PNG images are supported by this function')
    
    jpg_file_name = png_file_name.replace('png','jpg')
    
    png_image = Image.open(png_file_name)
    jpg_image = png_image.convert('RGB')
    jpg_image.save(jpg_file_name)
