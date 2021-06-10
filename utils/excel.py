import os
import win32com.client as win32
import utils.os as os_utils

from PIL import ImageGrab

def extract_images(file_name, output_folder):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    workbook = excel.Workbooks.Open(file_name)
    os_utils.create_folder(output_folder)

    print('Searching for images in "{}"'.format(file_name))

    for sheet in workbook.Worksheets:
        for i, shape in enumerate(sheet.Shapes):
            image_name = os.path.join(output_folder, 'image_{}.png'.format(i + 1))

            if shape.Name.startswith('Picture'):
                print('Extracting image to "{}"'.format(image_name))
                shape.Copy()
                image = ImageGrab.grabclipboard()
                image.save(image_name, 'png')
            
            if shape.Name.startswith('Image'):
                print('Extracting image to "{}"'.format(image_name))
                shape.Copy()
                image = ImageGrab.grabclipboard()
                image.save(image_name, 'png')

    workbook.Close()
    excel.Quit()