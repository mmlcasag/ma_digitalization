import os
import sys
import pandas
import openpyxl

sys.path.append("..\..")

import utils.os as os_utils
import utils.ma as ma_utils
import utils.html as html_utils
import utils.excel as excel_utils

absolute_path = os.getcwd()

input_folder = "input"
output_folder = "output"
csv_folder = "csv"
html_folder = "html"
excel_folder = "xlsx"

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(os.path.join(output_folder, csv_folder))
os_utils.create_folder(os.path.join(output_folder, html_folder))
os_utils.create_folder(os.path.join(output_folder, excel_folder))

dataset_sheet_1 = pandas.DataFrame(columns=ma_utils.get_spreadsheet_columns())
dataset_sheet_2 = pandas.DataFrame()

asset_number = 0

allowed_extensions = ["xlsx", "xlsb"]

for excel_file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        print('INFO: PROCESSANDO O ARQUIVO "{}"'.format(excel_file_name))

        asset_number = asset_number + 1

        file_name = os_utils.get_file_name(excel_file_name)

        print('DEBUG: Nome do arquivo sem extensão "{}"'.format(file_name))

        print("INFO: Abrindo o arquivo Excel")
        workbook = openpyxl.load_workbook(
            os.path.join(input_folder, excel_file_name), data_only=True
        )

        print("INFO: Selecionando a aba ativa da planilha")
        sheet = workbook.active

        print('DEBUG: Deletando linhas até chegar em "Cód."')
        excel_utils.delete_until(sheet, "Cód.")

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
        df = df.rename(columns={"PMM": "Unitário", "Valor": "Total", "UM": "UN"})

        print(
            "DEBUG: Carregando um dataset baseado no dataset principal, para ser utilizado na geração da aba de listagem"
        )
        df_listagem = df

        print("DEBUG: Removendo colunas desnecessárias do dataset da aba de listagem")
        unwanted_columns = [
            "Motivo",
            "Analista",
            "Aprovador",
            "Diretoria",
            "Gerência",
            "Código Grupo de mercadorias",
            "Descrição do grupo de mercadorias",
            "Preço da última compra ou valor comercial\n(PREÇO UNITÁRIO)",
            "Endereço do item",
            "Campo de conferência para armazem",
            "Campo de conferência para CMD (opcional)",
            "Peso estimado em Kg",
            "Valor estimado do sucateamento",
            "Responsável CMD",
            "CMD / Mina\n(selecionar a opção da lista)",
            "Cidade / Estado\n(onde se encontra o lote fisicamente)",
        ]
        df_listagem = df_listagem.drop(columns=unwanted_columns)

        print("INFO: Exportando os produtos do lote para um arquivo HTML")

        print(
            "DEBUG: Carregando um dataset baseado no dataset do arquivo Excel, para ser utilizado na geração do HTML"
        )
        df_html = df_listagem

        print("DEBUG: Removendo colunas desnecessárias do dataset do arquivo HTML")
        df_html = df_html.drop(columns=["Unitário", "Total"])

        print("DEBUG: Movendo colunas de posição no dataset do arquivo HTML")
        cols = list(df_html.columns.values)
        df_html = df_html[cols[0:4] + cols[5:8] + [cols[4]] + [cols[8]]]

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
        asset_manager_name = df["Responsável CMD"][0]

        print("DEBUG: Buscando o nome da unidade do lote")
        asset_owner_name = df["CMD / Mina\n(selecionar a opção da lista)"][0]

        print("DEBUG: Buscando o município e o estado do lote")
        asset_location = df["Cidade / Estado\n(onde se encontra o lote fisicamente)"][0]
        asset_location = asset_location.replace(" / ", "/")
        asset_location = asset_location.replace(" - ", "-")
        asset_location = asset_location.replace("-", "/")
        asset_location = asset_location.replace(" ", "/")
        asset_location = asset_location.split("/")
        asset_location_city = asset_location[0]
        asset_location_state = asset_location[1]

        print("DEBUG: Buscando o número de referência do lote")
        asset_reference_number = df["Nº lote"][0]

        print("DEBUG: Definindo a descrição resumida do lote")
        asset_description = ma_utils.get_asset_description(df, "Descrição", "Total", 5)

        print("DEBUG: Buscando o valor de referência do lote")
        asset_reference_value = round(df["Total"].astype(float).sum(), 2)

        print("DEBUG: Buscando o valor inicial do lote")
        asset_initial_value = round(float(asset_reference_value / 100), 2)

        print("DEBUG: Buscando o valor de incremento do lote")
        asset_increment_value = int(
            ma_utils.get_closest_value(
                ma_utils.get_available_increments(), asset_initial_value / 10
            )
        )

        print("DEBUG: Gerando a linha colunada do lote")
        dataset_sheet_1 = dataset_sheet_1.append(
            pandas.Series(
                [
                    asset_number,
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

        dataset_sheet_2 = dataset_sheet_2.append(df_listagem)

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

print("INFO: Processo finalizado com sucesso")
