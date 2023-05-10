import os

import pandas

import utils.excel as excel_utils
import utils.html as html_utils
import utils.ma as ma_utils
import utils.os as os_utils
from services.base.logger import Logger
from services.base.spreadsheet_converter import SpreadsheetConverter

logger = Logger.__call__().get_logger()


def handle_sheet_row(row, index=0, prefix="", empty_value="", as_type=str):
    if as_type == int:
        if row.fillna(empty_value).values[index]:
            return f"{prefix}{str(int(row.fillna(empty_value).values[index]))}"
        else:
            return ""
    else:
        return f"{prefix}{row.fillna(empty_value).astype(as_type).values[index]}"


def format_to_decimal(value):
    return "{:.2f}".format(float(value))


class CONST:
    ALERT = "ATENÇÃO!!!! AO INSERIR LINHAS, AJUSTAR AS FÓRMULAS DA PLANILHA"
    DESCRIPTION = "Descrição Completa\nInformar marca, modelo, ano, se está funcionando, se faltam peças ou qualquer outra informação relevante para o processo de venda"
    LOCATION = "Cidade / Estado\n(onde se encontra o lote fisicamente)"
    TOTAL_AMOUNT = "(FÓRMULA)\nValor total avaliação\n(= qte x PMU)"
    LOT = "Lote"
    CMD = "CMD"
    REQUESTER = "Solicitante"
    CATEGORY = "Categoria"
    SUBCATEGORY = "Sub-categoria\n(selecionar da lista abaixo)"
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

        location = ma_utils.split_city_and_state(
            handle_sheet_row(sheet_row_01[CONST.LOCATION])
        )
        total_amount = float(sheet_row_02[CONST.TOTAL_AMOUNT].dropna().tail(1))
        vi = float(total_amount) * 0.3

        total_items = sheet_row_02["Qte"].dropna()

        description = handle_sheet_row(
            sheet_row_02[CONST.STARTED_WITH_1000], 0, "Código do Produto: ", "", int
        )
        description += handle_sheet_row(
            sheet_row_02[CONST.STARTED_WITH_8000],
            0,
            "<br>Referência do Produto: ",
            "",
            int,
        )
        description += handle_sheet_row(
            sheet_row_02[CONST.DESCRIPTION], 0, "<br>Descrição do Produto: ", ""
        )
        description += handle_sheet_row(
            sheet_row_02[CONST.SUBCATEGORY], 0, "<br>Descrição do Grupo: ", ""
        )
        description += handle_sheet_row(
            sheet_row_02[CONST.QTD], 0, "<br>Quantidade: ", ""
        )
        description += handle_sheet_row(sheet_row_02[CONST.UN], 0, "<br>Unidade: ", "")
        description += handle_sheet_row(
            sheet_row_01[CONST.LOT], 0, "<br>Lote de Referência: ", ""
        )

        html_description = ""
        lot_name = handle_sheet_row(sheet_row_02[CONST.DESCRIPTION])

        if len(total_items) > 1:
            lot_name = ma_utils.generate_description_from_array(
                sheet_row_02[CONST.DESCRIPTION].dropna().values
            )
            description = "Para maiores informações, clique em ANEXOS"
            html_description = "Em arquivo separado"

        subcategories = list(set(sheet_row_02[CONST.SUBCATEGORY].dropna().values))

        subcategory = ""

        if len(subcategories) == 1:
            subcategory = subcategories[0]

        df = pandas.DataFrame(
            {
                "Nº do lote": handle_sheet_row(sheet_row_01[CONST.LOT]),
                "Status": "novo",
                "Lote Ref. / Ativo-Frota": handle_sheet_row(sheet_row_01[CONST.LOT]),
                "Nome do Lote (SEMPRE MAIUSCULA)": lot_name.strip().upper(),
                "Descrição": description,
                "VI": vi,
                "VMV": "",
                "VER": "",
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
                "Descrição HTML": html_description,
                "Categoria": handle_sheet_row(sheet_row_01[CONST.CATEGORY]),
                "Subcategoria": subcategory,
            },
            index=[0],
        )

        df["VI"] = df["VI"].apply(lambda x: excel_utils.convert_to_currency(x))
        df["Incremento"] = df["Incremento"].apply(
            lambda x: excel_utils.convert_to_currency(x)
        )
        df["Valor de Referência do Vendedor (Contábil)"] = df[
            "Valor de Referência do Vendedor (Contábil)"
        ].apply(lambda x: excel_utils.convert_to_currency(x))

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

        for index, item in enumerate(total_items):
            append_data = {
                "Código do Produto": handle_sheet_row(
                    sheet_row_02[CONST.STARTED_WITH_1000], index, "", "", int
                ),
                "Referência do Produto": handle_sheet_row(
                    sheet_row_02[CONST.STARTED_WITH_8000], index, "", "", int
                ),
                "Descrição do Produto": handle_sheet_row(
                    sheet_row_02[CONST.DESCRIPTION], index
                ),
                "Descrição do Grupo": handle_sheet_row(
                    sheet_row_02[CONST.SUBCATEGORY], index
                ),
                "Quantidade": format_to_decimal(
                    handle_sheet_row(sheet_row_02[CONST.QTD], index)
                ),
                "Unidade": handle_sheet_row(sheet_row_02[CONST.UN], index),
                "Valor Unitário": excel_utils.convert_to_currency(
                    format_to_decimal(
                        handle_sheet_row(sheet_row_02[CONST.UNIT_PRICE], index)
                    )
                ),
                "Valor Total": excel_utils.convert_to_currency(
                    format_to_decimal(
                        handle_sheet_row(sheet_row_02[CONST.TOTAL_AMOUNT], index)
                    )
                ),
                "Peso Estimado": format_to_decimal(
                    handle_sheet_row(sheet_row_02[CONST.WEIGHT], index)
                ),
                "Lote de Referência": handle_sheet_row(sheet_row_01[CONST.LOT]),
            }
            temp_list.append(append_data)

            if len(total_items) > 1:
                logger.info("Carregando um dataset para geração do arquivo HTML")
                df_html = pandas.DataFrame(temp_list, columns=df_columns)

                del df_html["Valor Unitário"]
                del df_html["Valor Total"]
                del df_html["Peso Estimado"]

                df_html["Quantidade"] = df_html["Quantidade"].apply(
                    lambda x: excel_utils.convert_to_numeric(x)
                )

                logger.info("Gerando código HTML a partir dos dados do dataset")
                html_content = df_html.to_html(index=False, na_rep="")

                logger.info("Concatenando o cabeçalho e o rodapé do arquivo HTML")
                html_content = (
                    html_utils.get_header() + html_content + html_utils.get_footer()
                )

                html_file = open(
                    os.path.join(
                        "output", "html", os_utils.get_file_name(file_name) + ".html"
                    ),
                    "w",
                    newline="",
                    encoding="utf-8",
                )

                html_file.write(html_content)
                html_file.close()

        df_list = pandas.DataFrame(temp_list, columns=df_columns)
        df_list["Quantidade"] = df_list["Quantidade"].apply(
            lambda x: excel_utils.convert_to_numeric(x)
        )

        df_list["Peso Estimado"] = df_list["Peso Estimado"].apply(
            lambda x: excel_utils.convert_to_numeric(x)
        )

        logger.info("Rodando o processo de extração de imagens")
        excel_utils.extract_images(
            file,
            os.path.join(
                os.getcwd(),
                "output",
                "images",
                handle_sheet_row(sheet_row_01[CONST.LOT]),
            ),
        )
        logger.info("Processo de extração de imagens finalizado")

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

        df.sort_values("Nº do lote", ascending=True).to_excel(
            writer, sheet_name="Colunada", index=False
        )

        df_list.sort_values(
            ["Lote de Referência", "Código do Produto"], ascending=True
        ).to_excel(writer, sheet_name="Listagem", index=False)

        writer.close()


if __name__ == "__main__":
    try:
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
        valeMEConverter.execute()
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado no processamento da planilha")
        logger.exception(error)

    logger.info("Processo finalizado com sucesso.")
    done = str(input("Pressione ENTER para encerrar..."))
