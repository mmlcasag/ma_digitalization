import re


def get_available_increments():
    # increments must be of integer, round values that make sense business-wise
    # defined by William de Andrade Ramos da Silva
    return [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]


def get_closest_value(lst, K):
    # given a list of available increments and a given value
    # determines the closest available increment for that given value
    # i.e.:
    # given list: [5, 10, 20, 50]
    # given value: 27
    # result: 20, because 27 is closest to 20, than it is to 50
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]


def generate_description_from_array(data, max_characters=225, max_items=5):
    items = []
    if len(data) > 1:
        for item in data:
            description = re.sub(r"\(OBS:[^)]*\)", "", item)
            items.append(str(description).split(" ")[0].upper())

        unique_items = list(dict.fromkeys(items))
        others_text = " E OUTROS"
        description = ", ".join(unique_items[0:max_items])

        if len(unique_items) > max_items:
            return description[0 : (max_characters - len(others_text))] + others_text

        return description[0:max_characters]
    else:
        description = re.sub(r"\(OBS:[^)]*\)", "", data[0])

        if description.startswith("."):
            return description[1:]

        return description


def get_asset_description(dataframe, description_column, sort_by_column, how_many_rows):
    # creates a local copy in order not to change values in the original dataframe
    local_dataframe = dataframe.copy(deep=True)

    # gets the total number of rows in the dataframe
    total_rows = local_dataframe.count()[description_column]

    if total_rows == 1:
        return local_dataframe[description_column][0].upper()

    # retains in the dataframe only the first word of the original description
    for index, row in local_dataframe.iterrows():
        local_dataframe.at[index, description_column] = str(
            row[description_column]
        ).split(" ")[0]

    # sorts the dataframe by the requested column and retrieves only the unique values
    assets = local_dataframe.sort_values([sort_by_column], ascending=False)[
        description_column
    ].unique()

    # stores the amount of unique rows found in the dataframe
    unique_rows = len(assets)

    # retrieves only the first n rows specified in the "how_many_rows" argument
    if unique_rows > how_many_rows:
        assets = assets[0:how_many_rows]

    # concatenates all the rows into a single description separated by commas
    asset_description = ""
    for asset in assets:
        asset_description = asset_description + asset + ", "

    # removes the trailing comma from the description
    asset_description = asset_description[0 : len(asset_description) - 2]

    # if the asset contains more products than shown, adds "and more"
    if unique_rows > how_many_rows:
        asset_description = asset_description + " e outros"

    # converts to uppercase
    asset_description = asset_description.upper()

    # limits the description to 225 characters
    asset_description = asset_description[0:225]

    return asset_description


def split_city_and_state(location):
    # workaround in case the user fills out only the state and not the state
    if len(location) == 2:
        return ["", location]

    location = location.replace(" / ", "/")
    location = location.replace("/ ", "/")
    location = location.replace(" /", "/")
    location = location.replace(" - ", "-")
    location = location.replace("- ", "-")
    location = location.replace(" -", "-")
    location = location.replace("-", "/")

    if "/" in location:
        location = location.split("/")
    elif "-" in location:
        location = location.split("-")
    else:
        location = location.split(" ")

    return location


def get_spreadsheet_columns():
    return [
        "Nº do lote",
        "Status",
        "Lote Ref. / Ativo-Frota",
        "Nome do Lote (SEMPRE MAIUSCULA)",
        "Descrição",
        "VI",
        "VMV",
        "VER",
        "Incremento",
        "Valor de Referência do Vendedor (Contábil)",
        "Comitente",
        "Município",
        "UF",
        "Assessor",
        "Pendências",
        "Restrições",
        "Débitos (Total)",
        "Unid. Métrica",
        "Fator Multiplicativo",
        "Alteração/Adicionado",
        "Descrição HTML",
    ]
