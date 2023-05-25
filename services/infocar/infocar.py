import os
import pandas
import convert
import extrato
import base_estadual
import codificador_fipe
from services.base.logger import Logger
from services.base.spreadsheet_converter import SpreadsheetConverter


logger = Logger.__call__().get_logger()


class InfocarConverter(SpreadsheetConverter):
    def execute(self, output_format):
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

                if output_format == "1":
                    self.planilha_colunada(file)
                if output_format == "2":
                    self.plataforma_gestor(file)

                logger.info(
                    f"Processamento da planilha {count} de {len(list_files)} finalizado"
                )
                count += 1
            except Exception as error:
                logger.error(f'Erro "{error}" no processamento do arquivo "{file}"')

    def planilha_colunada(self, file):
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

        for idx, v in enumerate(data["Placa"]):
            check_fipe = False

            placa = (
                data["Placa"]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )
            chassi = (
                data["Chassi"]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )
            fipe = (
                data["Consultar Tabela Fipe?"]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )

            if placa == "NULL":
                placa = ""

            if chassi == "NULL":
                chassi = ""

            if fipe == "S" or fipe == "SIM" or fipe == "Y" or fipe == "YES":
                check_fipe = True

            logger.info("Lendo registro da planilha de entrada:")
            logger.info(f'--> Placa: "{placa}"')
            logger.info(f'--> Chassi: "{chassi}"')
            logger.info(f'--> Consultar Tabela Fipe? "{fipe}"')

            if placa != "" or chassi != "":
                try:
                    dados_base_estadual = None
                    if placa != "":
                        dados_base_estadual = base_estadual.request_by_placa(placa)
                        logger.debug(
                            f"Dados Base Estadual:{dados_base_estadual.to_string()}"
                        )
                    elif chassi != "":
                        dados_base_estadual = base_estadual.request_by_chassi(chassi)
                        logger.debug(
                            f"Dados Base Estadual:{dados_base_estadual.to_string()}"
                        )
                    else:
                        raise Exception(
                            "É necessário informar ou placa ou chassi para acessar a base estadual"
                        )

                    dados_precificador = None
                    if check_fipe and placa != "":
                        dados_precificador = codificador_fipe.request_by_placa(placa)
                        logger.debug(
                            f"Dados Precificador:{dados_precificador.to_string()}"
                        )
                    elif check_fipe and chassi != "":
                        dados_precificador = codificador_fipe.request_by_chassi(chassi)
                        logger.debug(
                            f"Dados Precificador:{dados_precificador.to_string()}"
                        )
                    else:
                        logger.info(
                            "Usuário optou por não consultar os dados do Precificador para esse registro"
                        )

                    restricoes_concatenadas = ""
                    if dados_base_estadual is not None:
                        if len(dados_base_estadual.restricoes.restricoes) > 0:
                            for restricao in dados_base_estadual.restricoes.restricoes:
                                if restricoes_concatenadas == "":
                                    restricoes_concatenadas = restricao
                                else:
                                    restricoes_concatenadas = (
                                        restricoes_concatenadas + ", " + restricao
                                    )

                    total_multas = 0
                    try:
                        total_multas = (
                            dados_base_estadual.debitos.debitos_dpvat
                            + dados_base_estadual.debitos.debitos_ipva
                            + dados_base_estadual.debitos.debitos_licenciamento
                            + dados_base_estadual.debitos.debitos_multas
                        )
                    except Exception:
                        total_multas = 0

                    tabelas_fipes_concatenadas = ""
                    if check_fipe and dados_precificador is not None:
                        if len(dados_precificador.tabelas_fipe.valores) > 0:
                            for valor in dados_precificador.tabelas_fipe.valores:
                                if tabelas_fipes_concatenadas == "":
                                    tabelas_fipes_concatenadas = (
                                        "R$ " + convert.from_float_to_string(valor, 2)
                                    )
                                else:
                                    tabelas_fipes_concatenadas = (
                                        tabelas_fipes_concatenadas
                                        + " / "
                                        + "R$ "
                                        + convert.from_float_to_string(valor, 2)
                                    )

                    montagem = ""
                    if check_fipe and dados_precificador is not None:
                        montagem = dados_precificador.dados_veiculo.tipo_montagem

                    logger.debug(f"Restrições concatenadas: {restricoes_concatenadas}")
                    logger.debug(
                        f"Total de multas: {convert.from_float_to_string(total_multas, 2)}"
                    )
                    logger.debug(
                        f"Tabelas FIPE concatenadas: {tabelas_fipes_concatenadas}"
                    )
                    logger.debug(f"Montagem: {montagem}")

                    append_data = {
                        "Lote Ref. / Ativo-Frota": "",
                        "Tabela Molicar": "",
                        "Tabela Fipe": tabelas_fipes_concatenadas,
                        "Proprietário/CNPJ (Proprietário do documento)": dados_base_estadual.proprietario.nome
                        + " / "
                        + dados_base_estadual.proprietario.documento,
                        "Restrições": restricoes_concatenadas,
                        "Débitos (Total)": convert.from_float_to_string(
                            total_multas, 2
                        ),
                        "Tipo": dados_base_estadual.dados_veiculo.tipo_veiculo,
                        "Marca (SEMPRE MAIUSCULA)": dados_base_estadual.dados_veiculo.modelo,
                        "Modelo (SEMPRE MAIUSCULA)": dados_base_estadual.dados_veiculo.modelo,
                        "Ano Fab/Modelo": convert.from_int_to_string(
                            dados_base_estadual.dados_veiculo.ano_fabricacao
                        )
                        + " / "
                        + convert.from_int_to_string(
                            dados_base_estadual.dados_veiculo.ano_modelo
                        ),
                        "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))": dados_base_estadual.dados_veiculo.placa
                        + " "
                        + "("
                        + dados_base_estadual.dados_veiculo.uf_emplacado
                        + ")",
                        "Chassi (SEMPRE MAIUSCULA)": dados_base_estadual.dados_veiculo.chassi,
                        "Renavam": dados_base_estadual.dados_veiculo.renavam,
                        "Cor": dados_base_estadual.dados_veiculo.cor,
                        "Combustível": dados_base_estadual.dados_veiculo.combustivel,
                        "Cilindrada": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.cilindradas
                        ),
                        "Situação Veículo": dados_base_estadual.restricoes.situacao_veiculo,
                        "Tipo de Remarcação do Chassi": dados_base_estadual.especificacoes.situacao_chassi,
                        "Espécie": dados_base_estadual.especificacoes.especie,
                        "Carroceria": dados_base_estadual.especificacoes.carroceria,
                        "Potência": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.potencia
                        ),
                        "Município": dados_base_estadual.dados_veiculo.municipio,
                        "Nº Motor": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.motor
                        ),
                        "Procedência do Veículo": dados_base_estadual.especificacoes.procedencia,
                        "Capacidade de Carga": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.carga
                        ),
                        "Capacidade de Passageiros": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.passageiros
                        ),
                        "Nº Carroceria": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.num_carroceria
                        ),
                        "Nº Caixa de Câmbio": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.cambio
                        ),
                        "Nº Eixos": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.eixos
                        ),
                        "Terceiro Eixo": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.terceiro_eixo
                        ),
                        "Eixo Traseiro Diferencial": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.eixo_traseiro
                        ),
                        "Montagem": montagem,
                        "CMT": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.cmt
                        ),
                        "PBT": convert.from_int_to_string(
                            dados_base_estadual.especificacoes.pbt
                        ),
                        "Observações Gerais": dados_base_estadual.solicitacao.mensagem_extenso,
                    }

                    temp_list.append(append_data)

                    logger.info("Registro adicionado à planilha de saída com sucesso")
                except Exception as error:
                    temp_list.append(
                        {
                            "Placa (colocar apenas a placa e qual UF está registrada) (SEMPRE MAIUSCULA - EX.: XXX1234 (UF))": str(
                                placa
                            ).upper(),
                            "Chassi (SEMPRE MAIUSCULA)": str(chassi).upper(),
                            "Observações Gerais": f"{error}",
                        }
                    )
                    logger.info(
                        "Registro adicionado à planilha de saída descrevendo erro encontrado durante o processamento"
                    )

        df = pandas.DataFrame(temp_list, columns=df_columns)
        writer = pandas.ExcelWriter(
            file.replace("input", "output/xlsx"), engine="xlsxwriter"
        )
        df.to_excel(writer, sheet_name="Listagem", index=False)
        writer.close()

    def plataforma_gestor(self, file):
        data = pandas.read_excel(file)

        temp_list = []
        df_columns = [
            "Proprietário/CNPJ (Proprietário do documento)",
            "Restrições",
            "Débitos (Total)",
            "Tipo",
            "Marca",
            "Modelo",
            "Ano Fabricação",
            "Ano Modelo",
            "Placa",
            "UF",
            "Chassi",
            "Renavam",
            "Cor",
            "Tipo Combustível",
            "Origem",
            "Valor Tabela FIPE",
            "Chave de Ignição",
            "Tipo de Câmbio",
            "KM",
            "Motor",
            "Câmbio",
            "Pintura",
            "Lataria",
            "Tapeçaria / Forração",
            "Pneus",
            "Eixos",
            "Tração",
            "Primeiro Cardan",
            "Segundo Cardan",
            "Primeiro Diferencial",
            "Segundo Diferencial",
            "Quinta Roda",
            "Quantidade de Pneus",
            "Bancos",
            "Chassi Oxidado",
            "Chassi Remarcado",
            "Tipo de Carroceria",
            "Estado da Carroceria",
            "Comprimento (m)",
            "Largura (m)",
            "Altura (m)",
            "PBT (kg)",
            "CMT (kg)",
            "Dimesões dos Pneus",
            "Tacógrafo",
            "Pneu Estepe",
            "Ferramentas Obrigatórias",
            "Rodoar",
            "Grade",
            "Parabrisa",
            "Capô",
            "Parachoque Dianteiro",
            "Farol Direito",
            "Lanterna Dianteira Direita",
            "Farol Esquerdo",
            "Lanterna Dianteira Esquerda",
            "Paralama Direito",
            "Retrovisor Direito",
            "Porta Direita",
            "Lanterna Traseira Direita",
            "Lanterna Traseira Esquerda",
            "Parachoque Traseiro",
            "Vidro Traseiro",
            "Porta Esquerda",
            "Retrovisor Esquerdo",
            "Paralama Esquerdo",
            "Painel de Instrumentos",
            "Bancos",
            "Teto",
            "Longarina",
            "Bateria",
            "Total",
            "Observações",
            "Número de Portas",
            "Cep de Origem",
            "Número (Processo)",
            "Ano (Processo)",
            "Tipo (Processo)",
            "Natureza (Processo)",
            "Fórum (Processo)",
            "Comarca (Processo)",
            "Juíz (Processo)",
            "Autor (Processo)",
            "Réu (Processo)",
            "Advogados (Processo)",
            "Depositário (Processo)",
            "Recurso (Processo)",
            "Link (Processo)",
        ]

        for idx, v in enumerate(data["Placa"]):
            check_fipe = False

            placa = (
                data["Placa"]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )
            chassi = (
                data["Chassi"]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )
            fipe = (
                data["Consultar Tabela Fipe?"]
                .fillna("NULL")
                .values[idx]
                .upper()
                .replace(" ", "")
                .strip()
            )

            if placa == "NULL":
                placa = ""

            if chassi == "NULL":
                chassi = ""

            if fipe == "S" or fipe == "SIM" or fipe == "Y" or fipe == "YES":
                check_fipe = True

            logger.info("Lendo registro da planilha de entrada:")
            logger.info(f'--> Placa: "{placa}"')
            logger.info(f'--> Chassi: "{chassi}"')
            logger.info(f'--> Consultar Tabela Fipe? "{fipe}"')

            if placa != "" or chassi != "":
                try:
                    dados_base_estadual = None
                    if placa != "":
                        dados_base_estadual = base_estadual.request_by_placa(placa)
                        logger.debug(
                            f"Dados Base Estadual:{dados_base_estadual.to_string()}"
                        )
                    elif chassi != "":
                        dados_base_estadual = base_estadual.request_by_chassi(chassi)
                        logger.debug(
                            f"Dados Base Estadual:{dados_base_estadual.to_string()}"
                        )
                    else:
                        raise Exception(
                            "É necessário informar ou placa ou chassi para acessar a base estadual"
                        )

                    dados_precificador = None
                    if check_fipe and placa != "":
                        dados_precificador = codificador_fipe.request_by_placa(placa)
                        logger.debug(
                            f"Dados Precificador:{dados_precificador.to_string()}"
                        )
                    elif check_fipe and chassi != "":
                        dados_precificador = codificador_fipe.request_by_chassi(chassi)
                        logger.debug(
                            f"Dados Precificador:{dados_precificador.to_string()}"
                        )
                    else:
                        logger.info(
                            "Usuário optou por não consultar os dados do Precificador para esse registro"
                        )

                    restricoes_concatenadas = ""
                    if dados_base_estadual is not None:
                        if len(dados_base_estadual.restricoes.restricoes) > 0:
                            for restricao in dados_base_estadual.restricoes.restricoes:
                                if restricoes_concatenadas == "":
                                    restricoes_concatenadas = restricao
                                else:
                                    restricoes_concatenadas = (
                                        restricoes_concatenadas + ", " + restricao
                                    )

                    total_multas = 0
                    try:
                        total_multas = (
                            dados_base_estadual.debitos.debitos_dpvat
                            + dados_base_estadual.debitos.debitos_ipva
                            + dados_base_estadual.debitos.debitos_licenciamento
                            + dados_base_estadual.debitos.debitos_multas
                        )
                    except Exception:
                        total_multas = 0

                    tabelas_fipes_concatenadas = ""
                    if check_fipe and dados_precificador is not None:
                        if len(dados_precificador.tabelas_fipe.valores) > 0:
                            for valor in dados_precificador.tabelas_fipe.valores:
                                if tabelas_fipes_concatenadas == "":
                                    tabelas_fipes_concatenadas = (
                                        "R$ " + convert.from_float_to_string(valor, 2)
                                    )
                                else:
                                    tabelas_fipes_concatenadas = (
                                        tabelas_fipes_concatenadas
                                        + " / "
                                        + "R$ "
                                        + convert.from_float_to_string(valor, 2)
                                    )

                    montagem = ""
                    if check_fipe and dados_precificador is not None:
                        montagem = dados_precificador.dados_veiculo.tipo_montagem

                    logger.debug(f"Restrições concatenadas: {restricoes_concatenadas}")
                    logger.debug(
                        f"Total de multas: {convert.from_float_to_string(total_multas, 2)}"
                    )
                    logger.debug(
                        f"Tabelas FIPE concatenadas: {tabelas_fipes_concatenadas}"
                    )
                    logger.debug(f"Montagem: {montagem}")

                    append_data = {
                        "Proprietário/CNPJ (Proprietário do documento)": dados_base_estadual.proprietario.nome
                        + " / "
                        + dados_base_estadual.proprietario.documento,
                        "Restrições": restricoes_concatenadas,
                        "Débitos (Total)": convert.from_float_to_string(
                            total_multas, 2
                        ),
                        "Tipo": dados_base_estadual.dados_veiculo.tipo_veiculo,
                        "Marca": dados_base_estadual.dados_veiculo.modelo,
                        "Modelo": dados_base_estadual.dados_veiculo.modelo,
                        "Ano Fabricação": convert.from_int_to_string(
                            dados_base_estadual.dados_veiculo.ano_fabricacao
                        ),
                        "Ano Modelo": convert.from_int_to_string(
                            dados_base_estadual.dados_veiculo.ano_modelo
                        ),
                        "Placa": dados_base_estadual.dados_veiculo.placa,
                        "UF": dados_base_estadual.dados_veiculo.uf_emplacado,
                        "Chassi": dados_base_estadual.dados_veiculo.chassi,
                        "Renavam": dados_base_estadual.dados_veiculo.renavam,
                        "Cor": dados_base_estadual.dados_veiculo.cor,
                        "Tipo Combustível": dados_base_estadual.dados_veiculo.combustivel,
                        "Origem": "Script Python Infocar",
                        "Valor Tabela FIPE": tabelas_fipes_concatenadas,
                        "Chave de Ignição": "",
                        "Tipo de Câmbio": "",
                        "KM": "",
                        "Motor": dados_base_estadual.especificacoes.motor,
                        "Câmbio": dados_base_estadual.especificacoes.cambio,
                        "Pintura": dados_base_estadual.dados_veiculo.cor,
                        "Lataria": dados_base_estadual.dados_veiculo.cor,
                        "Tapeçaria / Forração": "",
                        "Pneus": "",
                        "Eixos": dados_base_estadual.especificacoes.eixos,
                        "Tração": "",
                        "Primeiro Cardan": "",
                        "Segundo Cardan": "",
                        "Primeiro Diferencial": "",
                        "Segundo Diferencial": dados_base_estadual.especificacoes.eixo_traseiro,
                        "Quinta Roda": "",
                        "Quantidade de Pneus": "",
                        "Bancos": "",
                        "Chassi Oxidado": "",
                        "Chassi Remarcado": dados_base_estadual.especificacoes.situacao_chassi,
                        "Tipo de Carroceria": dados_base_estadual.especificacoes.carroceria
                        + " "
                        + dados_base_estadual.especificacoes.num_carroceria,
                        "Estado da Carroceria": "",
                        "Comprimento (m)": "",
                        "Largura (m)": "",
                        "Altura (m)": "",
                        "PBT (kg)": dados_base_estadual.especificacoes.pbt,
                        "CMT (kg)": dados_base_estadual.especificacoes.cmt,
                        "Dimesões dos Pneus": "",
                        "Tacógrafo": "",
                        "Pneu Estepe": "",
                        "Ferramentas Obrigatórias": "",
                        "Rodoar": "",
                        "Grade": "",
                        "Parabrisa": "",
                        "Capô": "",
                        "Parachoque Dianteiro": "",
                        "Farol Direito": "",
                        "Lanterna Dianteira Direita": "",
                        "Farol Esquerdo": "",
                        "Lanterna Dianteira Esquerda": "",
                        "Paralama Direito": "",
                        "Retrovisor Direito": "",
                        "Porta Direita": "",
                        "Lanterna Traseira Direita": "",
                        "Lanterna Traseira Esquerda": "",
                        "Parachoque Traseiro": "",
                        "Vidro Traseiro": "",
                        "Porta Esquerda": "",
                        "Retrovisor Esquerdo": "",
                        "Paralama Esquerdo": "",
                        "Painel de Instrumentos": "",
                        "Bancos": "",
                        "Teto": "",
                        "Longarina": "",
                        "Bateria": "",
                        "Total": "",
                        "Observações": dados_base_estadual.solicitacao.mensagem_extenso,
                        "Número de Portas": "",
                        "Cep de Origem": "",
                        "Número (Processo)": "",
                        "Ano (Processo)": "",
                        "Tipo (Processo)": "",
                        "Natureza (Processo)": "",
                        "Fórum (Processo)": "",
                        "Comarca (Processo)": "",
                        "Juíz (Processo)": "",
                        "Autor (Processo)": "",
                        "Réu (Processo)": "",
                        "Advogados (Processo)": "",
                        "Depositário (Processo)": "",
                        "Recurso (Processo)": "",
                        "Link (Processo)": "",
                    }

                    temp_list.append(append_data)

                    logger.info("Registro adicionado à planilha de saída com sucesso")
                except Exception as error:
                    temp_list.append(
                        {
                            "Placa": str(placa).upper(),
                            "Chassi": str(chassi).upper(),
                            "Observações": f"{error}",
                        }
                    )
                    logger.info(
                        "Registro adicionado à planilha de saída descrevendo erro encontrado durante o processamento"
                    )

        df = pandas.DataFrame(temp_list, columns=df_columns)
        writer = pandas.ExcelWriter(
            file.replace("input", "output/xlsx"), engine="xlsxwriter"
        )
        df.to_excel(writer, sheet_name="Listagem", index=False)
        writer.close()


if __name__ == "__main__":
    try:
        dados_extrato = extrato.request_extrato()
        while True:
            print(
                f"Já foram feitas {dados_extrato.resposta.quantidade} requisições para a API da Infocar nesse mês"
            )
            print("Deseja continuar?")
            print("S - Sim")
            print("N - Não")

            option_selected = input()

            if option_selected.upper() == "N":
                print("Finalizando a execução do script")
                exit()
            elif option_selected.upper() == "S":
                break
            else:
                print("Opção inválida. Tente novamente")

        while True:
            print("Qual o formato que você quer gerar a planilha de saída?")
            print("1 - Formato legado (Planilha colunada)")
            print("2 - Formato novo (Plataforma gestor)")

            output_format = input()

            if output_format.upper() == "1" or output_format.upper() == "2":
                break
            else:
                print("Opção inválida. Tente novamente")

        logger.info("Iniciando a conversão")
        infocarConverter = InfocarConverter(
            ".",
            ["input"],
            ["output", os.path.join("output", "xlsx")],
            os.path.join("output", "xlsx", "resulting_spreadsheet.xlsx"),
        )
        infocarConverter.execute(output_format)

        logger.info("Conversão finalizada com sucesso")
        done = str(input("Pressione ENTER para encerrar..."))
    except Exception as error:
        logger.error(f'Ocorreu o erro "{error}" no processamento da planilha')
