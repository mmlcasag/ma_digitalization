import common
import convert
import requests
import xml.etree.ElementTree as ET
from services.base.logger import Logger
from datetime import date

logger = Logger.__call__().get_logger()

CONST_EXTRATO = "Extrato"


def request_extrato():
    infocar_response = request_endpoint(CONST_EXTRATO)
    return Extrato(infocar_response)


def request_endpoint(endpoint):
    try:
        logger.info(f"Requisitando o endpoint {endpoint}")
        for i in range(5):
            try:
                logger.info(f"Tentativa {(i + 1)}/5")

                return make_request(endpoint)
            except requests.exceptions.Timeout:
                logger.warning("Ocorreu timeout")

                if (i + 1) == 5:
                    raise Exception("Atingiu o limite de tentativas")
            except Exception:
                raise
    except Exception as error:
        logger.error(error)


def make_request(endpoint):
    today = date.today()

    url = get_url()
    headers = get_headers()
    key = get_key()
    body = get_body(
        endpoint,
        today.strftime("%m"),
        today.strftime("%Y"),
        key,
    )

    response = requests.post(url, data=body, headers=headers, timeout=30)

    return response.content


def get_url():
    return "http://datacast3.com/WebService/servico.asmx"


def get_headers():
    return {
        "Host": "datacast3.com",
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/Extrato",
    }


def get_key():
    return "alI0RkoxU3c6S2I0amw4eVg="


def get_body(endpoint, mes, ano, key):
    return f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <{endpoint} xmlns="http://tempuri.org/">
                <ano>{ano}</ano>
                <mes>{mes}</mes>
                <chave>{key}</chave>
            </{endpoint}>
        </soap:Body>
    </soap:Envelope>"""


class Extrato:
    def __init__(self, infocar_response):
        self.solicitacao = None
        self.resposta = None

        solicitacao_tag = None
        resposta_tag = None

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

        if solicitacao_tag is not None:
            self.solicitacao = Solicitacao(solicitacao_tag)
        if self.solicitacao.mensagem != "1":
            raise Exception(
                f"Erro na resposta da Infocar: {self.solicitacao.mensagem_extenso}"
            )
        if resposta_tag is not None:
            self.resposta = Resposta(resposta_tag)

    def to_string(self):
        return f"{self.solicitacao.to_string()}{self.resposta.to_string()}"


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
        return f"""\nSOLICITACAO:\n* Dado: {self.dado}\n* Número Resposta: {self.numero_resposta}\n* Tempo: {convert.from_float_to_string(self.tempo, 4)}\n* Mensagem: {self.mensagem}\n* Mensagem Extenso: {self.mensagem_extenso}\n* Horário: {convert.from_datetime_to_string(self.horario)}"""


class Resposta:
    def __init__(self, resposta_tag):
        today = date.today()
        quantidade = 0

        for child in resposta_tag:
            if child.tag == "USUARIO":
                usuario = child.text
            if child.tag == "QTD":
                quantidade += convert.to_int(child.text)

        self.usuario = convert.to_string(usuario)
        self.mes = convert.to_string(today.strftime("%m/%Y"))
        self.quantidade = quantidade

    def to_string(self):
        return f"""\nRESPOSTA:\n* Usuário: {self.usuario}\n* Mês: {self.mes}\n* Quantidade: {convert.from_int_to_string(self.quantidade)}"""
