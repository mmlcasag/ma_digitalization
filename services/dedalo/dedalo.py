import os
import pandas
from services.base.spreadsheet_converter import SpreadsheetConverter
from services.base.logger import Logger
from services.base.images_handler import ImageHandler
import re

logger = Logger.__call__().get_logger()


class DedaloConverter(SpreadsheetConverter):
    def process_file(self, file):
        sheet = pandas.read_excel(file)
        sheet["DESCRIÇÃO"] = sheet["DESCRIÇÃO"].apply(
            lambda x: self.remove_prefix(x, "Lote com").strip().capitalize()
        )

        if "INFORMAÇÕES COMPLEMENTARES" in sheet.columns:
            sheet["INFORMAÇÕES COMPLEMENTARES"] = sheet[
                "INFORMAÇÕES COMPLEMENTARES"
            ].fillna("")

            sheet[
                "INFORMAÇÕES COMPLEMENTARES"
            ] = "<br><br>#PRODUCT_DESCRIPTION<br><br>" + sheet[
                "INFORMAÇÕES COMPLEMENTARES"
            ].astype(
                str
            )

            sheet["INFORMAÇÕES COMPLEMENTARES"] = sheet.apply(
                lambda x: x["INFORMAÇÕES COMPLEMENTARES"].replace("\n", "<br>"),
                axis=1,
            )

            sheet["INFORMAÇÕES COMPLEMENTARES"] = sheet.apply(
                lambda x: x["INFORMAÇÕES COMPLEMENTARES"].replace(
                    "#PRODUCT_DESCRIPTION", x["DESCRIÇÃO"]
                ),
                axis=1,
            )

        data = sheet.to_dict("list")
        data_to_output = dict()
        data_to_output["Nº do lote"] = data["LOTE"]
        data_to_output["Status"] = "novo"
        data_to_output["Lote Ref. / Ativo-Frota"] = ""
        data_to_output["Nome do Lote (SEMPRE MAIUSCULA)"] = sheet[
            "DESCRIÇÃO"
        ].str.upper()
        data_to_output["Descrição"] = (
            data["INFORMAÇÕES COMPLEMENTARES"]
            if "INFORMAÇÕES COMPLEMENTARES" in data
            else ""
        )
        data_to_output["VI"] = data["BASE"]
        data_to_output["VMV"] = ""
        data_to_output["VER"] = ""
        data_to_output["Incremento"] = data["INCREMENTO"]
        data_to_output["Valor de Referência do Vendedor (Contábil)"] = ""
        data_to_output["Comitente"] = "Dédalo Leilões"
        data_to_output["Município"] = "São Paulo"
        data_to_output["UF"] = "SP"
        data_to_output["Assessor"] = "Vendedor"
        data_to_output["Pendências"] = ""
        data_to_output["Restrições"] = ""
        data_to_output["Débitos (Total)"] = ""
        data_to_output["Unid. Métrica"] = ""
        data_to_output["Fator Multiplicativo"] = "1"
        data_to_output["Alteração/Adicionado"] = ""
        data_to_output["Descrição HTML"] = ""

        file_name = os.path.basename(file)
        filepath = os.path.join("output", "xlsx", file_name)
        logger.info(f"Criando arquivo de saída: {filepath}")
        writer = pandas.ExcelWriter(filepath, engine="xlsxwriter")

        df = pandas.DataFrame(data_to_output)
        df["VI"] = pandas.to_numeric(df["VI"])
        df.to_excel(writer, sheet_name="Colunada", index=False)
        writer.save()
        logger.info(f"Arquivo processado com sucesso: {filepath}")


if __name__ == "__main__":
    logger.info("Iniciando a conversão")
    dedaloConverter = DedaloConverter(
        ".",
        ["input"],
        [
            "output",
            os.path.join("output", "xlsx"),
        ],
    )
    try:
        dedaloConverter.execute()
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado no processamento da planilha")
        logger.exception(error)

    logger.info("Processo de conversão da planilha finalizado com sucesso.")

    input_folder = os.path.join("input", "images")
    output_folder = os.path.join("output", "images")

    try:
        logger.info("Iniciando processo de separação das imagens")
        img_handler = ImageHandler(input_folder, output_folder)
        img_handler.move_images(
            lambda img_name: re.search(r"\d+", img_name),
            lambda img_name: re.search(r"\d+", img_name)[0].lstrip("0"),
        )

        logger.info("Finalizando processo de separação das imagens")
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado ao mover as imagens")
        logger.exception(error)

    done = str(input("Pressione ENTER para encerrar..."))
