import os
import sys
import pandas
import openpyxl

path = "..{}..".format(os.sep)
sys.path.append(path)

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
images_folder = "images"

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(output_folder, csv_folder)
os_utils.create_folder(output_folder, html_folder)
os_utils.create_folder(output_folder, excel_folder)
os_utils.create_folder(output_folder, images_folder)

allowed_extensions = ["xlsx", "xlsb", "xlsm"]

for excel_file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        print('INFO: PROCESSANDO O ARQUIVO "{}"'.format(excel_file_name))

        file_name = os_utils.get_file_name(excel_file_name)

        print('DEBUG: Nome do arquivo sem extensão "{}"'.format(file_name))

        dataset_sheet_1 = pandas.DataFrame(columns=ma_utils.get_spreadsheet_columns())

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

        print('INFO: Selecionando a aba de nome "1. Materiais"')
        sheet = workbook["1. Materiais"]

        print('DEBUG: Deletando linhas até chegar em "NM"')
        excel_utils.delete_until(sheet, "NM")

        print("INFO: Exportando o resultado da aba para um arquivo CSV")
        excel_utils.export_to_csv(
            sheet,
            os.path.join(output_folder, csv_folder, file_name + "_sheet_1.csv"),
            ";",
            ",",
        )

        print('INFO: Selecionando a aba de nome "2. Lotes"')
        sheet = workbook["2. Lotes"]

        print("DEBUG: Deletando a primeira coluna")
        sheet.delete_cols(1, 1)

        print('DEBUG: Deletando linhas até chegar em "Nº do Lote"')
        excel_utils.delete_until(sheet, "Nº do Lote")

        print("INFO: Exportando o resultado da aba para um arquivo CSV")
        excel_utils.export_to_csv(
            sheet,
            os.path.join(output_folder, csv_folder, file_name + "_sheet_2.csv"),
            ";",
            ",",
        )

        print("DEBUG: Fechando o arquivo Excel")
        workbook.close()

        print("INFO: Carregando um dataset com os dados do arquivo CSV da primeira aba")
        df1 = pandas.read_csv(
            os.path.join(output_folder, csv_folder, file_name + "_sheet_1.csv"),
            delimiter=";",
        )

        print(
            "DEBUG: Convertendo todas as colunas do dataset da primeira aba para texto"
        )
        df1 = df1.astype(str)

        print(
            "DEBUG: Mantendo apenas as primeiras 13 colunas do dataset da primeira aba e desconsiderando o resto"
        )
        df1_cols = list(df1.columns.values)
        df1 = df1[df1_cols[0:13]]

        print("INFO: Carregando um dataset com os dados do arquivo CSV da segunda aba")
        df2 = pandas.read_csv(
            os.path.join(output_folder, csv_folder, file_name + "_sheet_2.csv"),
            delimiter=";",
        )

        print(
            "DEBUG: Convertendo todas as colunas do dataset da segunda aba para texto"
        )
        df2 = df2.astype(str)

        print(
            "DEBUG: Mantendo apenas as primeiras 6 colunas do dataset da segunda aba e desconsiderando o resto"
        )
        df2_cols = list(df2.columns.values)
        df2 = df2[df2_cols[0:6]]

        print("DEBUG: Varrendo por números de lote únicos no dataset da primeira aba")
        for asset_number in df1["Número do Lote"].unique():
            try:
                print("INFO: Processando o lote de número: {}".format(asset_number))

                if str(asset_number) == "None":
                    print("WARNING: Número do Lote inválido. Desconsiderando a linha")
                    continue

                print("DEBUG: Carregando um dataset apenas com os produtos desse lote")
                local_df1 = df1.loc[df1["Número do Lote"] == str(asset_number)]
                local_df1 = local_df1.reset_index(drop=True)
                local_df1_cols = list(local_df1.columns.values)

                print(
                    "DEBUG: Carregando um dataset apenas com os valores totais desse lote"
                )
                local_df2 = df2.loc[df2["Nº do Lote"] == str(asset_number)]
                local_df2 = local_df2.reset_index(drop=True)
                local_df2_cols = list(local_df2.columns.values)

                print("INFO: Exportando os produtos do lote para um arquivo HTML")

                print(
                    "DEBUG: Carregando um dataset baseado no dataset da primeira aba, porém sem valores totais para geração do HTML"
                )
                html_df = local_df1[
                    local_df1_cols[0:7] + [local_df1_cols[8]] + [local_df1_cols[7]]
                ]

                print("DEBUG: Gerando código HTML a partir dos dados do dataset")
                html_content = html_df.to_html(index=False, na_rep="")

                print("DEBUG: Concatenando o cabeçalho e o rodapé do arquivo HTML")
                html_content = (
                    html_utils.get_header() + html_content + html_utils.get_footer()
                )

                print("DEBUG: Montando o nome completo do arquivo HTML a ser criado")
                html_file_name = os.path.join(
                    output_folder,
                    html_folder,
                    file_name + "_" + str(asset_number) + ".html",
                )

                print("DEBUG: Criando o arquivo HTML")
                html_file = open(html_file_name, "w", newline="", encoding="utf-8")

                print("DEBUG: Escrevendo no arquivo HTML")
                html_file.write(html_content)

                print("DEBUG: Fechando o arquivo HTML")
                html_file.close()

                print("INFO: Exportação do arquivo HTML finalizada com sucesso")

                print("INFO: Montando a linha da planilha colunada")

                print("DEBUG: Definindo a descrição resumida do lote")
                asset_description = ma_utils.get_asset_description(
                    local_df1, "TEXTO BREVE", "VALOR CONTÁBIL ATUAL", 5
                )

                print("DEBUG: Buscando o valor de referência do lote")
                asset_reference_value = round(
                    float(local_df2.at[0, "Valor contábil total"]), 2
                )

                print("DEBUG: Buscando o valor inicial do lote")
                asset_initial_value = round(
                    float(local_df2.at[0, "Lance de Partida Leilão"]), 2
                )

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
                            asset_number,
                            asset_description,
                            "Para maiores informações, clique em ANEXOS",
                            asset_initial_value,
                            0,
                            0,
                            asset_increment_value,
                            asset_reference_value,
                            "Petrobrás",
                            "",
                            "",
                            "Vendedor",
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

                print("INFO: Linha da planilha colunada montada com sucesso")
            except Exception as error:
                print(
                    "ERROR: {} ao tentar processar o lote {}".format(
                        error, asset_number
                    )
                )

        print("INFO: Gerando o arquivo Excel resultante")

        print("DEBUG: Montando o objeto de geração do arquivo Excel")
        excel_file = pandas.ExcelWriter(
            os.path.join(output_folder, excel_folder, file_name + ".xlsx"),
            engine="xlsxwriter",
        )

        print("DEBUG: Escrevendo na primeira aba da planilha o conteúdo da colunada")
        dataframe_sheet_1 = pandas.DataFrame(dataset_sheet_1)
        dataframe_sheet_1.to_excel(excel_file, sheet_name="Colunada", index=False)

        print(
            "DEBUG: Escrevendo na segunda aba da planilha a listagem total de produtos"
        )
        dataframe_sheet_2 = pandas.DataFrame(df1)
        dataframe_sheet_2.to_excel(excel_file, sheet_name="Listagem", index=False)

        print("DEBUG: Salvando e fechando o arquivo Excel resultante")
        excel_file.save()

        print("INFO: Arquivo Excel gerado com sucesso")
    except Exception as error:
        print(
            "ERROR: {} ao tentar processar o arquivo {}".format(error, excel_file_name)
        )

print("INFO: Processo finalizado com sucesso")
