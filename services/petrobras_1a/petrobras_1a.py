import os
import pandas as pd
from services.base.spreadsheet_converter import SpreadsheetConverter
from services.base.images_handler import ImageHandler
from services.base.logger import Logger
import re
import utils.ma as ma_utils
import utils.html as html_utils

logger = Logger.__call__().get_logger()


class PetrobrasConverter(SpreadsheetConverter):
    def create_city_mapper(self, dataframe):
        logger.info("Criando o mapper de cidade")
        mapper_lot_city = {}
        for n_lot, local in zip(dataframe["Lote"], dataframe["Local de Armazenamento"]):
            if isinstance(n_lot, list):
                for lot_in_dictionary in n_lot:
                    mapper_lot_city[lot_in_dictionary] = ma_utils.split_city_and_state(
                        local
                    )[0]
            else:
                mapper_lot_city[n_lot] = ma_utils.split_city_and_state(local)[0]

        return mapper_lot_city

    def create_state_mapper(self, dataframe):
        logger.info("Criando o mapper de estados")
        mapper_lot_state = {}
        for n_lot, local in zip(dataframe["Lote"], dataframe["Local de Armazenamento"]):
            if isinstance(n_lot, list):
                for lot_in_dictionary in n_lot:
                    mapper_lot_state[lot_in_dictionary] = ma_utils.split_city_and_state(
                        local
                    )[1]
            else:
                mapper_lot_state[n_lot] = ma_utils.split_city_and_state(local)[1]

        return mapper_lot_state

    def create_lot_name_mapper(self, dataframe):
        logger.info("Criando o mapper para o name dos lotes")
        map_product_value = {}

        for i, row in dataframe.iterrows():
            key = row["Número do Lote"]
            product_desc = row["Descrição do Produto"]
            product_value = row["Valor Total"]

            if key not in map_product_value:
                map_product_value[key] = []

            product_info = {"desc": product_desc, "value": product_value}
            map_product_value[key].append(product_info)

        product_value_description = {}

        for dt in map_product_value:
            product_value_description[dt] = ma_utils.get_asset_description(
                pd.DataFrame(map_product_value[dt]), "desc", "value", 5
            )

        return product_value_description

    def process_file(self, file):
        xls = pd.ExcelFile(file)
        df1 = pd.read_excel(xls, "RESUMO - LOTES E VMA", header=1, usecols="A")
        df2 = pd.read_excel(xls, "RESUMO - LOTES E VMA", header=1, usecols="F:K")

        first_colum_data = df1.to_dict("list")
        values_columns_data = df2.to_dict("list")

        vi = []
        increment = []
        for value in values_columns_data["Lance de Partida"]:
            new_value = round(value, 2)
            vi.append(value)
            new_increment = ma_utils.get_closest_value(
                ma_utils.get_available_increments(), new_value / 10
            )
            increment.append(new_increment)

        colunada = dict()
        colunada["Nº do lote"] = first_colum_data["LOTES"]
        colunada["Status"] = "novo"
        colunada["Lote Ref. / Ativo-Frota"] = first_colum_data["LOTES"]
        colunada["Nome do Lote (SEMPRE MAIUSCULA)"] = ""
        colunada[
            "Descrição"
        ] = "No anexo, consta a coluna Percentual de representação do item no Lote, pois será previsto no edital o desconto do percentual caso o item não estiver disponível para venda."
        colunada["VI"] = vi
        colunada["VMV"] = "0"
        colunada["VER"] = "0"
        colunada["Incremento"] = increment
        colunada["Valor de Referência do Vendedor (Contábil)"] = values_columns_data[
            "VMA Total do Lote"
        ]
        colunada["Comitente"] = "Petrobras"
        colunada["Município"] = ""
        colunada["UF"] = ""
        colunada["Assessor"] = "Vendedor"
        colunada["Pendências"] = ""
        colunada["Restrições"] = ""
        colunada["Débitos (Total)"] = ""
        colunada["Unid. Métrica"] = ""
        colunada["Fator Multiplicativo"] = "1"
        colunada["Alteração/Adicionado"] = ""
        colunada["Descrição HTML"] = "Em arquivo separado"

        items_df = pd.read_excel(xls, "LISTA DOS ITENS")
        items_df["Lote"] = items_df["Lote"].apply(lambda n: n if n % 1 else int(n))

        mapper_lote_city = self.create_city_mapper(items_df)
        mapper_lote_state = self.create_state_mapper(items_df)

        items_dc = items_df.to_dict("list")

        listagem = dict()
        listagem["Código do Produto"] = items_dc["Material"]
        listagem["Descrição do Produto"] = items_dc["Descrição do Material"]
        listagem["Avaliação"] = items_dc["Tipo de Avaliação"]
        listagem["Quantidade"] = items_dc["Quantidade"]
        listagem["Unidade"] = items_dc["Unidade"]
        listagem["Valor Unitário"] = items_dc["VMA - Unitário"]
        listagem["Valor Total"] = items_dc["VMA - Total"]
        listagem["Percentual do Item em Relação ao Lote"] = items_dc[
            "Percentual do Item em Relação ao Lote"
        ]
        listagem["Número do Lote"] = items_dc["Lote"]

        colunada_sheet = pd.DataFrame(colunada)
        logger.info("Aplicando mapper de cidade")
        colunada_sheet["Município"] = colunada_sheet["Nº do lote"].map(mapper_lote_city)

        logger.info("Aplicando mapper de estado")
        colunada_sheet["UF"] = colunada_sheet["Nº do lote"].map(mapper_lote_state)
        colunada_sheet.drop(colunada_sheet.tail(1).index, inplace=True)

        listagem_sheet = pd.DataFrame(listagem)
        listagem_sheet["Percentual do Item em Relação ao Lote"] = pd.Series(
            [
                "{0:.2f}%".format(val * 100)
                for val in listagem_sheet["Percentual do Item em Relação ao Lote"]
            ],
            index=listagem_sheet.index,
        )

        logger.info("Aplicando mapper para nome do lote")
        product_value_name = self.create_lot_name_mapper(listagem_sheet)

        colunada_sheet["Nome do Lote (SEMPRE MAIUSCULA)"] = colunada_sheet[
            "Nº do lote"
        ].map(product_value_name)

        file_name = os.path.basename(file).replace("xlsm", "xlsx")
        filepath = os.path.join("output", "xlsx", file_name)

        logger.info("Buscando lotes contendo apenas um produto")
        lots_to_remove = []
        for i, dataframe_group in listagem_sheet.groupby("Número do Lote"):
            lot_number = dataframe_group["Número do Lote"].iloc[0]

            count_products = int(dataframe_group["Código do Produto"].count())
            if count_products == 1:
                lots_to_remove.append(lot_number)

        logger.info("Ajustando campos da aba colunada para lotes com apenas um produto")
        for lot_number in lots_to_remove:
            colunada_sheet.loc[
                colunada_sheet["Nº do lote"] == lot_number,
                ["Descrição", "Descrição HTML"],
            ] = ["", ""]

        logger.info("Removendo da aba de listagem os lotes contendo apenas um produto")
        listagem_sheet = listagem_sheet[
            ~listagem_sheet["Número do Lote"].isin(lots_to_remove)
        ]

        logger.info("Criando arquivo xlsx de saída")
        writer = pd.ExcelWriter(filepath, engine="xlsxwriter")
        colunada_sheet.to_excel(writer, sheet_name="Colunada", index=False)
        listagem_sheet.to_excel(writer, sheet_name="Listagem", index=False)

        writer.save()
        logger.info("Xlsx criado com sucesso")

        logger.info("Criando o arquivos HTML")
        listagem_sheet["Código do Produto"] = listagem_sheet[
            "Código do Produto"
        ].astype(int)
        del listagem_sheet["Valor Unitário"]
        del listagem_sheet["Valor Total"]

        for i, dataframe_group in listagem_sheet.groupby("Número do Lote"):
            lot_number = dataframe_group["Número do Lote"].iloc[0]

            filepath = os.path.join("output", "html", f"{lot_number}.html")
            html_file = open(filepath, "w", newline="", encoding="utf-8")

            html_content = dataframe_group.to_html(index=False, na_rep="")
            html_content = (
                html_utils.get_header() + html_content + html_utils.get_footer()
            )
            html_file.write(html_content)
            html_file.close()

        logger.info("Arquivos HTML criados com sucesso")


if __name__ == "__main__":
    logger.info("Iniciando a conversão")
    petrobras_converter = PetrobrasConverter(
        ".",
        ["input"],
        [
            "output",
            os.path.join("output", "xlsx"),
            os.path.join("output", "html"),
        ],
    )

    try:
        petrobras_converter.execute()
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado no processamento da planilha")
        logger.exception(error)

    input_folder = os.path.join("input", "images")
    output_folder = os.path.join("output", "images")

    try:
        img_handler = ImageHandler(input_folder, output_folder)

        img_handler.move_images(
            lambda img_name: img_name.find("Lote") != -1,
            lambda img_name: re.search(r"\d+", img_name)[0],
        )
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado ao mover as imagens")
        logger.exception(error)

    done = str(input("Pressione ENTER para encerrar..."))
