import re
import json
import requests
import utils.os as os_utils


from services.base.logger import Logger

logger = Logger.__call__().get_logger()


input_folder = "input"
config_folder = "config"
output_folder = "output"


def get_config_images():
    allowed_extensions = ["jpg", "jpeg", "png"]
    return os_utils.get_files_list(config_folder, allowed_extensions)


def get_config_files():
    allowed_extensions = ["txt"]
    return os_utils.get_files_list(config_folder, allowed_extensions)


def get_input_images():
    allowed_extensions = ["jpg", "jpeg", "png"]

    files_list = os_utils.get_files_list(input_folder, allowed_extensions)

    if len(files_list) == 0:
        logger.warning("Nenhuma imagem foi encontrada no diretório de entrada")

    return files_list


def process_image(input_image, background_image, background_color):
    URL = "https://api.slazzer.com/v2.0/remove_image_background"
    API_KEY = "232e215149364ddfb37a173222a1965c"
    PATH = f"{input_folder}/{input_image}"
    BG = f"{config_folder}/{background_image}"
    headers = {"API-KEY": API_KEY}

    files = ""
    data = ""
    if background_image != "":
        logger.info(
            f'Como carregamos a imagem de fundo "{background_image}", aplicaremos esse fundo na imagem'
        )
        files = {"source_image_file": open(PATH, "rb"), "bg_image_file": open(BG, "rb")}
        data = {"format": "jpg", "scale": "70%", "position": "center"}
    elif background_color != "":
        logger.info(
            f'Como carregamos a cor de fundo "{background_color}", aplicaremos essa cor de fundo na imagem'
        )
        files = {"source_image_file": open(PATH, "rb")}
        data = {
            "format": "jpg",
            "scale": "70%",
            "position": "center",
            "bg_color_code": background_color,
        }
    else:
        logger.info(
            "Como não carregamos nem imagem nem cor de fundo, apenas removeremos o fundo da imagem"
        )
        files = {"source_image_file": open(PATH, "rb")}
        data = {"format": "jpg", "scale": "70%", "position": "center"}

    logger.info("Processando a imagem")
    response = requests.post(URL, headers=headers, files=files, data=data)

    if str(response.status_code) != "200":
        message = json.loads(response.content.decode("ascii"))
        raise Exception(
            f'HTTP Status: {response.status_code} - Error Code: {message["error_code"]} - Message: {message["error"]}'
        )

    return response.content


def save_output_image(output_image_name, output_image):
    file_name = os_utils.get_file_name(output_image_name)
    file_extension = "jpg"

    with open(f"{output_folder}/{file_name}.{file_extension}", "wb") as img:
        img.write(output_image)


def get_background_image():
    background_image = ""
    background_image_count = 0
    for config_background_image in get_config_images():
        logger.info(
            f'Encontrada imagem de fundo "{config_background_image}" no diretório de configuração'
        )
        background_image = config_background_image
        background_image_count = background_image_count + 1

    if background_image_count == 0:
        logger.warning("Nenhuma imagem de fundo foi encontrada")

    if background_image_count > 1:
        logger.warning("Mais do que uma imagem de fundo foi encontrada")
        logger.warning("A aplicação irá considerar a última válida encontrada")

    return background_image


def get_background_color():
    background_color = ""
    background_color_count = 0
    for config_background_color in get_config_files():
        logger.debug(
            f'Encontrado arquivo de configuração "{config_background_color}" no diretório de configuração'
        )

        logger.debug("Abrindo o arquivo de configuração")
        file_content = open(f"{config_folder}/{config_background_color}", "r")
        html_color = str(file_content.read()).strip()
        logger.debug(f'Conteúdo do arquivo de configuração: "{html_color}"')

        if re.search(r"^#[0-9a-fA-F]{6}$", html_color):
            logger.debug("Esse é um código válido de cor de fundo")
            logger.info(
                f'Encontrada cor de fundo "{html_color}" no diretório de configuração'
            )
            background_color = html_color
            background_color_count = background_color_count + 1
        else:
            logger.warning("Esse não é um valor válido de cor de fundo")
            logger.warning("Apenas códigos hexadecimais são permitidos")

    if background_color_count == 0:
        logger.warning("Nenhuma cor de fundo foi encontrada")

    if background_color_count > 1:
        logger.warning("Mais do que uma cor de fundo foi encontrada")
        logger.warning("A aplicação irá considerar a última válida encontrada")

    return background_color


def init_application():
    os_utils.create_folder(input_folder)
    os_utils.create_folder(output_folder)


def run_application():
    logger.info("Buscando imagem de fundo")
    background_image = get_background_image()

    logger.info("Buscando cor de fundo")
    background_color = get_background_color()

    for input_image in get_input_images():
        try:
            logger.info(f'Encontrada a imagem "{input_image}" no diretório de entrada')
            output_image = process_image(
                input_image, background_image, background_color
            )
            logger.info("Imagem processada com sucesso")

            logger.info("Salvando a imagem no diretório de saída")
            save_output_image(input_image, output_image)
            logger.info("Imagem salva com sucesso")
        except Exception as error:
            logger.warning("Ocorreu um erro ao tentar processar a imagem")
            logger.warning(f'Mais informações: "{error}"')

    logger.info("Processo finalizado com sucesso.")
    str(input("Pressione ENTER para encerrar..."))


if __name__ == "__main__":
    init_application()
    run_application()
