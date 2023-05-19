import utils
import common
import xml.etree.ElementTree as ET
from services.base.logger import Logger

logger = Logger.__call__().get_logger()

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

        self.solicitacao = Solicitacao(solicitacao_tag)
        self.dados_veiculo = DadosVeiculo(dados_veiculo_tag)
        self.tabelas_fipe = Precificadores(tabelas_fipe_tag)

    def to_string(self):
        logger.debug(
            f"{self.solicitacao.to_string()}{self.dados_veiculo.to_string()}{self.tabelas_fipe.to_string()}"
        )


class Solicitacao:
    def __init__(self, solicitacao_tag):
        dado = solicitacao_tag.find("DADO").text
        numero_resposta = solicitacao_tag.find("NUMERO_RESPOSTA").text
        tempo = solicitacao_tag.find("TEMPO").text
        mensagem = solicitacao_tag.find("MENSAGEM").text
        horario = solicitacao_tag.find("HORARIO").text

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

        self.dado = utils.to_string(dado)
        self.numero_resposta = utils.to_string(numero_resposta)
        self.tempo = utils.to_float(tempo, "US")
        self.mensagem = utils.to_string(mensagem_extenso)
        self.horario = utils.to_datetime(horario)

    def to_string(self):
        return f"\nSOLICITACAO:\n* Dado: {self.dado}\n* Número Resposta: {self.numero_resposta}\n* Tempo: {utils.from_float_to_string(self.tempo,4)}\n* Mensagem: {self.mensagem}\n* Horário: {utils.from_datetime_to_string(self.horario)}"


class DadosVeiculo:
    def __init__(self, dados_veiculo_tag):
        procedencia = dados_veiculo_tag.find("PROCEDENCIA").text
        municipio = dados_veiculo_tag.find("MUNICIPIO").text
        uf = dados_veiculo_tag.find("UF").text
        placa = dados_veiculo_tag.find("PLACA").text
        chassi = dados_veiculo_tag.find("CHASSI").text
        situacao_chassi = dados_veiculo_tag.find("SITUACAO_DO_CHASSI").text
        marca_modelo = dados_veiculo_tag.find("MARCA_MODELO").text
        ano = dados_veiculo_tag.find("ANO").text
        capacidade_carga = dados_veiculo_tag.find("CAPACIDADE_DE_CARGA").text
        combustivel = dados_veiculo_tag.find("COMBUSTIVEL").text
        cor = dados_veiculo_tag.find("COR").text
        potencia = dados_veiculo_tag.find("POTENCIA").text
        cilindradas = dados_veiculo_tag.find("CILINDRADAS").text
        max_passageiros = dados_veiculo_tag.find("QUANTIDADE_PASSAGEIRO").text
        tipo_montagem = dados_veiculo_tag.find("TIPO_MONTAGEM").text
        eixos = dados_veiculo_tag.find("QUANTIDADE_DE_EIXOS").text
        pbt = dados_veiculo_tag.find("PBT").text
        cmt = dados_veiculo_tag.find("CMT").text
        tipo_veiculo = dados_veiculo_tag.find("TIPO_DE_VEICULO").text
        tipo_carroceria = dados_veiculo_tag.find("TIPO_CARROCERIA").text
        motor = dados_veiculo_tag.find("N_MOTOR").text
        cambio = dados_veiculo_tag.find("CAIXA_CAMBIO").text
        eixo_traseiro = dados_veiculo_tag.find("EIXO_TRASEIRO_DIF").text
        carroceria = dados_veiculo_tag.find("CARROCERIA").text

        self.procedencia = utils.to_string(procedencia)
        self.municipio = utils.to_string(municipio)
        self.uf = utils.to_string(uf)
        self.placa = utils.to_string(placa)
        self.chassi = utils.to_string(chassi)
        self.situacao_chassi = utils.to_string(situacao_chassi)
        self.marca_modelo = utils.to_string(marca_modelo)
        self.ano = utils.to_string(ano)
        self.capacidade_carga = utils.to_string(capacidade_carga)
        self.combustivel = utils.to_string(combustivel)
        self.cor = utils.to_string(cor)
        self.potencia = utils.to_string(potencia)
        self.cilindradas = utils.to_string(cilindradas)
        self.max_passageiros = utils.to_string(max_passageiros)
        self.tipo_montagem = utils.to_string(tipo_montagem)
        self.eixos = utils.to_string(eixos)
        self.pbt = utils.to_string(pbt)
        self.cmt = utils.to_string(cmt)
        self.tipo_veiculo = utils.to_string(tipo_veiculo)
        self.tipo_carroceria = utils.to_string(tipo_carroceria)
        self.motor = utils.to_string(motor)
        self.cambio = utils.to_string(cambio)
        self.eixo_traseiro = utils.to_string(eixo_traseiro)
        self.carroceria = utils.to_string(carroceria)

    def to_string(self):
        return f"\nDADOS VEICULO:\n* Procedência: {self.procedencia}\n* Município: {self.municipio}\n* UF: {self.uf}\n* Placa: {self.placa}\n* Chassi: {self.chassi}\n* Situação do Chassi: {self.situacao_chassi}\n* Marca/Modelo: {self.marca_modelo}\n* Ano: {self.ano}\n* Capacidade de Carga: {self.capacidade_carga}\n* Combustível: {self.combustivel}\n* Cor: {self.cor}\n* Potência: {self.potencia}\n* Cilindradas: {self.cilindradas}\n* Máximo de Passageiros: {self.max_passageiros}\n* Tipo de Montagem: {self.tipo_montagem}\n* Eixos: {self.eixos}\n* PBT: {self.pbt}\n* CMT: {self.cmt}\n* Tipo Veículo: {self.tipo_veiculo}\n* Tipo Carroceria: {self.tipo_carroceria}\n* Motor: {self.motor}\n* Câmbio: {self.cambio}\n* Eixo Traseiro: {self.eixo_traseiro}\n* Carroceria: {self.carroceria}"


class Precificadores:
    def __init__(self, tabelas_fipe_tag):
        valores_tabela_fipe = []
        for tabela_fipe_tag in tabelas_fipe_tag:
            for child in tabela_fipe_tag:
                valor_fipe = utils.to_float(child.find("VALOR").text, "US")
                valores_tabela_fipe.append(valor_fipe)

        self.tabelas_fipe = valores_tabela_fipe

    def to_string(self):
        string = f"\nTABELAS FIPE:"

        if len(self.tabelas_fipe) == 0:
            string = string + f"\n* Nenhuma tabela FIPE encontrada"
        else:
            for tabela_fipe in self.tabelas_fipe:
                string = (
                    string + f"\n* Valor: {utils.from_float_to_string(tabela_fipe, 2)}"
                )

        return string
