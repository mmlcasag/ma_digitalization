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

input_folder = "input"
output_folder = "output"
csv_folder = "csv"
html_folder = "html"
excel_folder = "xlsx"

os_utils.create_folder(input_folder)
os_utils.create_folder(output_folder)
os_utils.create_folder(output_folder, csv_folder)
os_utils.create_folder(output_folder, html_folder)
os_utils.create_folder(output_folder, excel_folder)

allowed_extensions = ["xlsx", "xlsb", "xlsm"]

for excel_file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        print('INFO: PROCESSANDO O ARQUIVO "{}"'.format(excel_file_name))

        file_name = os_utils.get_file_name(excel_file_name)

        print('DEBUG: Nome do arquivo sem extensão "{}"'.format(file_name))

        dataset_sheet_1 = pandas.DataFrame(columns=ma_utils.get_spreadsheet_columns())

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

        print("DEBUG: Deletando a primeira linha")
        sheet.delete_rows(1, 1)

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

        print("DEBUG: Ajustando os nomes das colunas")
        df1 = df1.rename(
            columns={
                "NM": "Código do Produto",
                "TEXTO BREVE": "Descrição do Produto",
                "GM": "Código do Grupo",
                "Descrição GM": "Descrição do Grupo",
                "Fabricante": "Nome do Fabricante",
                "AVALIAÇÃO": "Avaliação",
                "QTD ATUAL": "Quantidade",
                "UM": "Unidade",
                "Valor Contábil Unitário": "Valor Unitário",
                "VALOR CONTÁBIL ATUAL": "Valor Total",
                "Número do Lote": "Número do Lote",
                "Descrição do lote": "Descrição do Lote",
            }
        )

        print(
            "DEBUG: Desconsiderando colunas desnecessárias para o processamento do arquivo"
        )
        df1 = df1.reindex(
            columns=[
                "Código do Produto",
                "Descrição do Produto",
                "Código do Grupo",
                "Descrição do Grupo",
                "Nome do Fabricante",
                "Avaliação",
                "Quantidade",
                "Unidade",
                "Valor Unitário",
                "Valor Total",
                "Número do Lote",
                "Descrição do Lote",
            ]
        )

        print("INFO: Carregando um dataset com os dados do arquivo CSV da segunda aba")
        df2 = pandas.read_csv(
            os.path.join(output_folder, csv_folder, file_name + "_sheet_2.csv"),
            delimiter=";",
        )

        print(
            "DEBUG: Convertendo todas as colunas do dataset da segunda aba para texto"
        )
        df2 = df2.astype(str)

        print("DEBUG: Ajustando os nomes das colunas")
        df2 = df2.rename(
            columns={
                "Unidade": "Unidade",
                "Localização": "Localização",
                "Nº do Lote": "Número do Lote",
                "Descrição do lote": "Descrição do Lote",
                "Valor contábil total": "Valor Total",
                "Lance de Partida Leilão": "Valor Inicial",
            }
        )

        print(
            "DEBUG: Desconsiderando colunas desnecessárias para o processamento do arquivo"
        )
        df2 = df2.reindex(
            columns=[
                "Unidade",
                "Localização",
                "Número do Lote",
                "Descrição do Lote",
                "Valor Total",
                "Valor Inicial",
            ]
        )

        print("DEBUG: Varrendo por números de lote únicos no dataset da primeira aba")
        for asset_number in df1["Número do Lote"].unique():
            try:
                print("INFO: Processando o lote de número: {}".format(asset_number))

                if asset_number == "None":
                    print("WARNING: Número do Lote inválido. Desconsiderando a linha")
                    continue

                print("DEBUG: Carregando um dataset apenas com os produtos desse lote")
                local_df1 = df1.loc[df1["Número do Lote"] == asset_number]
                local_df1 = local_df1.reset_index(drop=True)
                local_df1_cols = list(local_df1.columns.values)

                print(
                    "DEBUG: Carregando um dataset apenas com os valores totais desse lote"
                )
                local_df2 = df2.loc[df2["Número do Lote"] == asset_number]
                local_df2 = local_df2.reset_index(drop=True)
                local_df2_cols = list(local_df2.columns.values)

                print("INFO: Exportando os produtos do lote para um arquivo HTML")

                print(
                    "DEBUG: Carregando um dataset baseado no dataset da primeira aba, porém sem valores totais para geração do HTML"
                )
                html_df = local_df1.reindex(
                    columns=[
                        "Código do Produto",
                        "Descrição do Produto",
                        "Código do Grupo",
                        "Descrição do Grupo",
                        "Nome do Fabricante",
                        "Avaliação",
                        "Quantidade",
                        "Unidade",
                        "Valor Unitário",
                        "Valor Total",
                        "Número do Lote",
                    ]
                )

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
                    file_name + "_" + asset_number + ".html",
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
                try:
                    asset_description = ma_utils.get_asset_description(
                        local_df1, "Descrição do Produto", "Valor Total", 5
                    )
                except Exception as error:
                    print(
                        "ERROR: {} ao tentar definir a descrição resumida do lote".format(
                            error
                        )
                    )
                    asset_description = ""

                print("DEBUG: Buscando o nome da unidade do lote")
                try:
                    asset_owner_name = local_df2.at[0, "Unidade"]
                except Exception as error:
                    print(
                        "ERROR: {} ao tentar buscar o nome da unidade do lote".format(
                            error
                        )
                    )
                    asset_owner_name = "Petrobrás"

                print("DEBUG: Buscando o município e o estado do lote")
                try:
                    asset_location = ma_utils.split_city_and_state(
                        local_df2.at[0, "Localização"]
                    )
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

                print("DEBUG: Buscando o valor de referência do lote")
                try:
                    asset_reference_value = round(
                        float(local_df2.at[0, "Valor Total"]), 2
                    )
                except Exception as error:
                    print(
                        "ERROR: {} ao tentar buscar o valor de referência do lote".format(
                            error
                        )
                    )
                    asset_reference_value = 0

                print("DEBUG: Buscando o valor inicial do lote")
                try:
                    asset_initial_value = round(
                        float(local_df2.at[0, "Valor Inicial"]), 2
                    )
                except Exception as error:
                    print(
                        "ERROR: {} ao tentar buscar o valor inicial do lote".format(
                            error
                        )
                    )
                    asset_initial_value = 0

                print("DEBUG: Buscando o valor de incremento do lote")
                try:
                    asset_increment_value = int(
                        ma_utils.get_closest_value(
                            ma_utils.get_available_increments(),
                            asset_initial_value / 10,
                        )
                    )
                except Exception as error:
                    print(
                        "ERROR: {} ao tentar buscar o valor de incremento do lote".format(
                            error
                        )
                    )
                    asset_increment_value = 0

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
                            asset_owner_name,
                            asset_location_city,
                            asset_location_state,
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
                    "ERROR: {} ao tentar processar o lote de número {}".format(
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

        print("DEBUG: Escrevendo na segunda aba da planilha o conteúdo da listagem")
        dataframe_sheet_2 = pandas.DataFrame(df1)
        dataframe_sheet_2.to_excel(excel_file, sheet_name="Listagem", index=False)

        print("DEBUG: Salvando e fechando o arquivo Excel resultante")
        excel_file.save()

        print("INFO: Arquivo Excel gerado com sucesso")
    except Exception as error:
        print(
            "ERROR: {} ao tentar processar o arquivo {}".format(error, excel_file_name)
        )

done = str(
    input("INFO: Processo finalizado com sucesso. Pressione enter para continuar...")
)
