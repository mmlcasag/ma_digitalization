import requests


from services.base.logger import Logger


logger = Logger.__call__().get_logger()


def request_endpoint(endpoint, placa, chassi):
    data = get_data(placa, chassi)
    type = get_type(placa, chassi)

    try:
        logger.info(f"Requisitando o endpoint {endpoint} com {type}: {data}")
        for i in range(5):
            try:
                logger.info(f"Tentativa {(i + 1)}/5")

                return make_request(endpoint, data, type)
            except requests.exceptions.Timeout:
                logger.warning("Ocorreu timeout")

                if (i + 1) == 5:
                    raise Exception("Atingiu o limite de tentativas")
            except Exception:
                raise
    except Exception as error:
        logger.error(error)


def make_request(endpoint, data, type):
    url = get_url()
    headers = get_headers()
    key = get_key()
    body = get_body(endpoint, data, type, key)

    response = requests.post(url, data=body, headers=headers, timeout=30)

    return response.content


def get_url():
    return "http://datacast3.com/WebService/servico.asmx"


def get_headers():
    return {"Content-Type": "text/xml; charset=utf-8"}


def get_data(placa, chassi):
    if placa is None and chassi is None:
        raise Exception("É necessário informar ou placa ou chassi")

    if placa is not None and chassi is None:
        return placa

    if placa is None and chassi is not None:
        return chassi

    if placa is not None and chassi is not None:
        raise Exception("É necessário informar ou placa ou chassi")


def get_type(placa, chassi):
    if placa is None and chassi is None:
        raise Exception("É necessário informar ou placa ou chassi")

    if placa is not None and chassi is None:
        return "PLACA"

    if placa is None and chassi is not None:
        return "CHASSI"

    if placa is not None and chassi is not None:
        raise Exception("É necessário informar ou placa ou chassi")


def get_key():
    return "alI0RkoxU3c6S2I0amw4eVg="


def get_body(endpoint, data, type, key):
    return f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <{endpoint} xmlns="http://tempuri.org/">
                <dado>{data}</dado>
                <tipo>{type}</tipo>
                <chave>{key}</chave>
            </{endpoint}>
        </soap:Body>
    </soap:Envelope>"""
