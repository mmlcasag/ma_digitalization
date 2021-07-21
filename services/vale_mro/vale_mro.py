import os
import pandas
import openpyxl
import warnings

import utils.os as os_utils
import utils.ma as ma_utils
import utils.html as html_utils
import utils.excel as excel_utils
from services.base.logger import Logger

logger = Logger.__call__().get_logger()

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
warnings.filterwarnings("ignore", category=UserWarning, module="xlsxwriter")

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

dataset_sheet_1 = pandas.DataFrame(columns=ma_utils.get_spreadsheet_columns())
dataset_sheet_2 = pandas.DataFrame()

allowed_extensions = ["xlsx", "xlsb", "xlsm", "xls"]


def get_asset_full_description(dataframe, asset_number):
    asset_full_description = ""

    asset_full_description = (
        asset_full_description
        + "Código do Produto: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number][
                "Código do Produto"
            ][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Descrição do Produto: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number][
                "Descrição do Produto"
            ][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Referência do Produto: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number][
                "Referência do Produto"
            ][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Centro: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number]["Centro"][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Depósito: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number]["Depósito"][
                0
            ]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Código do Grupo: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number][
                "Código do Grupo"
            ][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Descrição do Grupo: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number][
                "Descrição do Grupo"
            ][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Nome do Fabricante: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number][
                "Nome do Fabricante"
            ][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Quantidade: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number][
                "Quantidade"
            ][0]
        )
        + "<br>"
    )
    asset_full_description = (
        asset_full_description
        + "Unidade: {}".format(
            dataframe.loc[dataframe["Lote de Referência"] == asset_number]["Unidade"][0]
        )
        + "<br>"
    )

    return asset_full_description


# flake8: noqa: C901
for excel_file_name in os_utils.get_files_list(input_folder, allowed_extensions):
    try:
        logger.info('PROCESSANDO O ARQUIVO "{}"'.format(excel_file_name))

        file_name = os_utils.get_file_name(excel_file_name)

        logger.info('Nome do arquivo sem extensão "{}"'.format(file_name))

        try:
            logger.info("Extraindo imagens do arquivo Excel")

            input_path = os.path.join(absolute_path, input_folder, excel_file_name)
            output_path = os.path.join(
                absolute_path,
                output_folder,
                images_folder,
                file_name,
            )

            excel_utils.extract_images_from_xlsx(input_path, output_path)
        except Exception as error:
            logger.error(
                "Erro {} ao tentar extrair as imagens do arquivo Excel".format(error)
            )

        xls_to_exclude = ""
        if excel_file_name.endswith("xlsb"):
            logger.info("Convertendo arquivo de XLSB para XLSX")
            input_path = os.path.join(input_folder, excel_file_name)
            xls = pandas.ExcelFile(input_path, engine="pyxlsb")
            writer = pandas.ExcelWriter(
                input_path.replace("xlsb", "xlsx"), engine="xlsxwriter"
            )

            for sheet in xls.sheet_names:
                df = pandas.read_excel(xls, sheet_name=sheet)
                df.to_excel(writer, sheet_name=sheet, index=False)

            writer.save()
            writer.close()
            excel_file_name = excel_file_name.replace("xlsb", "xlsx")
            xls_to_exclude = input_path.replace("xlsb", "xlsx")
            logger.info("Conversão de XLSB para XLSX concluída com sucesso")

        logger.info("Abrindo o arquivo Excel")
        workbook = openpyxl.load_workbook(
            os.path.join(input_folder, excel_file_name), data_only=True
        )

        logger.info("Selecionando a aba ativa da planilha")

        sheets_to_remove = ["Principal", "Lista CMD", "Relação Grupo Mercadorias"]
        sheet_names = workbook.sheetnames
        for element in sheets_to_remove:
            if element in sheet_names:
                sheet_names.remove(element)

        sheet = workbook[sheet_names[0]]

        logger.info(
            'Deletando linhas até que a primeira linha seja "Cód", "Descrição" ou algo do gênero'
        )
        excel_utils.delete_until(
            sheet, ["Cód.", "Centro", "Depósito", "Material", "Descrição", "Processo"]
        )

        logger.info("Exportando o resultado para um arquivo CSV")
        excel_utils.export_to_csv(
            sheet,
            os.path.join(output_folder, csv_folder, file_name + ".csv"),
            ";",
            ",",
        )

        logger.info("Fechando o arquivo Excel")
        workbook.close()

        logger.info("Carregando um dataset com os dados do arquivo CSV")
        df = pandas.read_csv(
            os.path.join(output_folder, csv_folder, file_name + ".csv"), delimiter=";"
        )

        logger.info(
            "Convertendo todas as colunas do dataset da primeira aba para texto"
        )
        df = df.astype(str)

        logger.info(
            "Desconsiderando as linhas cujos valores de todas as colunas estão vazios ou inválidos"
        )
        df = df.mask(df.eq("None")).dropna(how="all")
        df = df.mask(df.eq("None")).fillna("")

        logger.info("Ajustando os nomes das colunas")
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

        logger.info(
            "Desconsiderando colunas desnecessárias para o processamento do arquivo"
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

        logger.info("Ordenando dados pelo número do lote e pelo código do produto")
        df = df.sort_values(["Lote de Referência", "Código do Produto"], ascending=True)

        count_products = int(df.count()["Código do Produto"])
        logger.info("Quantidade de produtos no lote: {}".format(count_products))

        if count_products == 1:
            logger.warning(
                "Não será gerado arquivo HTML pois lote possui apenas um produto"
            )
        else:
            logger.info("Exportando os produtos do lote para um arquivo HTML")

            logger.info("Carregando um dataset para geração do arquivo HTML")
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

            logger.info("Gerando código HTML a partir dos dados do dataset")
            html_content = df_html.to_html(index=False, na_rep="")

            logger.info("Concatenando o cabeçalho e o rodapé do arquivo HTML")
            html_content = (
                html_utils.get_header() + html_content + html_utils.get_footer()
            )

            logger.info("Criando o arquivo HTML")
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

            logger.info("Escrevendo no arquivo HTML")
            html_file.write(html_content)

            logger.info("Fechando o arquivo HTML")
            html_file.close()

            logger.info("Exportação do arquivo HTML finalizada com sucesso")

        logger.info("Montando a linha da planilha colunada")

        logger.info("Buscando o nome do responsável do lote")
        try:
            asset_manager_name = df["Responsável"][0]
        except Exception as error:
            logger.error(
                "{} ao tentar buscar o nome do responsável do lote".format(error)
            )
            asset_manager_name = ""

        logger.info("Buscando o nome da empresa do lote")
        try:
            asset_owner_name = df["Empresa"][0]
        except Exception as error:
            logger.error("{} ao tentar buscar o nome da empresa do lote".format(error))
            asset_owner_name = "Vale"

        logger.info("Buscando o município e o estado do lote")
        try:
            asset_location = ma_utils.split_city_and_state(df["Localização"][0])
            asset_location_city = asset_location[0]
            asset_location_state = asset_location[1]
        except Exception as error:
            logger.error(
                "{} ao tentar buscar o município e o estado do lote".format(error)
            )
            asset_location_city = ""
            asset_location_state = ""

        logger.info("Buscando o número do lote de referência")
        try:
            asset_reference_number = df["Lote de Referência"][0]
        except Exception as error:
            logger.error(
                "{} ao tentar buscar o número do lote de referência".format(error)
            )
            asset_reference_number = ""

        logger.info("Definindo a descrição resumida do lote")
        try:
            asset_description = ma_utils.get_asset_description(
                df, "Descrição do Produto", "Valor Total", 5
            )
        except Exception as error:
            logger.error(
                "{} ao tentar definir a descrição resumida do lote".format(error)
            )
            asset_description = ""

        logger.info("Buscando o valor de referência do lote")
        try:
            df["Valor Total"] = df["Valor Total"].apply(
                lambda n: float(n.replace(",", ".") if n else 0)
            )
            asset_reference_value = round(df["Valor Total"].astype(float).sum(), 2)
        except Exception as error:
            logger.error(
                "{} ao tentar buscar o valor de referência do lote".format(error)
            )
            asset_reference_value = 0

        logger.info("Buscando o valor inicial do lote")
        try:
            asset_initial_value = round(float(asset_reference_value / 100), 2)
        except Exception as error:
            logger.error("{} ao tentar buscar o valor inicial do lote".format(error))
            asset_initial_value = 0

        logger.info("Buscando o valor de incremento do lote")
        try:
            asset_increment_value = int(
                ma_utils.get_closest_value(
                    ma_utils.get_available_increments(), asset_initial_value / 10
                )
            )
        except Exception as error:
            logger.error(
                "{} ao tentar buscar o valor de incremento do lote".format(error)
            )
            asset_increment_value = 0

        if count_products == 1:
            asset_full_description = get_asset_full_description(
                df, asset_reference_number
            )
            asset_html_description = ""
        else:
            asset_full_description = "Para maiores informações, clique em ANEXOS"
            asset_html_description = "Em arquivo separado"

        logger.info("Gerando a linha colunada do lote")
        dataset_sheet_1 = dataset_sheet_1.append(
            pandas.Series(
                [
                    asset_reference_number,
                    "novo",
                    asset_reference_number,
                    asset_description,
                    asset_full_description,
                    asset_initial_value,
                    "",
                    "",
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
                    asset_html_description,
                ],
                index=dataset_sheet_1.columns,
            ),
            ignore_index=True,
        )
        logger.info("Linha da planilha colunada montada com sucesso")

        logger.info("Gerando linhas da planilha de listagem")
        dataset_sheet_2 = dataset_sheet_2.append(df)
        logger.info("Linhas da planilha de listagem montadas com sucesso")
    except Exception as error:
        logger.error(
            "{} ao tentar processar o arquivo {}".format(error, excel_file_name)
        )
    finally:
        try:
            logger.info("Excluindo arquivo XLSX gerado da conversão do XLSB")
            if xls_to_exclude:
                if os.path.isfile(xls_to_exclude):
                    file = open(xls_to_exclude, "wb")
                    file.close()
                    os.remove(xls_to_exclude)
            logger.info("Arquivo XLSX gerado da conversão do XLSB excluído com sucesso")
        except Exception as error:
            logger.error(
                "Erro {} ao tentar excluir o arquivo XLSX gerado da conversão do XLSB".format(
                    error
                )
            )

logger.info("Gerando o arquivo Excel resultante")

logger.info("Montando o objeto de geração do arquivo Excel")
excel_file = pandas.ExcelWriter(
    os.path.join(output_folder, excel_folder, "resulting_spreadsheet.xlsx"),
    engine="xlsxwriter",
)

logger.info("Escrevendo na primeira aba da planilha o conteúdo da colunada")
dataframe_sheet_1 = pandas.DataFrame(dataset_sheet_1)
dataframe_sheet_1.to_excel(excel_file, sheet_name="Colunada", index=False)

logger.info("Escrevendo na segunda aba da planilha o conteúdo da listagem")
dataframe_sheet_2 = pandas.DataFrame(dataset_sheet_2)
dataframe_sheet_2.to_excel(excel_file, sheet_name="Listagem", index=False)

logger.info("Salvando e fechando o arquivo Excel resultante")
excel_file.save()

logger.info("Arquivo Excel gerado com sucesso")

logger.info("Processo finalizado com sucesso.")
done = str(input("Pressione ENTER para encerrar..."))
