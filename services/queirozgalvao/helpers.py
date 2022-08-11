import utils.ma as ma_utils


def is_veiculo(registro):
    categorias_especiais = ["Veículos", "Caminhões", "Ônibus", "Guindastes"]

    if registro["categoria"] in categorias_especiais:
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
            descricao_curta = (
                descricao_curta + ", PL.: " + get_placa_com_uf(registro["placa"])
            )

        if registro["numeroSerie"]:
            if registro["numeroSerie"] == "*":
                descricao_curta = descricao_curta + ", CH.: NÃO IDENTIFICADO"
            else:
                descricao_curta = descricao_curta + ", CH.: " + registro["numeroSerie"]
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
            if registro["numeroSerie"] == "*":
                descricao_curta = descricao_curta + ", SÉRIE: NÃO IDENTIFICADO"
            else:
                descricao_curta = (
                    descricao_curta + ", SÉRIE: " + registro["numeroSerie"]
                )

    descricao_curta = descricao_curta.upper()

    descricao_curta = descricao_curta.replace("AUTOMOVEL ", "")
    descricao_curta = descricao_curta.replace("AUTOMÓVEL ", "")
    descricao_curta = descricao_curta.replace("VEICULO UTILITARIO ", "")
    descricao_curta = descricao_curta.replace("VEÍCULO UTILITÁRIO ", "")
    descricao_curta = descricao_curta.replace("LOTE ", "")
    descricao_curta = descricao_curta.replace("MBB ", "MERCEDES-BENZ ")
    descricao_curta = descricao_curta.replace("VW ", "VOLKSWAGEN ")
    descricao_curta = descricao_curta.replace("VOLKS ", "VOLKSWAGEN ")

    if descricao_curta[0:1] == "=":
        descricao_curta = descricao_curta[1:]

    return descricao_curta.strip()


def get_descricao_detalhada(registro):
    descricao_detalhada = ""

    if is_veiculo(registro):
        if registro["modelo"]:
            descricao_detalhada = descricao_detalhada + registro["modelo"] + "<br>"

        if registro["placa"]:
            descricao_detalhada = (
                descricao_detalhada
                + "Placa: "
                + get_placa_com_uf(registro["placa"])
                + "<br>"
            )

        if registro["numeroSerie"]:
            if registro["numeroSerie"] == "*":
                descricao_detalhada = (
                    descricao_detalhada + "Chassi: NÃO IDENTIFICADO<br>"
                )
            else:
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
            descricao_detalhada = descricao_detalhada + registro["modelo"] + "<br>"

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
            if registro["numeroSerie"] == "*":
                descricao_detalhada = (
                    descricao_detalhada + "Número de Série: NÃO IDENTIFICADO<br>"
                )
            else:
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

    descricao_detalhada = descricao_detalhada.replace("AUTOMOVEL ", "")
    descricao_detalhada = descricao_detalhada.replace("AUTOMÓVEL ", "")
    descricao_detalhada = descricao_detalhada.replace("VEICULO UTILITARIO ", "")
    descricao_detalhada = descricao_detalhada.replace("VEÍCULO UTILITÁRIO ", "")
    descricao_detalhada = descricao_detalhada.replace("LOTE ", "")
    descricao_detalhada = descricao_detalhada.replace("MBB ", "MERCEDES-BENZ ")
    descricao_detalhada = descricao_detalhada.replace("VW ", "VOLKSWAGEN ")
    descricao_detalhada = descricao_detalhada.replace("VOLKS ", "VOLKSWAGEN ")

    if descricao_detalhada[0:1] == "=":
        descricao_detalhada = descricao_detalhada[1:]

    return descricao_detalhada.strip()


def get_placa_com_uf(placa):
    if placa:
        if len(placa) == 8:
            letras = placa[0:3]
            numeros = placa[4:8]
            return letras + numeros
        elif len(placa) == 11:
            letras = placa[0:3]
            numeros = placa[4:8]
            estado = placa[9:11]
            return letras + numeros + " (" + estado + ")"
        else:
            return ""
    return ""


def get_placa(placa):
    if placa:
        if len(placa) == 8:
            letras = placa[0:3]
            numeros = placa[4:8]
            return letras + numeros
        elif len(placa) == 11:
            letras = placa[0:3]
            numeros = placa[4:8]
            return letras + numeros
        else:
            return ""
    return ""


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


def get_valor(valor):
    str_valor = valor.replace(".", "")
    str_valor = str_valor.replace(",", "")

    return int(str_valor) / 100


def get_incremento(valor):
    int_valor = get_valor(valor)

    if int_valor <= 100:
        return 25
    elif int_valor > 100 and int_valor <= 500:
        return 50
    elif int_valor > 500 and int_valor <= 1600:
        return 100
    elif int_valor > 1600 and int_valor <= 3000:
        return 200
    elif int_valor > 3000 and int_valor <= 8000:
        return 250
    elif int_valor > 8000 and int_valor <= 20000:
        return 500
    elif int_valor > 20000 and int_valor <= 50000:
        return 1000
    elif int_valor > 50000 and int_valor <= 100000:
        return 2000
    elif int_valor > 100000 and int_valor <= 200000:
        return 2500
    elif int_valor > 200000 and int_valor <= 300000:
        return 5000
    elif int_valor > 300000:
        return 10000
