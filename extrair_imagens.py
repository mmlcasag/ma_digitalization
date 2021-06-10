import os
import win32com.client as win32
from PIL import ImageGrab

excel = win32.gencache.EnsureDispatch('Excel.Application')
workbook = excel.Workbooks.Open(r'C:\ma_importer\input\CheckList_MRO.xlsx')

print('Procurando imagens na planilha "C:\ma_importer\input\CheckList_MRO.xlsx"')

for sheet in workbook.Worksheets:
    for i, shape in enumerate(sheet.Shapes):
        if shape.Name.startswith('Picture'):
            print('Encontrou objetos do tipo "Picture" dentro da planilha')
            shape.Copy()
            image = ImageGrab.grabclipboard()
            image.save('C:\ma_importer\output\Images\{}.png'.format(i+1), 'png')
            print('Gerou a imagem com o nome "C:\ma_importer\output\Images\{}.png"'.format(i+1))
        
        if shape.Name.startswith('Image'):
            print('Encontrou objetos do tipo "Image" dentro da planilha')
            shape.Copy()
            image = ImageGrab.grabclipboard()
            image.convert('RGB')
            image.save('C:\ma_importer\output\Images\{}.png'.format(i+1), 'png')
            print('Gerou a imagem com o nome "C:\ma_importer\output\Images\{}.png"'.format(i+1))

workbook.Close()
excel.Quit()