import os

import pandas
import requests

from services.base.logger import Logger
from services.base.spreadsheet_converter import SpreadsheetConverter

logger = Logger.__call__().get_logger()


class CONST:
    PLATE = "Placa"
    SERIAL_NUMBER = "Chassi"
    FIPE = "Consultar Tabela Fipe?"


class RGAutomovelConverter(SpreadsheetConverter):
    def calculate_debts(self, values):
        total = 0
        for value in values:
            total += float(value.replace(".", "").replace(",", "."))

        return total

    def get_vehicle_data(self, plate, serial_number, check_fipe):

        base_url = "http://ws.rgdoautomovel.com.br"
        request_params = {
            "pstrFormat": "json",
            "pstrCliente": "maisativo.sbid",
            "pstrLogin": "maisativo.sbid",
            "pstrSenha": "sbid153",
        }

        if plate != "null":
            request_params["pstrPlaca"] = plate

        if serial_number != "null":
            request_params["pstrChassi"] = serial_number

        logger.info("Aguarde, buscando informaçōes no RG Automovel...")

        bin_estadual_response = requests.get(
            f"{base_url}/binestadual", params=request_params
        )
        precificador_json = {
            "struct_RespostaRst": {"Resposta": {"struct_ResultadoPrecificador": False}}
        }
        if check_fipe:
            precificador_response = requests.get(
                f"{base_url}/precificador", params=request_params
            )
            precificador_json = precificador_response.json()

        bin_estadual_json = bin_estadual_response.json()

        return {
            "bin_estadual": bin_estadual_json["struct_RespostaRst"]["Resposta"],
            "precificador": precificador_json["struct_RespostaRst"]["Resposta"][
                "struct_ResultadoPrecificador"
            ],
        }

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
        data = pandas.read_excel(file)

        temp_list = []
        df_columns = [
            "Lote Ref. / Ativo-Frota",
            "Tabela Molicar",
            "Tabela Fipe",
            "Proprietário/CNPJ (Proprietário do documento)",
            "Restrições",
            "Débitos (Total)",
            "Tipo",
            "Marca (SEMPRE MAIUSCULA)",
            "Modelo (SEMPRE MAIUSCULA)",
            "Ano Fab/Modelo",
            "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))",
            "Chassi (SEMPRE MAIUSCULA)",
            "Renavam",
            "Cor",
            "Combustível",
            "Cilindrada",
            "Situação Veículo",
            "Tipo de Remarcação do Chassi",
            "Espécie",
            "Carroceria",
            "Potência",
            "Município",
            "Nº Motor",
            "Procedência do Veículo",
            "Capacidade de Carga",
            "Capacidade de Passageiros",
            "Nº Carroceria",
            "Nº Caixa de Câmbio",
            "Nº Eixos",
            "Terceiro Eixo",
            "Eixo Traseiro Diferencial",
            "Montagem",
            "CMT",
            "PBT",
        ]

        for idx, v in enumerate(data[CONST.PLATE]):
            plate = data[CONST.PLATE].fillna("null").values[idx]
            serial_number = data[CONST.SERIAL_NUMBER].fillna("null").values[idx]
            fipe = data[CONST.FIPE].fillna("null").values[idx].lower()
            check_fipe = False
            fipe_val = ""

            if fipe == "s" or fipe == " sim":
                check_fipe = True

            if plate != "null" or serial_number != "null":
                response = self.get_vehicle_data(plate, serial_number, check_fipe)

                if check_fipe:
                    fipe_val = response["precificador"]["PrecoFipe"]

                restricoes = ""

                restricao_1 = response["bin_estadual"]["Restricao1"]
                restricao_2 = response["bin_estadual"]["Restricao2"]
                restricao_3 = response["bin_estadual"]["Restricao3"]
                restricao_4 = response["bin_estadual"]["Restricao4"]
                restricao_5 = response["bin_estadual"]["Restricao5"]
                restricao_6 = response["bin_estadual"]["Restricao6"]
                restricao_7 = response["bin_estadual"]["Restricao7"]
                restricao_8 = response["bin_estadual"]["Restricao8"]
                restricao_9 = response["bin_estadual"]["Restricao9"]
                restricao_10 = response["bin_estadual"]["Restricao10"]
                restricao_11 = response["bin_estadual"]["Restricao11"]

                if restricao_1:
                    restricoes += restricao_1
                if restricao_2:
                    restricoes += f", {restricao_2}"
                if restricao_3:
                    restricoes += f", {restricao_3}"
                if restricao_4:
                    restricoes += f", {restricao_4}"
                if restricao_5:
                    restricoes += f", {restricao_5}"
                if restricao_6:
                    restricoes += f", {restricao_6}"
                if restricao_7:
                    restricoes += f", {restricao_7}"
                if restricao_8:
                    restricoes += f", {restricao_8}"
                if restricao_9:
                    restricoes += f", {restricao_9}"
                if restricao_10:
                    restricoes += f", {restricao_10}"
                if restricao_11:
                    restricoes += f", {restricao_11}"

                debts = self.calculate_debts(
                    [
                        response["bin_estadual"]["ValorDebitoDpvat"],
                        response["bin_estadual"]["ValorDebitoDersa"],
                        response["bin_estadual"]["ValorDebitoMunicipais"],
                        response["bin_estadual"]["ValorDebitoDer"],
                        response["bin_estadual"]["ValorDebitoPrf"],
                        response["bin_estadual"]["ValorDebitoLicenc"],
                        response["bin_estadual"]["ValorDebitoIpva"],
                        response["bin_estadual"]["ValorDebitoRenainf"],
                        response["bin_estadual"]["ValorDebitoMultas"],
                        response["bin_estadual"]["ValorDebitoCetesb"],
                        response["bin_estadual"]["ValorDebitoDetran"],
                    ]
                )

                append_data = {
                    "Lote Ref. / Ativo-Frota": "",
                    "Tabela Molicar": "",
                    "Tabela Fipe": fipe_val,
                    "Proprietário/CNPJ (Proprietário do documento)": response[
                        "bin_estadual"
                    ]["Proprietario"].upper(),
                    "Restrições": restricoes,
                    "Débitos (Total)": debts,
                    "Tipo": response["bin_estadual"]["Tipo"],
                    "Marca (SEMPRE MAIUSCULA)": response["bin_estadual"]["Marca"],
                    "Modelo (SEMPRE MAIUSCULA)": response["bin_estadual"]["Modelo"],
                    "Ano Fab/Modelo": response["bin_estadual"]["AnoFabricacao"],
                    "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))": response[
                        "bin_estadual"
                    ][
                        "Placa"
                    ].upper(),
                    "Chassi (SEMPRE MAIUSCULA)": response["bin_estadual"][
                        "Chassi"
                    ].upper(),
                    "Renavam": response["bin_estadual"]["Renavam"],
                    "Cor": response["bin_estadual"]["Cor"],
                    "Combustível": response["bin_estadual"]["Combustivel"],
                    "Cilindrada": response["bin_estadual"]["Cilindrada"],
                    "Situação Veículo": response["bin_estadual"]["SituacaoVeiculo"],
                    "Tipo de Remarcação do Chassi": response["bin_estadual"][
                        "TipoRemarcacaoChassi"
                    ],
                    "Espécie": response["bin_estadual"]["Especie"],
                    "Carroceria": response["bin_estadual"]["Carroceria"],
                    "Potência": response["bin_estadual"]["Potencia"],
                    "Município": response["bin_estadual"]["Municipio"],
                    "Nº Motor": response["bin_estadual"]["NrMotor"],
                    "Procedência do Veículo": response["bin_estadual"][
                        "ProcedenciaVeiculo"
                    ],
                    "Capacidade de Carga": response["bin_estadual"][
                        "CapacidadeDeCarga"
                    ],
                    "Capacidade de Passageiros": response["bin_estadual"][
                        "CapacidadePassageiros"
                    ],
                    "Nº Carroceria": response["bin_estadual"]["Carroceria"],
                    "Nº Caixa de Câmbio": response["bin_estadual"]["NrCaixaCambio"],
                    "Nº Eixos": response["bin_estadual"]["NrEixos"],
                    "Terceiro Eixo": response["bin_estadual"]["TerceiroEixo"],
                    "Eixo Traseiro Diferencial": response["bin_estadual"][
                        "EixoTrasDiferencial"
                    ],
                    "Montagem": response["bin_estadual"]["Montagem"],
                    "CMT": response["bin_estadual"]["CMT"],
                    "PBT": response["bin_estadual"]["PBT"],
                }

                temp_list.append(append_data)

        df_list = pandas.DataFrame(temp_list, columns=df_columns)
        writer = pandas.ExcelWriter(self._output_xlsx_file, engine="xlsxwriter")

        df_list.to_excel(writer, sheet_name="Listagem", index=False)
        writer.save()


if __name__ == "__main__":
    try:
        logger.info("Iniciando a conversão")
        rgAutomovelConverter = RGAutomovelConverter(
            ".",
            ["input"],
            [
                "output",
                os.path.join("output", "xlsx"),
            ],
            os.path.join("output", "xlsx", "Planilha_Unificada_2021_v6.3.xlsx"),
        )
        rgAutomovelConverter.execute()
    except Exception as error:
        logger.error("Ocorreu algum erro inesperado no processamento da planilha")
        logger.exception(error)

    logger.info("Processo finalizado com sucesso.")
    done = str(input("Pressione ENTER para encerrar..."))
