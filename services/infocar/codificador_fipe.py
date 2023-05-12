import common


CONST_CODIFICADOR_FIPE = "CodificacaoFIPE_V2"


def request_by_chassi(chassi):
    return common.request_endpoint(CONST_CODIFICADOR_FIPE, None, chassi)


def request_by_placa(placa):
    return common.request_endpoint(CONST_CODIFICADOR_FIPE, placa, None)
