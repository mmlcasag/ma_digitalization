import os
import re

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
            try:
                val = re.sub("[^0-9,.]", "", value)
                
                if len(val.strip()) == 0:
                    val = "0,00"
                
                total += float(val.replace(".", "").replace(",", "."))
            except Exception as error:
                logger.error(f"Valor recebido que ocasionou um erro: {value}")
                raise

        return total


    def get_vehicle_data(self, plate, serial_number, check_fipe):
        try:
            base_url = "http://ws.rgdoautomovel.com.br"
            
            request_params = {
                "pstrFormat": "json",
                "pstrCliente": "maisativo.sbid",
                "pstrLogin": "maisativo.sbid",
                "pstrSenha": "sbid153",
            }

            if plate != "null":
                logger.info(
                    "Buscando informações do veículo de placa {}".format(str(plate))
                )
                request_params["pstrPlaca"] = plate

            if serial_number != "null":
                logger.info(
                    "Buscando informações do veículo de chassi {}".format(
                        str(serial_number)
                    )
                )
                request_params["pstrChassi"] = serial_number

            bin_estadual_response = requests.get(
                f"{base_url}/binestadual", params=request_params, timeout=300
            )

            bin_estadual_json = bin_estadual_response.json()

            logger.info("OK")
        except Exception as error:
            logger.error(f'Erro "{error}" ao tentar chamar a API de Dados Estaduais do RG do Automóvel')
            raise

        try:
            precificador = {
                "struct_RespostaRst": {"Resposta": {"struct_ResultadoPrecificador": False}}
            }
            if check_fipe:
                logger.info("Buscando valores na tabela Fipe")
                
                precificador_response = requests.get(
                    f"{base_url}/precificador", params=request_params, timeout=300
                )
                
                precificador_json = precificador_response.json()
                
                if "struct_RespostaRst" in precificador_json.keys():
                    precificador_json = precificador_json["struct_RespostaRst"]
                    if "Resposta" in precificador_json.keys():
                        precificador_json = precificador_json["Resposta"]
                        if "struct_ResultadoPrecificador" in precificador_json.keys():
                            precificador = precificador_json["struct_ResultadoPrecificador"]
                
                if isinstance(precificador, list):
                    precificador = precificador[0]

                logger.info("OK")
        except Exception as error:
            logger.error(f'Erro "{error}" ao tentar chamar a API de Precificação do RG do Automóvel')
            raise
        
        return {
            "bin_estadual": bin_estadual_json["struct_RespostaRst"]["Resposta"],
            "precificador": precificador,
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
        ]

        for idx, v in enumerate(data[CONST.PLATE]):
            plate = data[CONST.PLATE].fillna("null").values[idx]
            serial_number = data[CONST.SERIAL_NUMBER].fillna("null").values[idx]
            fipe = data[CONST.FIPE].fillna("null").values[idx].lower()
            check_fipe = False
            fipe_val = ""

            if fipe == "s" or fipe == " sim":
                check_fipe = True
            
            if plate == "null":
                plate = ""
            
            if serial_number == "null":
                serial_number = ""

            if plate != "" or serial_number != "":
                try:
                    response = self.get_vehicle_data(plate, serial_number, check_fipe)

                    if plate == "FUW0401":
                        raise Exception("Invalid plate")

                    if check_fipe:
                        if "PrecoFipe" in response["precificador"].keys():
                            fipe_val = response["precificador"]["PrecoFipe"]
                        else:
                            logger.warning("RG do Automóvel não encontrou valor de Fipe para esse veículo")

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
                    
                    restricoes = ""
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

                    logger.debug(f'Tabela Fipe: {fipe_val}')
                    logger.debug(f'Proprietário: {response["bin_estadual"]["Proprietario"].upper()}')
                    logger.debug(f'Restrição 1: {restricao_1}')
                    logger.debug(f'Restrição 2: {restricao_2}')
                    logger.debug(f'Restrição 3: {restricao_3}')
                    logger.debug(f'Restrição 4: {restricao_4}')
                    logger.debug(f'Restrição 5: {restricao_5}')
                    logger.debug(f'Restrição 6: {restricao_6}')
                    logger.debug(f'Restrição 7: {restricao_7}')
                    logger.debug(f'Restrição 8: {restricao_8}')
                    logger.debug(f'Restrição 9: {restricao_9}')
                    logger.debug(f'Restrição 10: {restricao_10}')
                    logger.debug(f'Restrição 11: {restricao_11}')
                    logger.debug(f'Restrições: {restricoes}')
                    logger.debug(f'Débitos Municipais: {response["bin_estadual"]["ValorDebitoMunicipais"]}')
                    logger.debug(f'Licenciamento: {response["bin_estadual"]["ValorDebitoLicenc"]}')
                    logger.debug(f'Multas: {response["bin_estadual"]["ValorDebitoMultas"]}')
                    logger.debug(f'IPVA: {response["bin_estadual"]["ValorDebitoIpva"]}')
                    logger.debug(f'DPVAT: {response["bin_estadual"]["ValorDebitoDpvat"]}')
                    logger.debug(f'DETRAN: {response["bin_estadual"]["ValorDebitoDetran"]}')
                    logger.debug(f'PRF: {response["bin_estadual"]["ValorDebitoPrf"]}')
                    logger.debug(f'DER: {response["bin_estadual"]["ValorDebitoDer"]}')
                    logger.debug(f'DERSA: {response["bin_estadual"]["ValorDebitoDersa"]}')
                    logger.debug(f'CETESB: {response["bin_estadual"]["ValorDebitoCetesb"]}')
                    logger.debug(f'RENAINF: {response["bin_estadual"]["ValorDebitoRenainf"]}')
                    logger.debug(f'Total de Débitos: {debts}')
                    logger.debug(f'Tipo: {response["bin_estadual"]["Tipo"]}')
                    logger.debug(f'Marca: {response["bin_estadual"]["Marca"].upper()}')
                    logger.debug(f'Modelo: {response["bin_estadual"]["Modelo"].upper()}')
                    logger.debug(f'Ano Fabricação: {response["bin_estadual"]["AnoFabricacao"]}')
                    logger.debug(f'Ano Modelo: {response["bin_estadual"]["AnoModelo"]}')
                    logger.debug(f'Placa: {response["bin_estadual"]["Placa"].upper()}')
                    logger.debug(f'UF: {response["bin_estadual"]["UF"].upper()}')
                    logger.debug(f'Chassi: {response["bin_estadual"]["Chassi"].upper()}')
                    logger.debug(f'Renavam: {response["bin_estadual"]["Renavam"]}')
                    logger.debug(f'Cor: {response["bin_estadual"]["Cor"]}')
                    logger.debug(f'Combustível: {response["bin_estadual"]["Combustivel"]}')
                    logger.debug(f'Cilindrada: {response["bin_estadual"]["Cilindrada"]}')
                    logger.debug(f'Situação do Veículo: {response["bin_estadual"]["SituacaoVeiculo"]}')
                    logger.debug(f'Tipo de Remarcação do Chassi: {response["bin_estadual"]["TipoRemarcacaoChassi"]}')
                    logger.debug(f'Espécie: {response["bin_estadual"]["Especie"]}')
                    logger.debug(f'Carroceria: {response["bin_estadual"]["Carroceria"]}')
                    logger.debug(f'Potência: {response["bin_estadual"]["Potencia"]}')
                    logger.debug(f'Município: {response["bin_estadual"]["Municipio"]}')
                    logger.debug(f'Nº Motor: {response["bin_estadual"]["NrMotor"]}')
                    logger.debug(f'Procedência do Veículo: {response["bin_estadual"]["ProcedenciaVeiculo"]}')
                    logger.debug(f'Capacidade de Carga: {response["bin_estadual"]["CapacidadeDeCarga"]}')
                    logger.debug(f'Capacidade de Passageiros: {response["bin_estadual"]["CapacidadePassageiros"]}')
                    logger.debug(f'Nº Carroceria: {response["bin_estadual"]["Carroceria"]}')
                    logger.debug(f'Nº Caixa de Câmbio: {response["bin_estadual"]["NrCaixaCambio"]}')
                    logger.debug(f'Nº Eixos: {response["bin_estadual"]["NrEixos"]}')
                    logger.debug(f'Terceiro Eixo: {response["bin_estadual"]["TerceiroEixo"]}')
                    logger.debug(f'Eixo Traseiro Diferencial: {response["bin_estadual"]["EixoTrasDiferencial"]}')
                    logger.debug(f'Montagem: {response["bin_estadual"]["Montagem"]}')
                    logger.debug(f'CMT: {response["bin_estadual"]["CMT"]}')
                    logger.debug(f'PBT: {response["bin_estadual"]["PBT"]}')
                    
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
                        "Marca (SEMPRE MAIUSCULA)": response["bin_estadual"]["Marca"].upper(),
                        "Modelo (SEMPRE MAIUSCULA)": response["bin_estadual"]["Modelo"].upper(),
                        "Ano Fab/Modelo": f"{response['bin_estadual']['AnoFabricacao']}/{response['bin_estadual']['AnoModelo']}",
                        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))": f"{str(response['bin_estadual']['Placa'].upper())} ({response['bin_estadual']['UF'].upper()})",
                        "Chassi (SEMPRE MAIUSCULA)": str(response["bin_estadual"][
                            "Chassi"
                        ]).upper(),
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
                except Exception as error:
                    temp_list.append({
                        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))": str(plate).upper(),
                        "Chassi (SEMPRE MAIUSCULA)": str(serial_number).upper(),
                        "Modelo (SEMPRE MAIUSCULA)": "Ocorreu um erro ao tentar processar esse registro"
                    })

                    logger.error(f'Ocorreu o erro "{error}" ao processar esse registro')

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
