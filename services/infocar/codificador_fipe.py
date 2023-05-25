import common
import convert
import xml.etree.ElementTree as ET


CONST_CODIFICADOR_FIPE = "CodificacaoFIPE_V2"


def request_by_chassi(chassi):
    infocar_response = common.request_endpoint(CONST_CODIFICADOR_FIPE, None, chassi)
    return CodificadorFipe(infocar_response)


def request_by_placa(placa):
    infocar_response = common.request_endpoint(CONST_CODIFICADOR_FIPE, placa, None)
    return CodificadorFipe(infocar_response)


class CodificadorFipe:
    def __init__(self, infocar_response):
        self.solicitacao = None
        self.dados_veiculo = None
        self.tabelas_fipe = None

        solicitacao_tag = None
        resposta_tag = None
        dados_veiculo_tag = None
        precificadores_tag = None
        tabelas_fipe_tag = None

        envelope_tag = ET.fromstring(infocar_response)
        for body_tag in envelope_tag:
            for response_tag in body_tag:
                for result_tag in response_tag:
                    for info_xml_tag in result_tag:
                        for child in info_xml_tag:
                            if child.tag == "SOLICITACAO":
                                solicitacao_tag = child
                            if child.tag == "RESPOSTA":
                                resposta_tag = child

        for infocar_codificacao_tag in resposta_tag:
            for child in infocar_codificacao_tag:
                if child.tag == "DADOS_DO_VEICULO":
                    dados_veiculo_tag = child
                if child.tag == "PRECIFICADORES":
                    precificadores_tag = child

        for precificador_tag in precificadores_tag:
            if precificador_tag.tag == "FIPES":
                tabelas_fipe_tag = child

        if solicitacao_tag is not None:
            self.solicitacao = Solicitacao(solicitacao_tag)
        if self.solicitacao.mensagem != "1":
            raise Exception(
                f"Erro na resposta da Infocar: {self.solicitacao.mensagem_extenso}"
            )
        if dados_veiculo_tag is not None:
            self.dados_veiculo = DadosVeiculo(dados_veiculo_tag)
        if tabelas_fipe_tag is not None:
            self.tabelas_fipe = Precificadores(tabelas_fipe_tag)

    def to_string(self):
        return f"{self.solicitacao.to_string()}{self.dados_veiculo.to_string()}{self.tabelas_fipe.to_string()}"


class Solicitacao:
    def __init__(self, solicitacao_tag):
        dado = common.find_element(solicitacao_tag, "DADO")
        numero_resposta = common.find_element(solicitacao_tag, "NUMERO_RESPOSTA")
        tempo = common.find_element(solicitacao_tag, "TEMPO")
        mensagem = common.find_element(solicitacao_tag, "MENSAGEM")
        horario = common.find_element(solicitacao_tag, "HORARIO")

        mensagem_extenso = ""
        match (int(mensagem)):
            case 0:
                mensagem_extenso = "Não Possui Registro"
            case 1:
                mensagem_extenso = "Possui Registro"
            case 2:
                mensagem_extenso = "Falha de Autenticação"
            case 3:
                mensagem_extenso = "Dado/Tipo Incorreto"
            case 4:
                mensagem_extenso = "Erro na Pesquisa/Sistema Indisponível"
            case 5:
                mensagem_extenso = "Limite Diário Excedido"
            case _:
                mensagem_extenso = "Erro Desconhecido"

        self.dado = convert.to_string(dado)
        self.numero_resposta = convert.to_string(numero_resposta)
        self.tempo = convert.to_float(tempo, "US")
        self.mensagem = convert.to_string(mensagem)
        self.mensagem_extenso = convert.to_string(mensagem_extenso)
        self.horario = convert.to_datetime(horario)

    def to_string(self):
        return f"\nSOLICITACAO:\n* Dado: {self.dado}\n* Número Resposta: {self.numero_resposta}\n* Tempo: {convert.from_float_to_string(self.tempo,4)}\n* Mensagem: {self.mensagem}\n* Mensagem Extenso: {self.mensagem_extenso}\n* Horário: {convert.from_datetime_to_string(self.horario)}"


class DadosVeiculo:
    def __init__(self, dados_veiculo_tag):
        procedencia = common.find_element(dados_veiculo_tag, "PROCEDENCIA")
        municipio = common.find_element(dados_veiculo_tag, "MUNICIPIO")
        uf = common.find_element(dados_veiculo_tag, "UF")
        placa = common.find_element(dados_veiculo_tag, "PLACA")
        chassi = common.find_element(dados_veiculo_tag, "CHASSI")
        situacao_chassi = common.find_element(dados_veiculo_tag, "SITUACAO_DO_CHASSI")
        marca_modelo = common.find_element(dados_veiculo_tag, "MARCA_MODELO")
        ano = common.find_element(dados_veiculo_tag, "ANO")
        capacidade_carga = common.find_element(dados_veiculo_tag, "CAPACIDADE_DE_CARGA")
        combustivel = common.find_element(dados_veiculo_tag, "COMBUSTIVEL")
        cor = common.find_element(dados_veiculo_tag, "COR")
        potencia = common.find_element(dados_veiculo_tag, "POTENCIA")
        cilindradas = common.find_element(dados_veiculo_tag, "CILINDRADAS")
        max_passageiros = common.find_element(
            dados_veiculo_tag, "QUANTIDADE_PASSAGEIRO"
        )
        tipo_montagem = common.find_element(dados_veiculo_tag, "TIPO_MONTAGEM")
        eixos = common.find_element(dados_veiculo_tag, "QUANTIDADE_DE_EIXOS")
        pbt = common.find_element(dados_veiculo_tag, "PBT")
        cmt = common.find_element(dados_veiculo_tag, "CMT")
        tipo_veiculo = common.find_element(dados_veiculo_tag, "TIPO_DE_VEICULO")
        tipo_carroceria = common.find_element(dados_veiculo_tag, "TIPO_CARROCERIA")
        motor = common.find_element(dados_veiculo_tag, "N_MOTOR")
        cambio = common.find_element(dados_veiculo_tag, "CAIXA_CAMBIO")
        eixo_traseiro = common.find_element(dados_veiculo_tag, "EIXO_TRASEIRO_DIF")
        carroceria = common.find_element(dados_veiculo_tag, "CARROCERIA")

        self.procedencia = convert.to_string(procedencia)
        self.municipio = convert.to_string(municipio)
        self.uf = convert.to_string(uf)
        self.placa = convert.to_string(placa)
        self.chassi = convert.to_string(chassi)
        self.situacao_chassi = convert.to_string(situacao_chassi)
        self.marca_modelo = convert.to_string(marca_modelo)
        self.ano = convert.to_string(ano)
        self.capacidade_carga = convert.to_int(capacidade_carga)
        self.combustivel = convert.to_string(combustivel)
        self.cor = convert.to_string(cor)
        self.potencia = convert.to_int(potencia)
        self.cilindradas = convert.to_int(cilindradas)
        self.max_passageiros = convert.to_int(max_passageiros)
        self.tipo_montagem = convert.to_string(tipo_montagem)
        self.eixos = convert.to_int(eixos)
        self.pbt = convert.to_int(pbt)
        self.cmt = convert.to_int(cmt)
        self.tipo_veiculo = convert.to_string(tipo_veiculo)
        self.tipo_carroceria = convert.to_string(tipo_carroceria)
        self.motor = convert.to_string(motor)
        self.cambio = convert.to_string(cambio)
        self.eixo_traseiro = convert.to_string(eixo_traseiro)
        self.carroceria = convert.to_string(carroceria)

    def to_string(self):
        return f"\nDADOS VEICULO:\n* Procedência: {self.procedencia}\n* Município: {self.municipio}\n* UF: {self.uf}\n* Placa: {self.placa}\n* Chassi: {self.chassi}\n* Situação do Chassi: {self.situacao_chassi}\n* Marca/Modelo: {self.marca_modelo}\n* Ano: {self.ano}\n* Capacidade de Carga: {convert.from_int_to_string(self.capacidade_carga)}\n* Combustível: {self.combustivel}\n* Cor: {self.cor}\n* Potência: {convert.from_int_to_string(self.potencia)}\n* Cilindradas: {convert.from_int_to_string(self.cilindradas)}\n* Máximo de Passageiros: {convert.from_int_to_string(self.max_passageiros)}\n* Tipo de Montagem: {self.tipo_montagem}\n* Eixos: {convert.from_int_to_string(self.eixos)}\n* PBT: {convert.from_int_to_string(self.pbt)}\n* CMT: {convert.from_int_to_string(self.cmt)}\n* Tipo Veículo: {self.tipo_veiculo}\n* Tipo Carroceria: {self.tipo_carroceria}\n* Motor: {self.motor}\n* Câmbio: {self.cambio}\n* Eixo Traseiro: {self.eixo_traseiro}\n* Carroceria: {self.carroceria}"


class Precificadores:
    def __init__(self, tabelas_fipe_tag):
        codigos = []
        marcas_modelos = []
        valores = []
        for tabela_fipe_tag in tabelas_fipe_tag:
            for child in tabela_fipe_tag:
                codigo = convert.to_string(common.find_element(child, "CODIGO"))
                marca_modelo = convert.to_string(
                    common.find_element(child, "MARCA_MODELO")
                )
                valor = convert.to_float(common.find_element(child, "VALOR"), "US")

                codigos.append(codigo)
                marcas_modelos.append(marca_modelo)
                valores.append(valor)

        self.codigos = codigos
        self.marcas_modelos = marcas_modelos
        self.valores = valores

    def to_string(self):
        string = f"\nTABELAS FIPE:"

        if len(self.codigos) == 0:
            string = string + f"\n* Nenhuma tabela FIPE encontrada"
        else:
            for i in range(len(self.codigos)):
                string = (
                    string
                    + f"\n  * Tabela {i+1}\n    * Código: {self.codigos[i]}\n    * Marca/Modelo: {self.marcas_modelos[i]}\n    * Valor: {convert.from_float_to_string(self.valores[i], 2)}"
                )

        return string
