import os
import utils.os as os_utils
import utils.image as image_utils
import win32com.client as win32

from PIL import ImageGrab

def extract_images(file_name, output_folder):
    print('Searching for images in "{}"'.format(file_name))
    
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    workbook = excel.Workbooks.Open(file_name)
    os_utils.create_folder(output_folder)
    
    for sheet in workbook.Worksheets:
        for i, shape in enumerate(sheet.Shapes):
            image_name = os.path.join(output_folder, 'image_{}.png'.format(i + 1))

            if shape.Name.startswith('Picture'):
                shape.Copy()
                
                print('Extracting image to "{}"'.format(image_name))
                image = ImageGrab.grabclipboard()
                image.save(image_name, 'png')

                print('Converting from PNG to JPG')
                image_utils.from_png_to_jpg(image_name, output_folder)
            
            if shape.Name.startswith('Image'):
                shape.Copy()
                
                print('Extracting image to "{}"'.format(image_name))
                image = ImageGrab.grabclipboard()
                image.save(image_name, 'png')

                print('Converting from PNG to JPG')
                image_utils.from_png_to_jpg(image_name, output_folder)

    workbook.Close()
    excel.Quit()