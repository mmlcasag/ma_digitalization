import os
import pandas
import openpyxl
import warnings

import utils.os as os_utils
import utils.ma as ma_utils
import utils.html as html_utils
import utils.excel as excel_utils

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

absolute_path = os.getcwd()

base_folder = "."
input_folder = os.path.join(base_folder, "input")
output_folder = os.path.join(base_folder, "output")
csv_folder = os.path.join(output_folder, "csv")
html_folder = os.path.join(output_folder, "html")
excel_folder = os.path.join(output_folder, "xlsx")
images_folder = os.path.join(output_folder, "images")

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(output_folder, csv_folder)
os_utils.create_folder(output_folder, html_folder)
os_utils.create_folder(output_folder, excel_folder)
os_utils.create_folder(output_folder, images_folder)

dataset_sheet_1 = pandas.DataFrame(columns=ma_utils.get_spreadsheet_columns())
dataset_sheet_2 = pandas.DataFrame()

allowed_extensions = ["xlsx", "xlsb"]

for excel_file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        print('INFO: PROCESSANDO O ARQUIVO "{}"'.format(excel_file_name))

        file_name = os_utils.get_file_name(excel_file_name)

        print('DEBUG: Nome do arquivo sem extensão "{}"'.format(file_name))

        print("INFO: Extraindo imagens do arquivo Excel")
        input_path = os.path.join(absolute_path, input_folder, excel_file_name)
        output_path = os.path.join(
            absolute_path,
            output_folder,
            images_folder,
            file_name,
        )
        excel_utils.extract_images(input_path, output_path)

        print("INFO: Abrindo o arquivo Excel")
        workbook = openpyxl.load_workbook(
            os.path.join(input_folder, excel_file_name), data_only=True
        )

        print("INFO: Selecionando a aba ativa da planilha")
        sheet = workbook.active

        print(
            'DEBUG: Deletando linhas até que quarta coluna, primeira linha seja "Descrição"'
        )
        excel_utils.delete_until(sheet, "Descrição", 4, 1)

        print("INFO: Exportando o resultado para um arquivo CSV")
        excel_utils.export_to_csv(
            sheet,
            os.path.join(output_folder, csv_folder, file_name + ".csv"),
            ";",
            ",",
        )

        print("DEBUG: Fechando o arquivo Excel")
        workbook.close()

        print("INFO: Carregando um dataset com os dados do arquivo CSV")
        df = pandas.read_csv(
            os.path.join(output_folder, csv_folder, file_name + ".csv"),
            delimiter=";",
        )

        print(
            "DEBUG: Convertendo todas as colunas do dataset da primeira aba para texto"
        )
        df = df.astype(str)

        print(
            "DEBUG: Desconsiderando as linhas cujos valores de todas as colunas estão vazios ou inválidos"
        )
        df = df.mask(df.eq("None")).dropna(how="all")

        print("DEBUG: Ajustando os nomes das colunas")
        df = df.rename(
            columns={
                "Cód.": "Código do Produto",
                "Material": "Código do Produto",
                "Descrição": "Descrição do Produto",
                "PN": "Referência do Produto",
                "Centro": "Centro",
                "Depósito": "Depósito",
                "Código Grupo de mercadorias": "Código do Grupo",
                "Código Grupo de Mercadorias": "Código do Grupo",
                "Descrição do grupo de mercadorias": "Descrição do Grupo",
                "Descrição do Grupo de Mercadorias": "Descrição do Grupo",
                "Fabricante": "Nome do Fabricante",
                "Qte": "Quantidade",
                "UM": "Unidade",
                "PMM": "Valor Unitário",
                "Valor": "Valor Total",
                "Responsável CMD": "Responsável",
                "CMD / Mina\n(selecionar a opção da lista)": "Empresa",
                "Cidade / Estado\n(onde se encontra o lote fisicamente)": "Localização",
                "Nº lote": "Lote de Referência",
            }
        )

        print(
            "DEBUG: Desconsiderando colunas desnecessárias para o processamento do arquivo"
        )
        df = df.reindex(
            columns=[
                "Código do Produto",
                "Descrição do Produto",
                "Referência do Produto",
                "Centro",
                "Depósito",
                "Código do Grupo",
                "Descrição do Grupo",
                "Nome do Fabricante",
                "Quantidade",
                "Unidade",
                "Valor Unitário",
                "Valor Total",
                "Responsável",
                "Empresa",
                "Localização",
                "Lote de Referência",
            ]
        )

        print("INFO: Exportando os produtos do lote para um arquivo HTML")

        print(
            "DEBUG: Carregando um dataset baseado no dataset principal, para ser utilizado na geração do HTML"
        )
        df_html = df.reindex(
            columns=[
                "Código do Produto",
                "Descrição do Produto",
                "Referência do Produto",
                "Centro",
                "Depósito",
                "Nome do Fabricante",
                "Quantidade",
                "Unidade",
                "Lote de Referência",
            ]
        )

        print("DEBUG: Gerando código HTML a partir dos dados do dataset")
        html_content = df_html.to_html(index=False, na_rep="")

        print("DEBUG: Concatenando o cabeçalho e o rodapé do arquivo HTML")
        html_content = html_utils.get_header() + html_content + html_utils.get_footer()

        print("DEBUG: Criando o arquivo HTML")
        html_file = open(
            os.path.join(
                output_folder,
                html_folder,
                file_name + ".html",
            ),
            "w",
            newline="",
            encoding="utf-8",
        )

        print("DEBUG: Escrevendo no arquivo HTML")
        html_file.write(html_content)

        print("DEBUG: Fechando o arquivo HTML")
        html_file.close()

        print("INFO: Exportação do arquivo HTML finalizada com sucesso")

        print("INFO: Montando a linha da planilha colunada")

        print("DEBUG: Buscando o nome do responsável do lote")
        try:
            asset_manager_name = df["Responsável"][0]
        except Exception as error:
            print(
                "ERROR: {} ao tentar buscar o nome do responsável do lote".format(error)
            )
            asset_manager_name = ""

        print("DEBUG: Buscando o nome da empresa do lote")
        try:
            asset_owner_name = df["Empresa"][0]
        except Exception as error:
            print("ERROR: {} ao tentar buscar o nome da empresa do lote".format(error))
            asset_owner_name = "Vale"

        print("DEBUG: Buscando o município e o estado do lote")
        try:
            asset_location = ma_utils.split_city_and_state(df["Localização"][0])
            asset_location_city = asset_location[0]
            asset_location_state = asset_location[1]
        except Exception as error:
            print(
                "ERROR: {} ao tentar buscar o município e o estado do lote".format(
                    error
                )
            )
            asset_location_city = ""
            asset_location_state = ""

        print("DEBUG: Buscando o número do lote de referência")
        try:
            asset_reference_number = df["Lote de Referência"][0]
        except Exception as error:
            print(
                "ERROR: {} ao tentar buscar o número do lote de referência".format(
                    error
                )
            )
            asset_reference_number = ""

        print("DEBUG: Definindo a descrição resumida do lote")
        try:
            asset_description = ma_utils.get_asset_description(
                df, "Descrição do Produto", "Valor Total", 5
            )
        except Exception as error:
            print(
                "ERROR: {} ao tentar definir a descrição resumida do lote".format(error)
            )
            asset_description = ""

        print("DEBUG: Buscando o valor de referência do lote")
        try:
            asset_reference_value = round(df["Valor Total"].astype(float).sum(), 2)
        except Exception as error:
            print(
                "ERROR: {} ao tentar buscar o valor de referência do lote".format(error)
            )
            asset_reference_value = 0

        print("DEBUG: Buscando o valor inicial do lote")
        try:
            asset_initial_value = round(float(asset_reference_value / 100), 2)
        except Exception as error:
            print("ERROR: {} ao tentar buscar o valor inicial do lote".format(error))
            asset_initial_value = 0

        print("DEBUG: Buscando o valor de incremento do lote")
        try:
            asset_increment_value = int(
                ma_utils.get_closest_value(
                    ma_utils.get_available_increments(), asset_initial_value / 10
                )
            )
        except Exception as error:
            print(
                "ERROR: {} ao tentar buscar o valor de incremento do lote".format(error)
            )
            asset_increment_value = 0

        print("DEBUG: Gerando a linha colunada do lote")
        dataset_sheet_1 = dataset_sheet_1.append(
            pandas.Series(
                [
                    asset_reference_number,
                    "novo",
                    asset_reference_number,
                    asset_description,
                    "Para maiores informações, clique em ANEXOS",
                    asset_initial_value,
                    0,
                    0,
                    asset_increment_value,
                    asset_reference_value,
                    asset_owner_name,
                    asset_location_city,
                    asset_location_state,
                    asset_manager_name,
                    "",
                    "",
                    "",
                    "",
                    "1",
                    "",
                    "Em arquivo separado",
                ],
                index=dataset_sheet_1.columns,
            ),
            ignore_index=True,
        )

        dataset_sheet_2 = dataset_sheet_2.append(df)

        print("INFO: Linha da planilha colunada montada com sucesso")
    except Exception as error:
        print(
            "ERROR: {} ao tentar processar o arquivo {}".format(error, excel_file_name)
        )

print("INFO: Gerando o arquivo Excel resultante")

print("DEBUG: Montando o objeto de geração do arquivo Excel")
excel_file = pandas.ExcelWriter(
    os.path.join(output_folder, excel_folder, "resulting_spreadsheet.xlsx"),
    engine="xlsxwriter",
)

print("DEBUG: Escrevendo na primeira aba da planilha o conteúdo da colunada")
dataframe_sheet_1 = pandas.DataFrame(dataset_sheet_1)
dataframe_sheet_1.to_excel(excel_file, sheet_name="Colunada", index=False)

print("DEBUG: Escrevendo na segunda aba da planilha o conteúdo da listagem")
dataframe_sheet_2 = pandas.DataFrame(dataset_sheet_2)
dataframe_sheet_2.to_excel(excel_file, sheet_name="Listagem", index=False)

print("DEBUG: Salvando e fechando o arquivo Excel resultante")
excel_file.save()

print("INFO: Arquivo Excel gerado com sucesso")

done = str(
    input("INFO: Processo finalizado com sucesso. Pressione enter para continuar...")
)
