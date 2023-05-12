import common


CONST_BASE_ESTADUAL = "BaseEstadual_B"


def request_by_chassi(chassi):
    return common.request_endpoint(CONST_BASE_ESTADUAL, None, chassi)


def request_by_placa(placa):
    return common.request_endpoint(CONST_BASE_ESTADUAL, placa, None)
