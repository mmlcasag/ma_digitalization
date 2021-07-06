import os
import pandas
from services.base.spreadsheet_converter import SpreadsheetConverter
from services.base.logger import Logger
import utils.os as os_utils
import utils.ma as ma_utils
import utils.excel as excel_utils
import utils.html as html_utils

logger = Logger.__call__().get_logger()


def handle_sheet_row(row, index=0, prefix="", empty_value="", as_type=str):
    return prefix + row.fillna(empty_value).astype(as_type).values[index]


class CONST:
    ALERT = "ATENÇÃO!!!! AO INSERIR LINHAS, AJUSTAR AS FÓRMULAS DA PLANILHA"
    DESCRIPTION = "Descrição Completa\nInformar marca, modelo, ano, se está funcionando, se faltam peças ou qualquer outra informação relevante para o processo de venda"
    LOCATION = "Cidade / Estado\n(onde se encontra o lote fisicamente)"
    TOTAL_AMOUNT = "(FÓRMULA)\nValor total avaliação\n(= qte x PMU)"
    LOT = "Lote"
    CMD = "CMD"
    REQUESTER = "Solicitante"
    CATEGORY = "Categoria"
    STARTED_WITH_1000 = "Imobilizado\n(começado c/ 1000)"
    STARTED_WITH_8000 = "Disponível para venda\n(começado c/ 8000)"
    QTD = "Qte"
    UN = "Un medida"
    UNIT_PRICE = "Preço unitário\nde avaliação"
    WEIGHT = "Peso estimado em Kg\n(digitar somente número)"


class ValeMEConverter(SpreadsheetConverter):
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
        file_name = os.path.basename(file)

        sheet_row_01 = pandas.read_excel(file, header=6, usecols="C:O", nrows=1)

        sheet_row_02 = pandas.read_excel(file, header=9, usecols="C:O")

        lot_name = ma_utils.generate_description_from_array(
            sheet_row_02[CONST.DESCRIPTION].dropna().values
        )

        location = ma_utils.split_city_and_state(
            handle_sheet_row(sheet_row_01[CONST.LOCATION])
        )
        total_amount = int(sheet_row_02[CONST.TOTAL_AMOUNT].dropna().tail(1))
        vi = round(float(total_amount), 2) * 0.3

        total_items = sheet_row_02["Qte"].dropna()

        description = ""
        if len(total_items) > 1:
            description = "Para maiores informações, clique em ANEXOS"

        df = pandas.DataFrame(
            {
                "Nº do lote": handle_sheet_row(sheet_row_01[CONST.LOT]),
                "Status": "novo",
                "Lote Ref. / Ativo-Frota": handle_sheet_row(sheet_row_01[CONST.LOT]),
                "Nome do Lote (SEMPRE MAIUSCULA)": lot_name.strip().upper(),
                "Descrição": description,
                "VI": vi,
                "VMV": 0,
                "VER": 0,
                "Incremento": ma_utils.get_closest_value(
                    ma_utils.get_available_increments(), vi / 10
                ),
                "Valor de Referência do Vendedor (Contábil)": total_amount,
                "Comitente": handle_sheet_row(sheet_row_01[CONST.CMD]),
                "Município": location[0],
                "UF": location[1],
                "Assessor": handle_sheet_row(
                    sheet_row_01[CONST.REQUESTER], 0, "", "Vendedor"
                ),
                "Pendências": "",
                "Restrições": "",
                "Débitos (Total)": "",
                "Unid. Métrica": "",
                "Fator Multiplicativo": 1,
                "Alteração/Adicionado": "",
                "Descrição HTML": "",
                "Categoria": handle_sheet_row(sheet_row_01[CONST.CATEGORY]),
            },
            index=[0],
        )

        temp_list = []
        df_columns = [
            "Código do Produto",
            "Referência do Produto",
            "Descrição do Produto",
            "Descrição do Grupo",
            "Quantidade",
            "Unidade",
            "Valor Unitário",
            "Valor Total",
            "Peso Estimado",
            "Lote de Referência",
        ]

        if len(total_items) > 1:
            for index, item in enumerate(total_items):
                append_data = {
                    "Código do Produto": handle_sheet_row(
                        sheet_row_02[CONST.STARTED_WITH_1000], index
                    ),
                    "Referência do Produto": handle_sheet_row(
                        sheet_row_02[CONST.STARTED_WITH_8000], index
                    ),
                    "Descrição do Produto": handle_sheet_row(
                        sheet_row_02[CONST.DESCRIPTION], index
                    ),
                    "Descrição do Grupo": lot_name,
                    "Quantidade": handle_sheet_row(sheet_row_02[CONST.QTD], index),
                    "Unidade": handle_sheet_row(sheet_row_02[CONST.UN], index),
                    "Valor Unitário": handle_sheet_row(
                        sheet_row_02[CONST.UNIT_PRICE], index
                    ),
                    "Valor Total": handle_sheet_row(
                        sheet_row_02[CONST.TOTAL_AMOUNT], index
                    ),
                    "Peso Estimado": handle_sheet_row(
                        sheet_row_02[CONST.WEIGHT], index
                    ),
                    "Lote de Referência": handle_sheet_row(sheet_row_01[CONST.LOT]),
                }
                temp_list.append(append_data)

            logger.info("Carregando um dataset para geração do arquivo HTML")
            df_html = pandas.DataFrame(temp_list, columns=df_columns)

            logger.info("Gerando código HTML a partir dos dados do dataset")
            html_content = df_html.to_html(index=False, na_rep="")

            logger.info("Concatenando o cabeçalho e o rodapé do arquivo HTML")
            html_content = (
                html_utils.get_header() + html_content + html_utils.get_footer()
            )

            html_file = open(
                os.path.join("output", "html", file_name + ".html"),
                "w",
                newline="",
                encoding="utf-8",
            )

            html_file.write(html_content)
            html_file.close()

        df_list = pandas.DataFrame(temp_list, columns=df_columns)

        excel_utils.extract_images_from_xlsx(
            file,
            os.path.join("output", "images", handle_sheet_row(sheet_row_01[CONST.LOT])),
        )

        if os.path.isfile(self._output_xlsx_file):
            append_data = pandas.read_excel(
                self._output_xlsx_file, sheet_name="Colunada"
            )
            df = pandas.concat([append_data, df])
            append_list = pandas.read_excel(
                self._output_xlsx_file, sheet_name="Listagem"
            )
            df_list = pandas.concat([append_list, df_list])

        writer = pandas.ExcelWriter(self._output_xlsx_file, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Colunada", index=False)
        df_list.to_excel(writer, sheet_name="Listagem", index=False)

        writer.save()


if __name__ == "__main__":
    logger.info("Iniciando a conversão")
    valeMEConverter = ValeMEConverter(
        ".",
        ["input"],
        [
            "output",
            os.path.join("output", "xlsx"),
            os.path.join("output", "html"),
        ],
        os.path.join("output", "xlsx", "resulting_spreadsheet.xlsx"),
    )
    try:
        valeMEConverter.execute()
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
