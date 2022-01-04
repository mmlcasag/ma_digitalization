import os
import re
import pandas
import shutil
import utils.os as os_utils
import utils.image as image_utils
from services.base.logger import Logger
logger = Logger.__call__().get_logger()


absolute_path = os.getcwd()
input_folder = 'input'
output_folder = 'output'
images_folder = 'images'

os_utils.create_folder(input_folder)
os_utils.create_folder(input_folder, images_folder)
os_utils.create_folder(output_folder)

allowed_extensions = ['xlsx', 'xlsb', 'xlsm', 'xls']

logger.info('PROCESSO DE EXTRAÇÃO DE IMAGENS DAS PLANILHAS EXCEL DO MEMENTO')
logger.info('Procurando por planilhas excel no diretório de entrada')


def get_image_name(image_path):
    pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}\.\d{2}\.\d{2}\.jpg|jpeg|png|gif'
    return re.findall(pattern, image_path)[0]


def extract_image(lot_reference, lot_reference_range_min, lot_reference_range_max, output_path, image_name):
    # Existem duas formas de tratar os lotes de referência
    # Forma 1) Individual: o lot_referente vem preenchido e lot_reference_range_min e lot_reference_range_max vem zerados
    # Forma 2) Range: o lot_referente vem zerado e lot_reference_range_min e lot_reference_range_max vem preenchidos
    if lot_reference > 0:
        fetch_image(output_path, image_name, lot_reference)
    
    if lot_reference == 0:
        for lot_reference in range(lot_reference_range_min, lot_reference_range_max + 1):
            fetch_image(output_path, image_name, lot_reference)


def fetch_image(output_path, image_name, lot_reference):
    image_path = os.path.join(output_path, str(lot_reference))
    os_utils.create_folder(image_path)
    
    path_original_file = os.path.join(absolute_path, input_folder, images_folder, image_name)
    path_destination_file = os.path.join(image_path, image_name)
    
    shutil.copyfile(path_original_file, path_destination_file)
    image_utils.resize_image(path_destination_file)


for file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        input_file = os.path.join(absolute_path, input_folder, file_name)
        logger.info('Encontrada a planilha "{}"'.format(input_file))

        output_path = os.path.join(absolute_path, output_folder, os_utils.get_file_name(file_name))
        logger.info('Criando o diretório de saída "{}"'.format(output_path))
        os_utils.create_folder(output_path)
        
        logger.info('Abrindo a planilha "{}"'.format(file_name))
        df = pandas.read_excel(input_file)

        logger.info("Convertendo colunas para texto")
        df = df.astype(str)

        logger.info('Obtendo nomes das colunas')
        df_columns = df.columns
        
        logger.info('Filtrando colunas de referência de lote')
        key_columns = ['Etiqueta (Lote Ref.)', 'Etiqueta (Lote Ref.) - Inicio', 'Etiqueta (Lote Ref.) - Fim']
        logger.debug(key_columns)

        logger.info("Convertendo colunas de referência de lote para numérico")
        df[key_columns] = df[key_columns].mask(df.eq('nan')).fillna(0).apply(pandas.to_numeric)
        
        logger.info('Filtrando colunas contendo referência para as fotos dos lotes')
        url_columns = ['Foto Etiqueta (Lote Ref.)', 'Foto Principal', 'Foto Adicional 1', 'Foto Adicional 2', 'Foto Adicional 3']
        logger.debug(url_columns)

        logger.info('Verificando linha a linha')
        row_number = 1
        for row in df.iterrows():
            row_number = row_number + 1
            
            logger.info('Linha "{}"'.format(row_number))

            lot_reference           = int(df.loc[row_number-2, 'Etiqueta (Lote Ref.)'])
            lot_reference_range_min = int(df.loc[row_number-2, 'Etiqueta (Lote Ref.) - Inicio'])
            lot_reference_range_max = int(df.loc[row_number-2, 'Etiqueta (Lote Ref.) - Fim'])
            
            if lot_reference > 0:
                logger.info('Referência "{}"'.format(lot_reference))
            else:
                logger.info('Referência "[{}-{}]"'.format(lot_reference_range_min, lot_reference_range_max))

            logger.info('Verificando coluna a coluna')
            for column in url_columns:
                cell = df.loc[row_number-2, column]
                
                if cell != 'nan':
                    image_name = get_image_name(cell)
                    
                    logger.info('Verificando a coluna "{}"'.format(column))
                    logger.info('Extraindo a foto "{}"'.format(image_name))
                    
                    try:
                        extract_image(lot_reference, lot_reference_range_min, lot_reference_range_max, output_path, image_name)
                    except:
                        logger.error('Não foi possível extrair a foto "{}"'.format(image_name))

    except Exception as error:
        logger.error("{} ao tentar processar o arquivo {}".format(error, file_name))
