import utils
import requests
import xml.etree.ElementTree as ET
from services.base.logger import Logger
from datetime import date, timedelta

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
    yesterday = date.today() - timedelta(days=1)

    url = get_url()
    headers = get_headers()
    key = get_key()
    body = get_body(
        endpoint,
        yesterday.strftime("%d"),
        yesterday.strftime("%m"),
        yesterday.strftime("%Y"),
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


def get_body(endpoint, dia, mes, ano, key):
    return f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <Extrato xmlns="http://tempuri.org/">
                <ano>2023</ano>
                <mes>05</mes>
                <dia>18</dia>
                <chave>alI0RkoxU3c6S2I0amw4eVg=</chave>
            </Extrato>
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

        self.solicitacao = Solicitacao(solicitacao_tag)
        self.resposta = Resposta(resposta_tag)

    def to_string(self):
        logger.debug(f"""{self.solicitacao.to_string()}{self.resposta.to_string()}""")


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

        self.dado = utils.to_date(dado)
        self.numero_resposta = utils.to_string(numero_resposta)
        self.tempo = utils.to_float(tempo, "US")
        self.mensagem = utils.to_string(mensagem_extenso)
        self.horario = utils.to_datetime(horario)

    def to_string(self):
        return f"""\nSOLICITACAO:\n* Dado: {utils.from_date_to_string(self.dado)}\n* Número Resposta: {self.numero_resposta}\n* Tempo: {utils.from_float_to_string(self.tempo, 4)}\n* Mensagem: {self.mensagem}\n* Horário: {utils.from_datetime_to_string(self.horario)}"""


class Resposta:
    def __init__(self, resposta_tag):
        usuario = resposta_tag.find("USUARIO").text
        data = resposta_tag.find("DATA").text
        quantidade = resposta_tag.find("QTD").text
        link = resposta_tag.find("LINK").text

        self.usuario = utils.to_string(usuario)
        self.data = utils.to_date(data)
        self.quantidade = utils.to_int(quantidade)
        self.link = utils.to_string(link)

    def to_string(self):
        return f"""\nRESPOSTA:\n* Usuário: {self.usuario}\n* Data: {utils.from_date_to_string(self.data)}\n* Tempo: {utils.from_int_to_string(self.quantidade)}\n* Link: {self.link}"""
