import os
import re

import pandas
import requests

from services.base.logger import Logger
from services.base.spreadsheet_converter import SpreadsheetConverter


logger = Logger.__call__().get_logger()


class CONST:
    PLATE = "Placa"
    CHASSI = "Chassi"
    FIPE = "Consultar Tabela Fipe?"


class RespostaException(Exception):
    """
    Disparada quando ocorre o erro O script não encontrou o objeto "Resposta" na resposta
    """

    pass


class RGAutomovelConverter(SpreadsheetConverter):
    def calculate_debts(self, values):
        total = 0
        for value in values:
            try:
                val = re.sub("[^0-9,.]", "", value)

                if len(val.strip()) == 0:
                    val = "0,00"

                total += float(val.replace(".", "").replace(",", "."))
            except Exception:
                logger.error(f"Valor recebido que ocasionou um erro: {value}")
                raise

        return total

    def get_vehicle_data(self, plate, chassi, check_fipe):
        base_url = "http://ws.rgdoautomovel.com.br"

        request_params = {
            "pstrFormat": "json",
            "pstrCliente": "maisativo.sbid",
            "pstrLogin": "maisativo.sbid",
            "pstrSenha": "sbid153",
        }

        if plate != "":
            request_params["pstrPlaca"] = plate
        elif chassi != "":
            request_params["pstrChassi"] = chassi

        if plate != "" or chassi != "":
            try:
                logger.info("Chamando a API BIN Estadual do RG do Automóvel")

                for i in range(5):
                    try:
                        logger.info(f"Tentativa {(i + 1)}/5")

                        bin_estadual_response = requests.get(
                            f"{base_url}/binestadual",
                            params=request_params,
                            timeout=300,
                        )

                        bin_estadual_json = bin_estadual_response.json()

                        logger.debug(
                            f'Resposta da API BIN Estadual do RG do Automóvel: "{bin_estadual_json}"'
                        )

                        if "struct_RespostaRst" in bin_estadual_json.keys():
                            bin_estadual_json = bin_estadual_json["struct_RespostaRst"]

                            if "erro" in bin_estadual_json.keys():
                                if bin_estadual_json["erro"]:
                                    raise Exception(
                                        str(bin_estadual_json["erroCodigo"])
                                        + " - "
                                        + str(bin_estadual_json["msg"])
                                    )

                            if "Resposta" in bin_estadual_json.keys():
                                bin_estadual_json = bin_estadual_json["Resposta"]

                                if "Placa" not in bin_estadual_json.keys():
                                    bin_estadual_json["Placa"] = ""
                                if "UF" not in bin_estadual_json.keys():
                                    bin_estadual_json["UF"] = ""
                                if "Chassi" not in bin_estadual_json.keys():
                                    bin_estadual_json["Chassi"] = ""
                                if "Tipo" not in bin_estadual_json.keys():
                                    bin_estadual_json["Tipo"] = ""
                                if "Marca" not in bin_estadual_json.keys():
                                    bin_estadual_json["Marca"] = ""
                                if "MarcaTratada" not in bin_estadual_json.keys():
                                    bin_estadual_json["MarcaTratada"] = ""
                                if "Modelo" not in bin_estadual_json.keys():
                                    bin_estadual_json["Modelo"] = ""
                                if "AnoFabricacao" not in bin_estadual_json.keys():
                                    bin_estadual_json["AnoFabricacao"] = ""
                                if "AnoModelo" not in bin_estadual_json.keys():
                                    bin_estadual_json["AnoModelo"] = ""
                                if "Renavam" not in bin_estadual_json.keys():
                                    bin_estadual_json["Renavam"] = ""
                                if "Cor" not in bin_estadual_json.keys():
                                    bin_estadual_json["Cor"] = ""
                                if "Combustivel" not in bin_estadual_json.keys():
                                    bin_estadual_json["Combustivel"] = ""
                                if "Cilindrada" not in bin_estadual_json.keys():
                                    bin_estadual_json["Cilindrada"] = ""
                                if "Proprietario" not in bin_estadual_json.keys():
                                    bin_estadual_json["Proprietario"] = ""
                                if "SituacaoVeiculo" not in bin_estadual_json.keys():
                                    bin_estadual_json["SituacaoVeiculo"] = ""
                                if (
                                    "TipoRemarcacaoChassi"
                                    not in bin_estadual_json.keys()
                                ):
                                    bin_estadual_json["TipoRemarcacaoChassi"] = ""
                                if "Especie" not in bin_estadual_json.keys():
                                    bin_estadual_json["Especie"] = ""
                                if "Carroceria" not in bin_estadual_json.keys():
                                    bin_estadual_json["Carroceria"] = ""
                                if "Potencia" not in bin_estadual_json.keys():
                                    bin_estadual_json["Potencia"] = ""
                                if "Municipio" not in bin_estadual_json.keys():
                                    bin_estadual_json["Municipio"] = ""
                                if "NrMotor" not in bin_estadual_json.keys():
                                    bin_estadual_json["NrMotor"] = ""
                                if "ProcedenciaVeiculo" not in bin_estadual_json.keys():
                                    bin_estadual_json["ProcedenciaVeiculo"] = ""
                                if "CapacidadeDeCarga" not in bin_estadual_json.keys():
                                    bin_estadual_json["CapacidadeDeCarga"] = ""
                                if (
                                    "CapacidadePassageiros"
                                    not in bin_estadual_json.keys()
                                ):
                                    bin_estadual_json["CapacidadePassageiros"] = ""
                                if "Carroceria" not in bin_estadual_json.keys():
                                    bin_estadual_json["Carroceria"] = ""
                                if "NrCaixaCambio" not in bin_estadual_json.keys():
                                    bin_estadual_json["NrCaixaCambio"] = ""
                                if "NrEixos" not in bin_estadual_json.keys():
                                    bin_estadual_json["NrEixos"] = ""
                                if "TerceiroEixo" not in bin_estadual_json.keys():
                                    bin_estadual_json["TerceiroEixo"] = ""
                                if (
                                    "EixoTrasDiferencial"
                                    not in bin_estadual_json.keys()
                                ):
                                    bin_estadual_json["EixoTrasDiferencial"] = ""
                                if "Montagem" not in bin_estadual_json.keys():
                                    bin_estadual_json["Montagem"] = ""
                                if "CMT" not in bin_estadual_json.keys():
                                    bin_estadual_json["CMT"] = ""
                                if "PBT" not in bin_estadual_json.keys():
                                    bin_estadual_json["PBT"] = ""
                                if "Restricao1" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao1"] = ""
                                if "Restricao2" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao2"] = ""
                                if "Restricao3" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao3"] = ""
                                if "Restricao4" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao4"] = ""
                                if "Restricao5" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao5"] = ""
                                if "Restricao6" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao6"] = ""
                                if "Restricao7" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao7"] = ""
                                if "Restricao8" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao8"] = ""
                                if "Restricao9" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao9"] = ""
                                if "Restricao10" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao10"] = ""
                                if "Restricao11" not in bin_estadual_json.keys():
                                    bin_estadual_json["Restricao11"] = ""
                                if "restricoes" not in bin_estadual_json.keys():
                                    bin_estadual_json["restricoes"] = ""
                                if "ValorDebitoIpva" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoIpva"] = ""
                                if "ValorDebitoDpvat" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoDpvat"] = ""
                                if "ValorDebitoDetran" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoDetran"] = ""
                                if "ValorDebitoPrf" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoPrf"] = ""
                                if "ValorDebitoDer" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoDer"] = ""
                                if "ValorDebitoDersa" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoDersa"] = ""
                                if "ValorDebitoCetesb" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoCetesb"] = ""
                                if "ValorDebitoRenainf" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoRenainf"] = ""
                                if "ValorDebitoMultas" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoMultas"] = ""
                                if "ValorDebitoLicenc" not in bin_estadual_json.keys():
                                    bin_estadual_json["ValorDebitoLicenc"] = ""
                                if (
                                    "ValorDebitoMunicipais"
                                    not in bin_estadual_json.keys()
                                ):
                                    bin_estadual_json["ValorDebitoMunicipais"] = ""
                                if "debitos" not in bin_estadual_json.keys():
                                    bin_estadual_json["debitos"] = ""
                                if "observacoes_gerais" not in bin_estadual_json.keys():
                                    bin_estadual_json["observacoes_gerais"] = ""

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "Marca"
                                ]

                                if bin_estadual_json["MarcaTratada"] == "CHEV":
                                    bin_estadual_json["MarcaTratada"] = "CHEVROLET"
                                elif bin_estadual_json["MarcaTratada"] == "GM":
                                    bin_estadual_json["MarcaTratada"] = "CHEVROLET"
                                elif bin_estadual_json["MarcaTratada"] == "VOLKS":
                                    bin_estadual_json["MarcaTratada"] = "VOLKSWAGEN"
                                elif bin_estadual_json["MarcaTratada"] == "VW":
                                    bin_estadual_json["MarcaTratada"] = "VOLKSWAGEN"
                                elif bin_estadual_json["MarcaTratada"] == "MMC":
                                    bin_estadual_json["MarcaTratada"] = "MITSUBISHI"
                                elif bin_estadual_json["MarcaTratada"] == "MB":
                                    bin_estadual_json["MarcaTratada"] = "MERCEDES-BENZ"
                                elif bin_estadual_json["MarcaTratada"] == "MBB":
                                    bin_estadual_json["MarcaTratada"] = "MERCEDES-BENZ"
                                elif bin_estadual_json["MarcaTratada"] == "LR":
                                    bin_estadual_json["MarcaTratada"] = "LAND ROVER"

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("CHEV ", "CHEVROLET ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("CHEV/", "CHEVROLET/")

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("GM ", "CHEVROLET ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("GM/", "CHEVROLET/")

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("VOLKS ", "VOLKSWAGEN ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("VOLKS/", "VOLKSWAGEN/")

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("VW ", "VOLKSWAGEN ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("VW/", "VOLKSWAGEN/")

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("MMC ", "MITSUBISHI ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("MMC/", "MITSUBISHI/")

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("MB ", "MERCEDES-BENZ ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("MB/", "MERCEDES-BENZ/")

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("MBB ", "MERCEDES-BENZ ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("MBB/", "MERCEDES-BENZ/")

                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("LR ", "LAND ROVER ")
                                bin_estadual_json["MarcaTratada"] = bin_estadual_json[
                                    "MarcaTratada"
                                ].replace("LR/", "LAND ROVER/")

                                logger.debug(
                                    f'Placa: "{bin_estadual_json["Placa"].upper()}"'
                                )
                                logger.debug(f'UF: "{bin_estadual_json["UF"].upper()}"')
                                logger.debug(
                                    f'Chassi: "{bin_estadual_json["Chassi"].upper()}"'
                                )
                                logger.debug(f'Tipo: "{bin_estadual_json["Tipo"]}"')
                                logger.debug(
                                    f'Marca (original): "{bin_estadual_json["Marca"].upper()}"'
                                )
                                logger.debug(
                                    f'Marca (tratada): "{bin_estadual_json["MarcaTratada"].upper()}"'
                                )
                                logger.debug(
                                    f'Modelo: "{bin_estadual_json["Modelo"].upper()}"'
                                )
                                logger.debug(
                                    f'Ano Fabricação: "{bin_estadual_json["AnoFabricacao"]}"'
                                )
                                logger.debug(
                                    f'Ano Modelo: "{bin_estadual_json["AnoModelo"]}"'
                                )
                                logger.debug(
                                    f'Renavam: "{bin_estadual_json["Renavam"]}"'
                                )
                                logger.debug(f'Cor: "{bin_estadual_json["Cor"]}"')
                                logger.debug(
                                    f'Combustível: "{bin_estadual_json["Combustivel"]}"'
                                )
                                logger.debug(
                                    f'Cilindrada: "{bin_estadual_json["Cilindrada"]}"'
                                )
                                logger.debug(
                                    f'Proprietário: "{bin_estadual_json["Proprietario"].upper()}"'
                                )
                                logger.debug(
                                    f'Situação do Veículo: "{bin_estadual_json["SituacaoVeiculo"]}"'
                                )
                                logger.debug(
                                    f'Tipo de Remarcação do Chassi: "{bin_estadual_json["TipoRemarcacaoChassi"]}"'
                                )
                                logger.debug(
                                    f'Espécie: "{bin_estadual_json["Especie"]}"'
                                )
                                logger.debug(
                                    f'Carroceria: "{bin_estadual_json["Carroceria"]}"'
                                )
                                logger.debug(
                                    f'Potência: "{bin_estadual_json["Potencia"]}"'
                                )
                                logger.debug(
                                    f'Município: "{bin_estadual_json["Municipio"]}"'
                                )
                                logger.debug(
                                    f'Nº Motor: "{bin_estadual_json["NrMotor"]}"'
                                )
                                logger.debug(
                                    f'Procedência do Veículo: "{bin_estadual_json["ProcedenciaVeiculo"]}"'
                                )
                                logger.debug(
                                    f'Capacidade de Carga: "{bin_estadual_json["CapacidadeDeCarga"]}"'
                                )
                                logger.debug(
                                    f'Capacidade de Passageiros: "{bin_estadual_json["CapacidadePassageiros"]}"'
                                )
                                logger.debug(
                                    f'Nº Carroceria: "{bin_estadual_json["Carroceria"]}"'
                                )
                                logger.debug(
                                    f'Nº Caixa de Câmbio: "{bin_estadual_json["NrCaixaCambio"]}"'
                                )
                                logger.debug(
                                    f'Nº Eixos: "{bin_estadual_json["NrEixos"]}"'
                                )
                                logger.debug(
                                    f'Terceiro Eixo: "{bin_estadual_json["TerceiroEixo"]}"'
                                )
                                logger.debug(
                                    f'Eixo Traseiro Diferencial: "{bin_estadual_json["EixoTrasDiferencial"]}"'
                                )
                                logger.debug(
                                    f'Montagem: "{bin_estadual_json["Montagem"]}"'
                                )
                                logger.debug(f'CMT: "{bin_estadual_json["CMT"]}"')
                                logger.debug(f'PBT: "{bin_estadual_json["PBT"]}"')

                                logger.debug(
                                    f'Restrição 1: "{bin_estadual_json["Restricao1"]}"'
                                )
                                logger.debug(
                                    f'Restrição 2: "{bin_estadual_json["Restricao2"]}"'
                                )
                                logger.debug(
                                    f'Restrição 3: "{bin_estadual_json["Restricao3"]}"'
                                )
                                logger.debug(
                                    f'Restrição 4: "{bin_estadual_json["Restricao4"]}"'
                                )
                                logger.debug(
                                    f'Restrição 5: "{bin_estadual_json["Restricao5"]}"'
                                )
                                logger.debug(
                                    f'Restrição 6: "{bin_estadual_json["Restricao6"]}"'
                                )
                                logger.debug(
                                    f'Restrição 7: "{bin_estadual_json["Restricao7"]}"'
                                )
                                logger.debug(
                                    f'Restrição 8: "{bin_estadual_json["Restricao8"]}"'
                                )
                                logger.debug(
                                    f'Restrição 9: "{bin_estadual_json["Restricao9"]}"'
                                )
                                logger.debug(
                                    f'Restrição 10: "{bin_estadual_json["Restricao10"]}"'
                                )
                                logger.debug(
                                    f'Restrição 11: "{bin_estadual_json["Restricao11"]}"'
                                )

                                bin_estadual_json["restricoes"] = ""

                                try:
                                    if bin_estadual_json["Restricao1"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += bin_estadual_json["Restricao1"]
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 1" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao2"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao2"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 2" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao3"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao3"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 3" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao4"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao4"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 4" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao5"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao5"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 5" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao6"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao6"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 6" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao7"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao7"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 7" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao8"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao8"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 8" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao9"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao9"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 9" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao10"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao10"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 10" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                try:
                                    if bin_estadual_json["Restricao11"]:
                                        bin_estadual_json[
                                            "restricoes"
                                        ] += f', {bin_estadual_json["Restricao11"]}'
                                except Exception:
                                    logger.warning(
                                        'Erro ao tentar concatenar "Restrição 11" ao campo "Restrições concatenadas". Campo foi desconsiderado para não abortar a operação.'
                                    )

                                if bin_estadual_json["restricoes"] == "":
                                    bin_estadual_json["restricoes"] = "NADA CONSTA"

                                logger.debug(
                                    f'Restrições Concatenadas: {bin_estadual_json["restricoes"]}'
                                )

                                logger.debug(
                                    f'IPVA: "{bin_estadual_json["ValorDebitoIpva"]}"'
                                )
                                logger.debug(
                                    f'DPVAT: "{bin_estadual_json["ValorDebitoDpvat"]}"'
                                )
                                logger.debug(
                                    f'DETRAN: "{bin_estadual_json["ValorDebitoDetran"]}"'
                                )
                                logger.debug(
                                    f'PRF: "{bin_estadual_json["ValorDebitoPrf"]}"'
                                )
                                logger.debug(
                                    f'DER: "{bin_estadual_json["ValorDebitoDer"]}"'
                                )
                                logger.debug(
                                    f'DERSA: "{bin_estadual_json["ValorDebitoDersa"]}"'
                                )
                                logger.debug(
                                    f'CETESB: "{bin_estadual_json["ValorDebitoCetesb"]}"'
                                )
                                logger.debug(
                                    f'RENAINF: "{bin_estadual_json["ValorDebitoRenainf"]}"'
                                )
                                logger.debug(
                                    f'Multas: "{bin_estadual_json["ValorDebitoMultas"]}"'
                                )
                                logger.debug(
                                    f'Licenciamento: "{bin_estadual_json["ValorDebitoLicenc"]}"'
                                )
                                logger.debug(
                                    f'Débitos Municipais: "{bin_estadual_json["ValorDebitoMunicipais"]}"'
                                )

                                bin_estadual_json["debitos"] = 0

                                try:
                                    bin_estadual_json["debitos"] = self.calculate_debts(
                                        [
                                            bin_estadual_json["ValorDebitoDpvat"],
                                            bin_estadual_json["ValorDebitoDersa"],
                                            bin_estadual_json["ValorDebitoMunicipais"],
                                            bin_estadual_json["ValorDebitoDer"],
                                            bin_estadual_json["ValorDebitoPrf"],
                                            bin_estadual_json["ValorDebitoLicenc"],
                                            bin_estadual_json["ValorDebitoIpva"],
                                            bin_estadual_json["ValorDebitoRenainf"],
                                            bin_estadual_json["ValorDebitoMultas"],
                                            bin_estadual_json["ValorDebitoCetesb"],
                                            bin_estadual_json["ValorDebitoDetran"],
                                        ]
                                    )
                                except Exception:
                                    logger.warning(
                                        "Erro ao tentar calcular somatório de débitos. Aplicado valor zero para não abortar a operação."
                                    )

                                if bin_estadual_json["debitos"] == 0:
                                    bin_estadual_json["debitos"] = "NADA CONSTA"

                                logger.debug(
                                    f'Total de Débitos: {bin_estadual_json["debitos"]}'
                                )

                                bin_estadual_json["observacoes_gerais"] = ""

                                if bin_estadual_json["Proprietario"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Proprietário não informado"

                                if bin_estadual_json["restricoes"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Restrições não informadas"

                                if bin_estadual_json["debitos"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Débitos não informados"

                                if bin_estadual_json["Tipo"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Tipo não informado"

                                if bin_estadual_json["MarcaTratada"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Marca não informada"

                                if bin_estadual_json["Modelo"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Modelo não informado"

                                if bin_estadual_json["AnoModelo"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Ano Fab/Modelo não informado"

                                if bin_estadual_json["Placa"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Placa não informada"

                                if bin_estadual_json["UF"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "UF não informada"

                                if bin_estadual_json["Chassi"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Chassi não informada"

                                if bin_estadual_json["Renavam"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Renavam não informado"

                                if bin_estadual_json["Cor"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Cor não informada"

                                if bin_estadual_json["Combustivel"] == "":
                                    bin_estadual_json[
                                        "observacoes_gerais"
                                    ] = "Combustível não informado"

                                break
                            else:
                                raise RespostaException(
                                    'O script não encontrou o objeto "Resposta" na resposta'
                                )
                        else:
                            raise Exception(
                                'O script não encontrou o objeto "struct_RespostaRst" na resposta'
                            )
                    except RespostaException as error:
                        logger.info(error)

                        if (i + 1) == 5:
                            raise Exception(bin_estadual_json["Controle"]["Descricao"])
                    except Exception as error:
                        if isinstance(error, requests.exceptions.ReadTimeout):
                            logger.info("Ocorreu timeout")

                            if (i + 1) == 5:
                                raise Exception("Atingiu o limite de timeouts")
                        else:
                            raise
            except Exception as error:
                logger.error(
                    f'A API BIN Estadual do RG do Automóvel respondeu diferente do esperado. Mais informações: "{error}"'
                )
                raise

        valor_fipe = ""
        if check_fipe:
            try:
                logger.info("Chamando a API Precificador do RG do Automóvel")

                for i in range(5):
                    try:
                        logger.info(f"Tentativa {(i + 1)}/5")

                        precificador_response = requests.get(
                            f"{base_url}/precificador",
                            params=request_params,
                            timeout=300,
                        )

                        precificador_json = precificador_response.json()

                        logger.debug(
                            f'Resposta da API Precificador do RG do Automóvel: "{precificador_json}"'
                        )

                        if "struct_RespostaRst" in precificador_json.keys():
                            precificador_json = precificador_json["struct_RespostaRst"]

                            if "erro" in precificador_json.keys():
                                if precificador_json["erro"]:
                                    raise Exception(
                                        str(precificador_json["erroCodigo"])
                                        + " - "
                                        + str(precificador_json["msg"])
                                    )

                            if "Resposta" in precificador_json.keys():
                                precificador_json = precificador_json["Resposta"]

                                if (
                                    "struct_ResultadoPrecificador"
                                    in precificador_json.keys()
                                ):
                                    precificador_json = precificador_json[
                                        "struct_ResultadoPrecificador"
                                    ]

                                    if isinstance(precificador_json, list):
                                        precificador_json = precificador_json[0]

                                    if "PrecoFipe" in precificador_json.keys():
                                        if precificador_json["PrecoFipe"]:
                                            valor_fipe = precificador_json["PrecoFipe"]
                                        else:
                                            valor_fipe = "0,00"

                                        logger.debug(f'Tabela Fipe: "{valor_fipe}"')
                                        break
                                    else:
                                        raise Exception(
                                            'O script não encontrou o atributo "PrecoFipe" na resposta'
                                        )
                                else:
                                    raise Exception(
                                        'O script não encontrou o objeto "struct_ResultadoPrecificador" na resposta'
                                    )
                            else:
                                raise Exception(
                                    'O script não encontrou o objeto "Resposta" na resposta'
                                )
                        else:
                            raise Exception(
                                'O script não encontrou o objeto "struct_RespostaRst" na resposta'
                            )
                    except RespostaException as error:
                        logger.info(error)

                        if (i + 1) == 5:
                            raise Exception(bin_estadual_json["Controle"]["Descricao"])
                    except Exception as error:
                        if isinstance(error, requests.exceptions.ReadTimeout):
                            logger.info("Ocorreu timeout")

                            if (i + 1) == 5:
                                valor_fipe = "Timeout"
                                raise Exception("Atingiu o limite de timeouts")
                        else:
                            raise
            except Exception as error:
                logger.error(
                    f'A API Precificador do RG do Automóvel respondeu diferente do esperado. Mais informações: "{error}"'
                )

        return {
            "bin_estadual": bin_estadual_json,
            "valor_fipe": valor_fipe,
        }

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
            "Observações Gerais",
        ]

        for idx, v in enumerate(data[CONST.PLATE]):
            check_fipe = False

            plate = (
                data[CONST.PLATE]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )
            chassi = (
                data[CONST.CHASSI]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )
            fipe = (
                data[CONST.FIPE]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )

            if plate == "NULL":
                plate = ""

            if chassi == "NULL":
                chassi = ""

            if fipe == "S" or fipe == "SIM" or fipe == "Y" or fipe == "YES":
                check_fipe = True

            logger.info("Lendo registro da planilha de entrada:")
            logger.info(f'--> Placa: "{plate}"')
            logger.info(f'--> Chassi: "{chassi}"')
            logger.info(f'--> Consultar Tabela Fipe? "{fipe}"')

            if plate != "" or chassi != "":
                try:
                    response = self.get_vehicle_data(plate, chassi, check_fipe)

                    logger.info("Adicionando registro à planilha de saída")

                    append_data = {
                        "Lote Ref. / Ativo-Frota": "",
                        "Tabela Molicar": "",
                        "Tabela Fipe": response["valor_fipe"],
                        "Proprietário/CNPJ (Proprietário do documento)": response[
                            "bin_estadual"
                        ]["Proprietario"].upper(),
                        "Restrições": response["bin_estadual"]["restricoes"],
                        "Débitos (Total)": response["bin_estadual"]["debitos"],
                        "Tipo": response["bin_estadual"]["Tipo"],
                        "Marca (SEMPRE MAIUSCULA)": response["bin_estadual"][
                            "MarcaTratada"
                        ].upper(),
                        "Modelo (SEMPRE MAIUSCULA)": response["bin_estadual"][
                            "Modelo"
                        ].upper(),
                        "Ano Fab/Modelo": f"{response['bin_estadual']['AnoFabricacao']}/{response['bin_estadual']['AnoModelo']}",
                        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))": f"{str(response['bin_estadual']['Placa'].upper())} ({response['bin_estadual']['UF'].upper()})",
                        "Chassi (SEMPRE MAIUSCULA)": str(
                            response["bin_estadual"]["Chassi"]
                        ).upper(),
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
                        "Observações Gerais": response["bin_estadual"][
                            "observacoes_gerais"
                        ],
                    }

                    temp_list.append(append_data)

                    logger.info("Registro adicionado à planilha de saída com sucesso")
                except Exception as error:
                    temp_list.append(
                        {
                            "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))": str(
                                plate
                            ).upper(),
                            "Chassi (SEMPRE MAIUSCULA)": str(chassi).upper(),
                            "Observações Gerais": f"{error}",
                        }
                    )

                    logger.info(
                        "Registro adicionado à planilha de saída descrevendo erro encontrado durante o processamento"
                    )

        df = pandas.DataFrame(temp_list, columns=df_columns)

        if os.path.isfile(self._output_xlsx_file):
            append_data = pandas.read_excel(
                self._output_xlsx_file, sheet_name="Listagem"
            )
            df = pandas.concat([append_data, df])

        writer = pandas.ExcelWriter(self._output_xlsx_file, engine="xlsxwriter")

        df.to_excel(writer, sheet_name="Listagem", index=False)
        writer.save()

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
                logger.info(
                    f"Processamento da planilha {count} de {len(list_files)} iniciado"
                )

                self.process_file(file)

                logger.info(
                    f"Processamento da planilha {count} de {len(list_files)} finalizado"
                )
                count += 1
            except Exception as error:
                logger.error(f'Erro "{error}" no processamento do arquivo "{file}"')


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
            os.path.join("output", "xlsx", "resulting_spreadsheet.xlsx"),
        )
        rgAutomovelConverter.execute()

        logger.info("Processo finalizado com sucesso.")
        done = str(input("Pressione ENTER para encerrar..."))
    except Exception as error:
        logger.error(f'Ocorreu o erro "{error}" no processamento da planilha')
