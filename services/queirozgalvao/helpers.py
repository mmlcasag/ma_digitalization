import utils.ma as ma_utils


def is_veiculo(registro):
    categorias_especiais = ["Veículos", "Caminhões", "Ônibus", "Guindastes"]

    if registro["categoria"] in categorias_especiais and len(registro["placa"]) > 0:
        return True

    return False


def get_descricao_curta(registro):
    descricao_curta = ""

    if is_veiculo(registro):
        if registro["modelo"]:
            descricao_curta = descricao_curta + registro["modelo"]

        if registro["anoFabricacao"] and registro["anoModelo"]:
            descricao_curta = (
                descricao_curta
                + ", "
                + str(registro["anoFabricacao"])
                + "/"
                + str(registro["anoModelo"])
            )
        elif registro["anoFabricacao"]:
            descricao_curta = descricao_curta + ", " + str(registro["anoFabricacao"])
        elif registro["anoModelo"]:
            descricao_curta = descricao_curta + ", " + str(registro["anoModelo"])

        if registro["placa"]:
            descricao_curta = descricao_curta + ", PL: " + registro["placa"]

        if registro["numeroSerie"]:
            descricao_curta = descricao_curta + ", CH: " + registro["numeroSerie"]
    else:
        if registro["modelo"]:
            descricao_curta = descricao_curta + registro["modelo"]

        if registro["anoFabricacao"] and registro["anoModelo"]:
            descricao_curta = (
                descricao_curta
                + ", ANO "
                + str(registro["anoFabricacao"])
                + "/"
                + str(registro["anoModelo"])
            )
        elif registro["anoFabricacao"]:
            descricao_curta = (
                descricao_curta + ", ANO " + str(registro["anoFabricacao"])
            )
        elif registro["anoModelo"]:
            descricao_curta = descricao_curta + ", ANO " + str(registro["anoModelo"])

        if registro["numeroSerie"]:
            descricao_curta = descricao_curta + ", SÉRIE: " + registro["numeroSerie"]

    return descricao_curta.upper()


def get_descricao_detalhada(registro):
    descricao_detalhada = ""

    if is_veiculo(registro):
        if registro["modelo"]:
            descricao_detalhada = (
                descricao_detalhada + "Nome: " + registro["modelo"] + "<br>"
            )

        if registro["placa"]:
            descricao_detalhada = (
                descricao_detalhada + "Placa: " + registro["placa"] + "<br>"
            )

        if registro["numeroSerie"]:
            descricao_detalhada = (
                descricao_detalhada + "Chassi: " + registro["numeroSerie"] + "<br>"
            )

        if registro["anoFabricacao"] and registro["anoModelo"]:
            descricao_detalhada = (
                descricao_detalhada
                + "Ano Fab/Modelo: "
                + str(registro["anoFabricacao"])
                + "/"
                + str(registro["anoModelo"])
                + "<br>"
            )
        elif registro["anoFabricacao"]:
            descricao_detalhada = (
                descricao_detalhada
                + "Ano Fabricação: "
                + str(registro["anoFabricacao"])
                + "<br>"
            )
        elif registro["anoModelo"]:
            descricao_detalhada = (
                descricao_detalhada
                + "Ano Modelo: "
                + str(registro["anoModelo"])
                + "<br>"
            )

        if registro["horimetro"] and registro["horimetro"] != "0":
            descricao_detalhada = (
                descricao_detalhada
                + "Horímetro acumulado: "
                + registro["horimetro"]
                + "<br>"
            )

        if registro["kms"] and registro["kms"] != "0":
            descricao_detalhada = (
                descricao_detalhada + "Km acima de: " + registro["kms"] + "<br>"
            )

        if registro["combustivel"]:
            descricao_detalhada = (
                descricao_detalhada + "Combustível: " + registro["combustivel"] + "<br>"
            )

        if registro["motor"]:
            descricao_detalhada = (
                descricao_detalhada + "Motor: " + registro["motor"] + "<br>"
            )

        if registro["descricaoAnuncio"]:
            descricao_detalhada = (
                descricao_detalhada + "Obs: " + registro["descricaoAnuncio"] + "<br>"
            )
    else:
        if registro["modelo"]:
            descricao_detalhada = (
                descricao_detalhada + "Nome: " + registro["modelo"] + "<br>"
            )

        if registro["anoFabricacao"]:
            descricao_detalhada = (
                descricao_detalhada
                + "Ano Fabricação: "
                + str(registro["anoFabricacao"])
                + "<br>"
            )

        if registro["anoModelo"]:
            descricao_detalhada = (
                descricao_detalhada
                + "Ano Modelo: "
                + str(registro["anoModelo"])
                + "<br>"
            )

        if registro["numeroSerie"]:
            descricao_detalhada = (
                descricao_detalhada
                + "Número de Série: "
                + registro["numeroSerie"]
                + "<br>"
            )

        if registro["combustivel"]:
            descricao_detalhada = (
                descricao_detalhada + "Combustível: " + registro["combustivel"] + "<br>"
            )

        if registro["horimetro"] and registro["horimetro"] != "0":
            descricao_detalhada = (
                descricao_detalhada
                + "Horímetro acumulado: "
                + registro["horimetro"]
                + "<br>"
            )

        if registro["kms"] and registro["kms"] != "0":
            descricao_detalhada = (
                descricao_detalhada + "Km acima de: " + registro["kms"] + "<br>"
            )

        if registro["descricaoAnuncio"]:
            descricao_detalhada = (
                descricao_detalhada + "Obs: " + registro["descricaoAnuncio"] + "<br>"
            )

    return descricao_detalhada


def get_cidade(localizacao):
    try:
        city_state = localizacao[localizacao.index("(") + 1 : localizacao.rindex(")")]
        city = ma_utils.split_city_and_state(city_state)[0].strip()
    except Exception:
        try:
            city_state = localizacao.split("-")
            city = city_state[1].strip()
        except Exception:
            city = ""
    finally:
        return city


def get_estado(localizacao):
    try:
        city_state = localizacao[localizacao.index("(") + 1 : localizacao.rindex(")")]
        state = ma_utils.split_city_and_state(city_state)[1].strip()
    except Exception:
        try:
            city_state = localizacao.split("-")
            state = city_state[2].strip()
        except Exception:
            state = ""
    finally:
        return state


def get_planta(localizacao):
    try:
        plant = localizacao[0 : localizacao.index("(") - 1]
        plant = plant.replace(" -", "").strip()
    except Exception:
        try:
            plant = localizacao[0 : localizacao.index("-") - 1]
            plant = plant.replace(" -", "").strip()
        except Exception:
            plant = ""
    finally:
        return plant


def get_fotos(anexos):
    fotos = []

    for anexo in anexos:
        fotos.append(anexo)

    return fotos
