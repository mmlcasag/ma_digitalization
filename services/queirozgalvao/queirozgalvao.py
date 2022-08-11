import os
import shutil
import pandas
import requests
import json

if os.path.exists("output"):
    shutil.rmtree("output")

import helpers
import utils.excel as excel_utils
import utils.image as image_utils
import utils.ma as ma_utils
import utils.os as os_utils

from services.base.logger import Logger

logger = Logger.__call__().get_logger()

logger.info("Criando o dataframe")
columns = ma_utils.get_spreadsheet_columns_with_categories()
columns.append("Placa")
dataset = pandas.DataFrame(columns=columns)

logger.info("Criando a estrutura de pastas de saída")
if not os.path.exists("output"):
    os.mkdir("output")
if not os.path.exists("output/images"):
    os.mkdir("output/images")
if not os.path.exists("output/json"):
    os.mkdir("output/json")
if not os.path.exists("output/logs"):
    os.mkdir("output/logs")
if not os.path.exists("output/xlsx"):
    os.mkdir("output/xlsx")

logger.info("Lendo o conteúdo da página web")
request = requests.get(
    "https://webapp2.queirozgalvao.com/portalvendas-api/v1/equipamentos?categoria=Todos"
)

logger.info("Escrevendo o conteúdo em um arquivo JSON")
text_file = open("output/json/content.json", "w")
text_file.write(request.text)
text_file.close()

logger.info("Lendo o arquivo JSON")
json_file = open("output/json/content.json", "r")
json_data = json.load(json_file)
json_file.close()

for element in json_data:
    valor = helpers.get_valor(element["valor"])
    incremento = helpers.get_incremento(element["valor"])
    placa_uf = helpers.get_placa_com_uf(element["placa"])
    placa = helpers.get_placa(element["placa"])
    cidade = helpers.get_cidade(element["localizacao"])
    estado = helpers.get_estado(element["localizacao"])
    planta = helpers.get_planta(element["localizacao"])
    fotos = helpers.get_fotos(element["idAnexo"])
    descricao_curta = helpers.get_descricao_curta(element)
    descricao_detalhada = helpers.get_descricao_detalhada(element)

    logger.info("Informações sobre o ativo {}".format(element["metadataId"]))
    logger.info("--> Código: {}".format(element["codigo"]))
    logger.info("--> ID: {}".format(element["id"]))
    logger.info("--> Nº Solicitação: {}".format(element["numeroSolicitacao"]))
    logger.info("--> Data de Cadastro: {}".format(element["dataCadastro"]))
    logger.info("--> Status: {}".format(element["status"]))
    logger.info("--> Categoria: {}".format(element["categoria"]))
    logger.info("--> Modelo: {}".format(element["modelo"]))
    logger.info("--> Valor (Original): {}".format(element["valor"]))
    logger.info("--> Valor (Numérico): {}".format(valor))
    logger.info("--> Valor do Incremento: {}".format(incremento))
    logger.info("--> Descrição do Anúncio: {}".format(element["descricaoAnuncio"]))
    logger.info("--> Proprietário: {}".format(element["proprietario"]))
    logger.info("--> Proprietário do Ativo: {}".format(element["proprietarioAtivo"]))
    logger.info("--> Grupo de Compliance: {}".format(element["grupoCompliance"]))
    logger.info("--> Ano de Fabricação: {}".format(element["anoFabricacao"]))
    logger.info("--> Ano do Modelo: {}".format(element["anoModelo"]))
    logger.info("--> Nº da Placa (Original): {}".format(element["placa"]))
    logger.info("--> Nº da Placa (Tratada): {}".format(placa_uf))
    logger.info("--> Nº de Série: {}".format(element["numeroSerie"]))
    logger.info("--> Nº do Motor: {}".format(element["motor"]))
    logger.info("--> Combustível: {}".format(element["combustivel"]))
    logger.info("--> KMs: {}".format(element["kms"]))
    logger.info("--> Horímetro: {}".format(element["horimetro"]))
    logger.info("--> Localização: {}".format(element["localizacao"]))
    logger.info("--> Cidade: {}".format(cidade))
    logger.info("--> Estado: {}".format(estado))
    logger.info("--> Planta: {}".format(planta))
    logger.info("--> Quantidade de fotos: {}".format(len(fotos)))
    logger.info("--> Descrição Curta: {}".format(descricao_curta))
    logger.info("--> Descrição Detalhada: {}".format(descricao_detalhada))

    logger.info("Adicionando o ativo ao dataframe")
    dataset = dataset.append(
        pandas.Series(
            [
                element["codigo"],
                "novo",
                element["codigo"],
                descricao_curta,
                descricao_detalhada,
                "",
                excel_utils.convert_to_currency(valor),
                "",
                excel_utils.convert_to_currency(incremento),
                excel_utils.convert_to_currency(valor),
                element["proprietario"],
                cidade,
                estado,
                planta,
                "",
                "",
                "",
                "",
                "1",
                "",
                "",
                element["categoria"],
                element["categoria"],
                placa,
            ],
            index=dataset.columns,
        ),
        ignore_index=True,
    )

    logger.info("Extraindo as fotos do ativo")
    for foto_url in fotos:
        diretorio_ativo = os.path.join(
            os.getcwd(), "output", "images", element["codigo"]
        )
        foto_ativo = os.path.join(diretorio_ativo, os.path.basename(foto_url))

        if not os.path.exists(diretorio_ativo):
            logger.info("Criando a pasta para a extração das fotos do ativo")
            os.mkdir(diretorio_ativo)

        try:
            logger.info(f'Extraindo foto "{foto_url}"')
            image_data = requests.get(foto_url).content
            with open(foto_ativo, "wb") as handler:
                handler.write(image_data)
        except Exception as error:
            logger.error('"{}" ao tentar extrair a imagem "{}"'.format(error, foto_url))

        try:
            logger.info("Redimensionando foto")
            image_utils.resize_image(os.path.join(os.getcwd(), foto_ativo))
        except Exception as error:
            logger.error(
                '"{}" ao tentar redimensionar a imagem "{}"'.format(error, foto_ativo)
            )

        if os_utils.get_file_extension(foto_ativo).lower() != "jpg":
            try:
                logger.info("Convertendo foto para JPG")
                image_utils.convert_to_jpg(
                    os.path.join(os.getcwd(), foto_ativo),
                    os_utils.get_file_extension(foto_ativo),
                    diretorio_ativo,
                    False,
                )
            except Exception as error:
                logger.error(
                    '"{}" ao tentar converter a imagem "{}"'.format(error, foto_ativo)
                )

logger.info("Ordenando dados pelo número do lote")
dataset = dataset.sort_values("Nº do lote")

logger.info("Gerando o arquivo Excel resultante")

logger.info("Montando o objeto de geração do arquivo Excel")
excel_file = pandas.ExcelWriter(
    os.path.join("output", "xlsx", "resulting_spreadsheet.xlsx"),
    engine="xlsxwriter",
)

logger.info("Escrevendo na primeira aba da planilha o conteúdo da colunada")
dataframe = pandas.DataFrame(dataset)
dataframe.to_excel(excel_file, sheet_name="Colunada", index=False)

logger.info("Salvando e fechando o arquivo Excel resultante")
excel_file.save()

logger.info("Arquivo Excel gerado com sucesso")

logger.info("Processo finalizado com sucesso.")
done = str(input("Pressione ENTER para encerrar..."))
