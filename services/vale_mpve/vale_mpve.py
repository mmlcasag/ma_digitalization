import os
import re
import pandas
from services.base.spreadsheet_converter import SpreadsheetConverter
from services.base.logger import Logger
import utils.ma as ma_utils
import utils.excel as excel_utils

logger = Logger.__call__().get_logger()


class CONST:
    SUBCATEGORY = "Sub-categoria:"
    BRAND = "Marca:"
    MODEL = "Modelo:"
    YEAR = "Ano: "
    SERIAL_NUMBER = "Serial / Chassi: "
    KMS = "KMs / Hrs trabalhadas: "
    TAG = "TAG/CP: "
    STARTED_WITH_1000 = "Número imobilizado SAP\n(começado 1000) "
    STARTED_WITH_8000 = "Número disponível p/ venda \n(começado 8000) "
    ENGINE = "Motor: "
    TRANSMISSION = "Transmissão: "
    BUCKET_BLADE = "Caçamba(pá)/lâmina: "
    ADDITIONAL_INFO = (
        "Dados adicionais (Mencionar principais informações sobre condições do lote)"
    )
    EVALUATION_VALUE = "Valor de avaliação: "
    LOCATION = "Cidade / Estado: \n(onde se encontra o lote fisicamente)"
    LOT = "Lote: "
    CMD = "CMD / Mina: "
    REQUESTER = "Solicitante: "
    CATEGORY = "Categoria: "
    PLATE = "Placa: "


class TEMPLATES:
    SHORT_DESCRIPTION_DEFAULT = (
        "{{SUBCATEGORY}} {{BRAND}} {{MODEL}}, ANO: {{YEAR}}, SÉRIE: {{SERIAL_NUMBER}}"
    )
    DESCRIPTION_DEFAULT = "<br><br>{{SUBCATEGORY}}<br>Marca: {{BRAND}}<br>Modelo: {{MODEL}}<br>Ano: {{YEAR}}<br>Série: {{SERIAL_NUMBER}}<br>Horímetro: {{KMS}}<br><br>Observações: TAG: {{TAG}}<br>IMOBILIZADO: {{STARTED_WITH_8000}}/{{STARTED_WITH_1000}}<br>Motor: {{ENGINE}}<br>Transmissão: {{TRANSMISSION}}<br>Caçamba/Lâmina: {{BUCKET_BLADE}}<br><br><br>{{ADDITIONAL_INFO}}."
    SHORT_DESCRIPTION_VEHICLE = (
        "{{BRAND}} {{MODEL}}, {{YEAR}}, PL.: {{PLATE}}, CH.: {{SERIAL_NUMBER}}"
    )
    DESCRIPTION_VEHICLE = "<br><br>Marca: {{BRAND}}<br>Modelo: {{MODEL}}<br>Ano: {{YEAR}}<br>Placa: {{PLATE}}<br>Chassi: {{SERIAL_NUMBER}}<br>Km: {{KMS}}<br><br>Observações: Motor: {{ENGINE}}<br>Transmissão: {{TRANSMISSION}}<br><br><br>{{ADDITIONAL_INFO}}."
    SHORT_DESCRIPTION_TRUCK = "{{SUBCATEGORY}} {{BRAND}} {{MODEL}}, {{YEAR}}, PL.: {{PLATE}} (PA), CH.: {{SERIAL_NUMBER}}"
    DESCRIPTION_TRUCK = "<br><br>{{SUBCATEGORY}}<br>Marca: {{BRAND}}<br>Modelo: {{MODEL}}<br>Ano: {{YEAR}}<br>Placa: {{PLATE}} (PA)<br>Chassi: {{SERIAL_NUMBER}}<br>Km: {{KMS}}<br><br>Observações: TAG: {{TAG}}<br>IMOBILIZADO: {{STARTED_WITH_8000}}/{{STARTED_WITH_1000}}<br>Motor: {{ENGINE}}<br>Transmissão: {{TRANSMISSION}}<br>Caçamba/Lâmina: {{BUCKET_BLADE}}<br><br><br>{{ADDITIONAL_INFO}}"
    SHORT_DESCRIPTION_FORK_LIFT = (
        "{{SUBCATEGORY}} {{BRAND}} {{MODEL}}, ANO: {{YEAR}}, SÉRIE: {{SERIAL_NUMBER}}"
    )
    DESCRIPTION_FORK_LIFT = "<br><br>{{SUBCATEGORY}}<br>Marca: {{BRAND}}<br>Modelo: {{MODEL}}<br>Ano: {{YEAR}}<br>Série: {{SERIAL_NUMBER}}<br>Horímetro: {{KMS}}<br><br>Observações: TAG: {{TAG}}<br>IMOBILIZADO: {{STARTED_WITH_8000}}/{{STARTED_WITH_1000}}<br>Motor: {{ENGINE}}<br>Transmissão: {{TRANSMISSION}}<br><br><br>{{ADDITIONAL_INFO}}"


def handle_sheet_row(row, prefix="", empty_value="", as_type=str):
    return prefix + row.fillna(empty_value).astype(as_type).values[0]


def generate_description(template, items):
    result = template
    for item in items:
        result = result.replace(
            "{{" + item["key"] + "}}", handle_sheet_row(item["value"])
        )

    result = re.sub(r"\{{([^}]*)}}", "--", result)
    return result


class ValeMPVEConverter(SpreadsheetConverter):
    def execute(self):
        self.create_input_folder()
        self.create_output_folder()

        if os.path.isfile(self._output_xlsx_file):
            os.remove(self._output_xlsx_file)

        list_files = self.get_file_list()
        logger.info(f"Encontrados {len(list_files)} arquivo(s) na pasta de entrada")
        count = 0
        for file in list_files:
            try:
                count += 1
                self.process_file(file)
                logger.info(
                    f"Processamento da planilha {count} de {len(list_files)} finalizado"
                )
            except Exception as error:
                logger.error(f"Erro no processamento do arquivo {file}")
                logger.exception(error)

    def process_file(self, file):
        engine = None
        if file.endswith(".xlsb"):
            engine = "pyxlsb"

        sheet_row_01 = pandas.read_excel(
            file, header=7, usecols="C:I", nrows=1, engine=engine
        )
        sheet_row_02 = pandas.read_excel(
            file, header=10, usecols="C:I", nrows=1, engine=engine
        )
        sheet_row_03 = pandas.read_excel(
            file, header=13, usecols="C:I", nrows=1, engine=engine
        )
        sheet_row_04 = pandas.read_excel(
            file, header=17, usecols="C:I", nrows=1, engine=engine
        )
        sheet_row_05 = pandas.read_excel(
            file, header=20, usecols="C:I", nrows=1, engine=engine
        )

        lot_name = generate_description(
            TEMPLATES.SHORT_DESCRIPTION_DEFAULT,
            [
                {"key": "SUBCATEGORY", "value": sheet_row_01[CONST.SUBCATEGORY]},
                {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                {"key": "SERIAL_NUMBER", "value": sheet_row_02[CONST.SERIAL_NUMBER]},
            ],
        )

        description = generate_description(
            TEMPLATES.DESCRIPTION_DEFAULT,
            [
                {"key": "SUBCATEGORY", "value": sheet_row_01[CONST.SUBCATEGORY]},
                {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                {"key": "SERIAL_NUMBER", "value": sheet_row_02[CONST.SERIAL_NUMBER]},
                {"key": "KMS", "value": sheet_row_03[CONST.KMS]},
                {"key": "TAG", "value": sheet_row_02[CONST.TAG]},
                {
                    "key": "STARTED_WITH_8000",
                    "value": sheet_row_03[CONST.STARTED_WITH_8000],
                },
                {
                    "key": "STARTED_WITH_1000",
                    "value": sheet_row_03[CONST.STARTED_WITH_1000],
                },
                {"key": "ENGINE", "value": sheet_row_04[CONST.ENGINE]},
                {"key": "TRANSMISSION", "value": sheet_row_04[CONST.TRANSMISSION]},
                {"key": "BUCKET_BLADE", "value": sheet_row_04[CONST.BUCKET_BLADE]},
                {
                    "key": "ADDITIONAL_INFO",
                    "value": sheet_row_05[CONST.ADDITIONAL_INFO],
                },
            ],
        )

        if handle_sheet_row(sheet_row_01[CONST.SUBCATEGORY]) in [
            "Utilitário",
            "Caminhonete",
            "Ambulância",
        ]:
            lot_name = generate_description(
                TEMPLATES.SHORT_DESCRIPTION_VEHICLE,
                [
                    {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                    {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                    {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                    {"key": "PLATE", "value": sheet_row_02[CONST.PLATE]},
                    {
                        "key": "SERIAL_NUMBER",
                        "value": sheet_row_02[CONST.SERIAL_NUMBER],
                    },
                ],
            )
            description = generate_description(
                TEMPLATES.DESCRIPTION_VEHICLE,
                [
                    {"key": "PLATE", "value": sheet_row_02[CONST.PLATE]},
                    {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                    {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                    {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                    {
                        "key": "SERIAL_NUMBER",
                        "value": sheet_row_02[CONST.SERIAL_NUMBER],
                    },
                    {"key": "KMS", "value": sheet_row_03[CONST.KMS]},
                    {"key": "ENGINE", "value": sheet_row_04[CONST.ENGINE]},
                    {"key": "TRANSMISSION", "value": sheet_row_04[CONST.TRANSMISSION]},
                    {
                        "key": "ADDITIONAL_INFO",
                        "value": sheet_row_05[CONST.ADDITIONAL_INFO],
                    },
                ],
            )

        if re.search(
            "caminhão", handle_sheet_row(sheet_row_01[CONST.SUBCATEGORY]).lower()
        ):
            lot_name = generate_description(
                TEMPLATES.SHORT_DESCRIPTION_TRUCK,
                [
                    {"key": "SUBCATEGORY", "value": sheet_row_01[CONST.SUBCATEGORY]},
                    {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                    {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                    {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                    {"key": "PLATE", "value": sheet_row_02[CONST.PLATE]},
                    {
                        "key": "SERIAL_NUMBER",
                        "value": sheet_row_02[CONST.SERIAL_NUMBER],
                    },
                ],
            )
            description = generate_description(
                TEMPLATES.DESCRIPTION_TRUCK,
                [
                    {"key": "SUBCATEGORY", "value": sheet_row_01[CONST.SUBCATEGORY]},
                    {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                    {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                    {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                    {"key": "PLATE", "value": sheet_row_02[CONST.PLATE]},
                    {
                        "key": "SERIAL_NUMBER",
                        "value": sheet_row_02[CONST.SERIAL_NUMBER],
                    },
                    {"key": "KMS", "value": sheet_row_03[CONST.KMS]},
                    {"key": "TAG", "value": sheet_row_02[CONST.TAG]},
                    {
                        "key": "STARTED_WITH_8000",
                        "value": sheet_row_03[CONST.STARTED_WITH_8000],
                    },
                    {
                        "key": "STARTED_WITH_1000",
                        "value": sheet_row_03[CONST.STARTED_WITH_1000],
                    },
                    {"key": "ENGINE", "value": sheet_row_04[CONST.ENGINE]},
                    {"key": "TRANSMISSION", "value": sheet_row_04[CONST.TRANSMISSION]},
                    {"key": "BUCKET_BLADE", "value": sheet_row_04[CONST.BUCKET_BLADE]},
                    {
                        "key": "ADDITIONAL_INFO",
                        "value": sheet_row_05[CONST.ADDITIONAL_INFO],
                    },
                ],
            )

        if handle_sheet_row(sheet_row_01[CONST.SUBCATEGORY]).lower() == "empilhadeira":
            lot_name = generate_description(
                TEMPLATES.SHORT_DESCRIPTION_FORK_LIFT,
                [
                    {"key": "SUBCATEGORY", "value": sheet_row_01[CONST.SUBCATEGORY]},
                    {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                    {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                    {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                    {
                        "key": "SERIAL_NUMBER",
                        "value": sheet_row_02[CONST.SERIAL_NUMBER],
                    },
                ],
            )
            description = generate_description(
                TEMPLATES.DESCRIPTION_FORK_LIFT,
                [
                    {"key": "SUBCATEGORY", "value": sheet_row_01[CONST.SUBCATEGORY]},
                    {"key": "BRAND", "value": sheet_row_02[CONST.BRAND]},
                    {"key": "MODEL", "value": sheet_row_02[CONST.MODEL]},
                    {"key": "YEAR", "value": sheet_row_02[CONST.YEAR]},
                    {
                        "key": "SERIAL_NUMBER",
                        "value": sheet_row_02[CONST.SERIAL_NUMBER],
                    },
                    {"key": "KMS", "value": sheet_row_03[CONST.KMS]},
                    {"key": "TAG", "value": sheet_row_02[CONST.TAG]},
                    {
                        "key": "STARTED_WITH_8000",
                        "value": sheet_row_03[CONST.STARTED_WITH_8000],
                    },
                    {
                        "key": "STARTED_WITH_1000",
                        "value": sheet_row_03[CONST.STARTED_WITH_1000],
                    },
                    {"key": "ENGINE", "value": sheet_row_04[CONST.ENGINE]},
                    {"key": "TRANSMISSION", "value": sheet_row_04[CONST.TRANSMISSION]},
                    {
                        "key": "ADDITIONAL_INFO",
                        "value": sheet_row_05[CONST.ADDITIONAL_INFO],
                    },
                ],
            )

        vi = (
            round(float(handle_sheet_row(sheet_row_03[CONST.EVALUATION_VALUE])), 2)
            * 0.3
        )

        location = ma_utils.split_city_and_state(
            handle_sheet_row(sheet_row_01[CONST.LOCATION])
        )

        city = ""
        try:
            city = location[0]
        except Exception as error:
            logger.error(f"Erro {error} ao tentar buscar o município")

        state = ""
        try:
            state = location[1]
        except Exception as error:
            logger.error(f"Erro {error} ao tentar buscar o estado")

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
                "Valor de Referência do Vendedor (Contábil)": handle_sheet_row(
                    sheet_row_03[CONST.EVALUATION_VALUE], "", 0
                ),
                "Comitente": handle_sheet_row(sheet_row_01[CONST.CMD]),
                "Município": city,
                "UF": state,
                "Assessor": handle_sheet_row(
                    sheet_row_01[CONST.REQUESTER], "", "Vendedor"
                ),
                "Pendências": "",
                "Restrições": "",
                "Débitos (Total)": "",
                "Unid. Métrica": "",
                "Fator Multiplicativo": 1,
                "Alteração/Adicionado": "",
                "Descrição HTML": "",
                "Categoria": handle_sheet_row(sheet_row_01[CONST.CATEGORY]),
                "Subcategoria": handle_sheet_row(sheet_row_01[CONST.SUBCATEGORY]),
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

        excel_utils.extract_images(
            file,
            os.path.join(
                os.getcwd(),
                "output",
                "images",
                handle_sheet_row(sheet_row_01[CONST.LOT]),
            ),
        )

        if os.path.isfile(self._output_xlsx_file):
            append_data = pandas.read_excel(
                self._output_xlsx_file, sheet_name="Colunada"
            )
            df = pandas.concat([append_data, df])

        writer = pandas.ExcelWriter(self._output_xlsx_file, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Colunada", index=False)
        writer.close()


if __name__ == "__main__":
    try:
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
        valeMPVEConverter.execute()
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado no processamento da planilha")
        logger.exception(error)

    logger.info("Processo finalizado com sucesso.")
    done = str(input("Pressione ENTER para encerrar..."))
