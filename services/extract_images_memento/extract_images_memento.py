import os
import re
import pandas
import utils.os as os_utils
import utils.image as image_utils


from services.base.logger import Logger
logger = Logger.__call__().get_logger()


input_folder = 'input'
output_folder = 'output'
images_folder = 'images'


def delete_output_folder():
    logger.info('Removendo diretório de saída')
    
    os_utils.delete_folder(output_folder)

    logger.info('Diretório de saída removido com sucesso')


def create_output_folder():
    logger.info('Criando diretório de saída')

    os_utils.create_folder(output_folder)
    os_utils.create_folder(os.path.join(output_folder, images_folder))
    
    logger.info('Diretório de saída criado com sucesso')


def create_input_folder():
    logger.info('Criando diretório de entrada')

    os_utils.create_folder(input_folder)
    os_utils.create_folder(os.path.join(input_folder, images_folder))
    
    logger.info('Diretório de entrada criado com sucesso')


def get_input_files():
    logger.info('Buscando arquivos no diretório de entrada')

    allowed_extensions = ['xlsx', 'xlsb', 'xlsm', 'xls']
    input_files = os_utils.get_files_list(input_folder, allowed_extensions)

    logger.info('Retornados arquivos no diretório de entrada com sucesso')
    logger.debug(input_files)

    return input_files


def get_full_file_path(file_name):
    logger.info('Montando o endereço completo do arquivo')

    full_file_path = os.path.join(os_utils.get_absolute_path(), input_folder, input_file)
    
    logger.info('Endereço completo do arquivo montado com sucesso')
    logger.debug(full_file_path)
    
    return full_file_path


def create_folder_for_file(file_name):
    logger.info('Criando pasta para o arquivo no diretório de saída')

    file_folder = os_utils.get_file_name(file_name)
    os_utils.create_folder(os.path.join(output_folder, images_folder, file_folder))
    
    logger.info('Pasta para o arquivo criada com sucesso')


def read_file(full_file_path):
    logger.info('Abrindo o arquivo para processá-lo')
    
    dataframe = pandas.read_excel(full_file_path)

    logger.info('Arquivo aberto com sucesso')
    
    return dataframe


def get_column_names(dataframe):
    logger.info('Obtendo colunas do arquivo')

    columns = dataframe.columns
    
    logger.info('Colunas do arquivo obtidas com sucesso')
    logger.debug(columns)

    return columns


def get_column_count(columns):
    logger.info('Contando colunas do arquivo')

    qty_columns = len(columns)
    
    logger.info('Colunas do arquivo contadas com sucesso')
    logger.debug(qty_columns)

    return qty_columns
    

def get_key_columns_names(columns):
    logger.info('Obtendo nomes das colunas-chave do arquivo')
    
    key_columns_names = []
    if 'Lote Ref. / Ativo-Frota' in columns:
        key_columns_names.append('Lote Ref. / Ativo-Frota')
    if 'Etiqueta (Lote Ref.)' in columns:
        key_columns_names.append('Etiqueta (Lote Ref.)')
    if 'Etiqueta (Lote Ref.) - Inicio' in columns:
        key_columns_names.append('Etiqueta (Lote Ref.) - Inicio')
    if 'Etiqueta (Lote Ref.) - Fim' in columns:
        key_columns_names.append('Etiqueta (Lote Ref.) - Fim')
    
    logger.info('Nomes das colunas-chave do arquivo obtidas com sucesso')
    logger.debug(key_columns_names)

    return key_columns_names


def get_key_columns_indexes(columns):
    logger.info('Obtendo índices das colunas-chave do arquivo')
    
    key_columns_indexes = []
    if 'Lote Ref. / Ativo-Frota' in columns:
        key_columns_indexes.append(columns.get_loc('Lote Ref. / Ativo-Frota'))
    if 'Etiqueta (Lote Ref.)' in columns:
        key_columns_indexes.append(columns.get_loc('Etiqueta (Lote Ref.)'))
    if 'Etiqueta (Lote Ref.) - Inicio' in columns:
        key_columns_indexes.append(columns.get_loc('Etiqueta (Lote Ref.) - Inicio'))
    if 'Etiqueta (Lote Ref.) - Fim' in columns:
        key_columns_indexes.append(columns.get_loc('Etiqueta (Lote Ref.) - Fim'))
    
    logger.info('Índices das colunas-chave do arquivo obtidas com sucesso')
    logger.debug(key_columns_indexes)

    return key_columns_indexes


def replace_nan_values(dataframe, key_columns_names):
    logger.info('Substituindo valores NaN por zero')

    for column in key_columns_names:
        dataframe[column] = dataframe[column].fillna(0)
        
    logger.info('Valores NaN substituídos por zero com sucesso')


def get_lot_references(row, key_columns):
    logger.info('Buscando os lotes de referência do registro')

    lot_references = []
    
    for key in key_columns:
        value = row[key + 1]
        
        if isinstance(value, int):
            if value > 0:
                lot_references.append(str(value))
        elif isinstance(value, float):
            if value > 0:
                lot_references.append(str(int(value)))
        else:
            if len(value) > 0:
                lot_references.append(value)

    logger.info('Lotes de referência do registro encontrados com sucesso')
    logger.debug(lot_references)

    """
    Um pouco de regra de negócio:
    =========================================================
    
    Cenário #1:
    Planilhas que possuem apenas um campo de lote de referência
    Nesse caso simplesmente retornamos o valor do campo
    Nunca o campo poderá estar vazio. Se isso ocorrer, a aplicação irá retornar erro

    Exemplo:
    Etiqueta (Lote Ref.)    |
    ------------------------|
    "PFK"                   |

    ou

    Lote Ref. / Ativo-Frota |
    ------------------------|
    "CBA"                   |
    
    Cenário #2:
    Planilhas que possuem três campos de lote de referência
    - Um campo para valor individual
    - Dois campos para intervalo de valores (valor inicial e valor final)

    Nesse caso, ou o campo individual deve ser preenchido, ou os dois campos do intervalo de valores
    Nunca os três campos deverão estar preenchidos. Se isso ocorrer, a aplicação irá retornar erro
    Nunca os três campos poderão estar vazios. Se isso ocorrer, a aplicação irá retornar erro
    
    Exemplo:
    Etiqueta (Lote Ref.) | Etiqueta (Lote Ref.) - Inicio | Etiqueta (Lote Ref.) - Fim
    ---------------------|-------------------------------|----------------------------------
    14314                |                               |
                         | 14317                         | 14323
    """

    if len(lot_references) > 2:
        logger.error('Formato inválido: Lotes de referência devem ser informados ou individual ou em intervalo')
        raise Exception('Formato Inválido', 'Lotes de referência devem ser informados ou individual ou em intervalo')
    elif len(lot_references) == 2:
        logger.info('Gerando o intervalo dos lotes de referência')
        
        int_lot_references = [ int(lot) for lot in lot_references ]
        interval_lot_references = list(range(min(int_lot_references), max(int_lot_references) + 1, 1))
        
        logger.info('Intervalo dos lotes de referência gerado com sucesso')
        logger.debug(interval_lot_references)

        return interval_lot_references
    elif len(lot_references) == 1:
        return lot_references
    else:
        logger.error('Formato inválido: Ao menos um lote de referência deve ser informados')
        raise Exception('Formato Inválido', 'Ao menos um lote de referência deve ser informados')


def get_image_name(file_name):
    pattern = r'\d{4}-\d{2}-\d{2}\s\d{2}\.\d{2}\.\d{2}\.jpg|jpeg|png|gif'
    return re.findall(pattern, file_name)[0]


def get_image_names(qty_columns, row):
    logger.info('Buscando as nomes das fotos do lote')

    image_names = []
    
    for column in range(qty_columns):
        cell_value = str(row[column])
        
        if cell_value.startswith('file:///'):
            image_name = get_image_name(cell_value)
            image_names.append(image_name)
    
    logger.info('Nomes das fotos do lote encontradas com sucesso')
    logger.debug(image_names)

    return image_names


def create_folder_for_lot(file_name, lot_reference):
    logger.info('Criando pasta para o lote de referência no diretório de saída')

    file_folder = os_utils.get_file_name(file_name)
    lot_folder = str(lot_reference)
    os_utils.create_folder(os.path.join(output_folder, images_folder, file_folder, lot_folder))
    
    logger.info('Pasta para o lote de referência criada com sucesso')


def copy_image_to_output_folder(file_name, lot_reference, image_names):
    logger.info('Copiando imagens do lote para a pasta do diretório de saída')

    file_folder = os_utils.get_file_name(file_name)
    lot_folder = str(lot_reference)

    for image_name in image_names:
        full_source_path = os.path.join(os_utils.get_absolute_path(), input_folder, images_folder, image_name)
        full_destination_path = os.path.join(os_utils.get_absolute_path(), output_folder, images_folder, file_folder, lot_folder, image_name)

        try:
            os_utils.copy_file(full_source_path, full_destination_path)
        except:
            logger.error('Não foi encontrada a foto "{}"'.format(image_name))
    
    logger.info('Imagens do lote copiadas com sucesso para a pasta do diretório de saída')


def resize_and_compress_images(file_name, lot_reference, image_names):
    logger.info('Redimensionando e compactando imagens do lote')

    file_folder = os_utils.get_file_name(file_name)
    lot_folder = str(lot_reference)

    for image_name in image_names:
        full_destination_path = os.path.join(os_utils.get_absolute_path(), output_folder, images_folder, file_folder, lot_folder, image_name)

        try:
            image_utils.resize_image(full_destination_path)
        except:
            logger.error('Não foi possível redimensionar e compactar a foto "{}"'.format(image_name))
    
    logger.info('Imagens do lote redimensionadas e compactadas com sucesso')


def process_row(input_file, qty_columns, key_columns, index, row):
    logger.info('Processando linha: {}'.format(index + 1))

    lot_references = get_lot_references(row, key_columns)
    image_names = get_image_names(qty_columns, row)

    for lot_reference in lot_references:
        create_folder_for_lot(input_file, lot_reference)
        copy_image_to_output_folder(input_file, lot_reference, image_names)
        resize_and_compress_images(input_file, lot_reference, image_names)

    logger.info('Linha processada com sucesso')


def process_file(input_file):
    logger.info('Processando arquivo: {}'.format(input_file))

    create_folder_for_file(input_file)
    full_file_path = get_full_file_path(input_file)
    dataframe = read_file(full_file_path)
    columns = get_column_names(dataframe)
    qty_columns = get_column_count(columns)
    key_column_names = get_key_columns_names(columns)
    key_columns_indexes = get_key_columns_indexes(columns)
    replace_nan_values(dataframe, key_column_names)
    for index, row in enumerate(dataframe.itertuples()):
        process_row(input_file, qty_columns, key_columns_indexes, index, row)

    logger.info('Arquivo processado com sucesso')


def show_success_message():
    logger.info("Processo finalizado com sucesso")
    done = str(input("Pressione ENTER para encerrar..."))


if __name__ == "__main__":
    create_input_folder()
    create_output_folder()

    input_files = get_input_files()
    for input_file in input_files:
        process_file(input_file)
    
    show_success_message()
