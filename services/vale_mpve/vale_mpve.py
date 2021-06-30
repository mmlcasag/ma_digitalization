import os
import pandas
from services.base.spreadsheet_converter import SpreadsheetConverter
from services.base.logger import Logger
import utils.os as os_utils
import utils.ma as ma_utils
import utils.excel as excel_utils

logger = Logger.__call__().get_logger()


def handle_sheet_row(row, prefix="", empty_value="", as_type=str):
    return prefix + row.fillna(empty_value).astype(as_type).values[0]


class ValeMPVEConverter(SpreadsheetConverter):
    def execute(self):
        self.create_input_folder()
        self.create_output_folder()

        if os.path.isfile(self._output_xlsx_file):
            os.remove(self._output_xlsx_file)

        list_files = self.get_file_list()
        logger.info(f"Encontrados {len(list_files)} arquivo(s) na pasta de entrada")
        count = 1
        for file in list_files:
            try:
                self.process_file(file)
                logger.info(
                    f"Processamento da planilha {count} de {len(list_files)} finalizado"
                )
                count += 1
            except Exception as error:
                logger.error(f"Erro no processamento do arquivo {file}")
                logger.exception(error)

    def process_file(self, file):

        sheet_row_01 = pandas.read_excel(
            file, header=7, usecols="C:I", nrows=1, engine="pyxlsb"
        )
        sheet_row_02 = pandas.read_excel(
            file, header=10, usecols="C:I", nrows=1, engine="pyxlsb"
        )
        sheet_row_03 = pandas.read_excel(
            file, header=13, usecols="C:I", nrows=1, engine="pyxlsb"
        )
        sheet_row_04 = pandas.read_excel(
            file, header=17, usecols="C:I", nrows=1, engine="pyxlsb"
        )
        sheet_row_05 = pandas.read_excel(
            file, header=20, usecols="C:I", nrows=1, engine="pyxlsb"
        )

        lot_name = handle_sheet_row(sheet_row_01["Sub-categoria:"])
        lot_name += handle_sheet_row(sheet_row_02["Marca:"], " ")
        lot_name += handle_sheet_row(sheet_row_02["Modelo:"], " ")
        lot_name += handle_sheet_row(sheet_row_02["Ano: "], ", ANO: ")
        lot_name += handle_sheet_row(sheet_row_02["Serial / Chassi: "], ", SÉRIE: ")

        description = handle_sheet_row(sheet_row_01["Sub-categoria:"], "<br><br>")
        description += handle_sheet_row(sheet_row_02["Marca:"], "<br>Marca: ")
        description += handle_sheet_row(sheet_row_02["Modelo:"], "<br>Modelo: ")
        description += handle_sheet_row(sheet_row_02["Ano: "], "<br>Ano: ")
        description += handle_sheet_row(
            sheet_row_02["Serial / Chassi: "], "<br>Série: "
        )
        description += handle_sheet_row(
            sheet_row_03["KMs / Hrs trabalhadas: "], "<br>Horímetro: "
        )
        description += handle_sheet_row(
            sheet_row_02["TAG/CP: "], "<br><br>Observações: TAG: "
        )
        description += handle_sheet_row(
            sheet_row_03["Número disponível p/ venda \n(começado 8000) "],
            "<br>IMOBILIZADO: ",
        )
        description += handle_sheet_row(
            sheet_row_03["Número imobilizado SAP\n(começado 1000) "], "/"
        )
        description += handle_sheet_row(sheet_row_04["Motor: "], "<br>Motor: ")
        description += handle_sheet_row(
            sheet_row_04["Transmissão: "], "<br>Transmissão: "
        )
        description += handle_sheet_row(
            sheet_row_04["Caçamba(pá)/lâmina: "], "<br>Caçamba/Lâmina: "
        )
        description += "<br><br><br>"
        description += handle_sheet_row(
            sheet_row_05[
                "Dados adicionais (Mencionar principais informações sobre condições do lote)"
            ]
        )

        vi = (
            round(float(handle_sheet_row(sheet_row_03["Valor de avaliação: "])), 2)
            * 0.3
        )
        location = ma_utils.split_city_and_state(
            handle_sheet_row(
                sheet_row_01["Cidade / Estado: \n(onde se encontra o lote fisicamente)"]
            )
        )

        df = pandas.DataFrame(
            {
                "Nº do lote": handle_sheet_row(sheet_row_01["Lote: "]),
                "Status": "novo",
                "Lote Ref. / Ativo-Frota": handle_sheet_row(sheet_row_01["Lote: "]),
                "Nome do Lote (SEMPRE MAIUSCULA)": lot_name.strip().upper(),
                "Descrição": description,
                "VI": vi,
                "VMV": 0,
                "VER": 0,
                "Incremento": ma_utils.get_closest_value(
                    ma_utils.get_available_increments(), vi / 10
                ),
                "Valor de Referência do Vendedor (Contábil)": handle_sheet_row(
                    sheet_row_03["Valor de avaliação: "], "", 0
                ),
                "Comitente": handle_sheet_row(sheet_row_01["CMD / Mina: "]),
                "Município": location[0],
                "UF": location[1],
                "Assessor": handle_sheet_row(
                    sheet_row_01["Solicitante: "], "", "Vendedor"
                ),
                "Pendências": "",
                "Restrições": "",
                "Débitos (Total)": "",
                "Unid. Métrica": "",
                "Fator Multiplicativo": 1,
                "Alteração/Adicionado": "",
                "Descrição HTML": "",
                "Categoria": handle_sheet_row(sheet_row_01["Categoria: "]),
                "Subcategoria": handle_sheet_row(sheet_row_01["Sub-categoria:"]),
            },
            index=[0],
        )

        excel_utils.extract_images_from_xlsx(
            file,
            os.path.join("output", "images", handle_sheet_row(sheet_row_01["Lote: "])),
        )

        if os.path.isfile(self._output_xlsx_file):
            append_data = pandas.read_excel(
                self._output_xlsx_file, sheet_name="Colunada"
            )
            df = pandas.concat([append_data, df])

        writer = pandas.ExcelWriter(self._output_xlsx_file, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Colunada", index=False)
        writer.save()


if __name__ == "__main__":
    logger.info("Iniciando a conversão")
    valeMPVEConverter = ValeMPVEConverter(
        ".",
        ["input"],
        [
            "output",
            os.path.join("output", "xlsx"),
        ],
        os.path.join("output", "xlsx", "resulting_spreadsheet.xlsx"),
    )
    try:
        valeMPVEConverter.execute()
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado no processamento da planilha")
        logger.exception(error)

    logger.info("Processo de conversão da planilha finalizado com sucesso.")

    input_folder = os.path.join("input", "images")
    output_folder = os.path.join("output", "images")

    try:
        logger.info("Iniciando processo de separação das imagens")
        os_utils.move_files_by_regex_name(input_folder, output_folder, r"\d+")
        logger.info("Finalizando processo de separação das imagens")
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado ao mover as imagens")
        logger.exception(error)

    done = str(input("Pressione ENTER para encerrar..."))
