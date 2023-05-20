from datetime import datetime


def to_string(original_input):
    str_input = str(original_input).strip().upper()

    if str_input is None:
        return ""
    elif str_input.upper() == "NONE":
        return ""
    elif str_input == "0":
        return ""
    elif str_input.upper() == "VALOR NAO INFORMADO":
        return ""
    elif str_input.upper() == "NAO CONSTAM INFORMACOES":
        return ""
    elif str_input.upper() == "NAO CONSTA COMUNICACAO DE VENDAS":
        return ""
    elif str_input.upper() == "NAO CONSTAM INFORMACOES NA BASE CONSULTADA":
        return ""
    else:
        return str_input


def to_int(original_input):
    str_input = to_string(original_input)

    if str_input == "":
        return 0

    return int(str_input)


def to_float(original_input, number_format):
    str_input = to_string(original_input).replace("R$ ", "").replace("R$", "")

    if number_format == "US":
        str_input = str_input.replace(",", "")

    if number_format == "BR":
        str_input = str_input.replace(".", "").replace(",", ".")

    if str_input == "":
        return 0

    return float(str_input)


def to_date(original_input):
    str_input = to_string(original_input)

    if str_input == "":
        return None

    if len(str_input) == 4:
        try:
            return datetime.strptime(f"{str_input[0:4]}", "%Y")
        except Exception:
            return None
    elif len(str_input) == 8:
        try:
            return datetime.strptime(
                f"{str_input[6:8]}/{str_input[4:6]}/{str_input[0:4]}", "%d/%m/%Y"
            )
        except Exception:
            return datetime.strptime(
                f"{str_input[0:2]}/{str_input[2:4]}/{str_input[4:8]}", "%d/%m/%Y"
            )
    elif len(str_input) == 10 and (str_input[4:5] == "-" or str_input[4:5] == "/"):
        return datetime.strptime(
            f"{str_input[8:10]}/{str_input[5:7]}/{str_input[0:4]}", "%d/%m/%Y"
        )
    elif len(str_input) == 10 and (str_input[2:3] == "-" or str_input[2:3] == "/"):
        return datetime.strptime(
            f"{str_input[0:2]}/{str_input[3:5]}/{str_input[6:10]}", "%d/%m/%Y"
        )
    else:
        raise Exception("Invalid date format: ", str_input)


def to_datetime(original_input):
    str_input = to_string(original_input)

    if str_input == "":
        return None

    if len(str_input) == 4:
        try:
            return datetime.strptime(f"{str_input[0:4]}", "%Y")
        except Exception:
            return None
    elif len(str_input) == 8:
        try:
            return datetime.strptime(
                f"{str_input[6:8]}/{str_input[4:6]}/{str_input[0:4]}", "%d/%m/%Y"
            )
        except Exception:
            return datetime.strptime(
                f"{str_input[0:2]}/{str_input[2:4]}/{str_input[4:8]}", "%d/%m/%Y"
            )
    elif len(str_input) == 10 and (str_input[4:5] == "-" or str_input[4:5] == "/"):
        return datetime.strptime(
            f"{str_input[8:10]}/{str_input[5:7]}/{str_input[0:4]}", "%d/%m/%Y"
        )
    elif len(str_input) == 10 and (str_input[2:3] == "-" or str_input[2:3] == "/"):
        return datetime.strptime(
            f"{str_input[0:2]}/{str_input[3:5]}/{str_input[6:10]}", "%d/%m/%Y"
        )
    elif len(str_input) == 19:
        return datetime.strptime(
            f"{str_input[8:10]}/{str_input[5:7]}/{str_input[0:4]} {str_input[11:19]}",
            "%d/%m/%Y %H:%M:%S",
        )
    else:
        raise Exception("Invalid datetime format: ", str_input)


def from_int_to_string(original_int):
    if original_int is None:
        return ""
    else:
        return to_string(original_int)


def from_float_to_string(original_float, decimal_places=None):
    if decimal_places is None:
        return to_string(original_float).replace(",", "").replace(".", ",")
    else:
        return (
            to_string(f"%.{decimal_places}f" % round(original_float, decimal_places))
            .replace(",", "")
            .replace(".", ",")
        )


def from_date_to_string(original_date):
    if original_date is None:
        return ""
    else:
        return to_string(original_date.strftime("%d/%m/%Y"))


def from_datetime_to_string(original_datetime):
    if original_datetime is None:
        return ""
    else:
        return to_string(original_datetime.strftime("%d/%m/%Y %H:%M:%S"))
