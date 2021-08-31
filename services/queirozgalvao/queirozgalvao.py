import os
import pandas
import requests

import utils.os as os_utils
import utils.ma as ma_utils
import utils.excel as excel_utils
import utils.image as image_utils

from classes.Crawler import Crawler
from classes.Category import Category
from classes.Product import Product
from services.base.logger import Logger

logger = Logger.__call__().get_logger()

os_utils.create_folder("output")
os_utils.create_folder("output", "xlsx")
os_utils.create_folder("output", "images")

categories = []

main_crawler = Crawler("https://vendas.queirozgalvao.com/")

for category_html in main_crawler.get_parent_category():
    category = Category(category_html)
    logger.info(category.to_string())

    category_crawler = Crawler(category.get_url())

    while category_crawler.get_page():
        logger.info(f"Página: {category_crawler.get_page_number()}")

        for product_url in category_crawler.get_products_url():
            product_crawler = Crawler(product_url)
            product_html = product_crawler.get_page()

            product = Product(product_html)
            logger.info(product.to_string())

            category.add_product(product)

        category_crawler.get_next_page()

    logger.info(f"Total de Produtos na Categoria: {category.get_total_products()}")

    categories.append(category)

dataset = pandas.DataFrame(columns=ma_utils.get_spreadsheet_columns_with_categories())

for category in categories:
    for product in category.get_products():
        dataset = dataset.append(
            pandas.Series(
                [
                    product.get_reference(),
                    "novo",
                    product.get_reference(),
                    product.get_short_description(),
                    product.get_full_description(),
                    "",
                    excel_utils.convert_to_currency(product.get_price()),
                    "",
                    excel_utils.convert_to_currency(50),
                    excel_utils.convert_to_currency(product.get_price()),
                    product.get_owner(),
                    product.get_city(),
                    product.get_state(),
                    product.get_plant(),
                    "",
                    "",
                    "",
                    "",
                    "1",
                    "",
                    "",
                    product.get_category(),
                    product.get_subcategory(),
                ],
                index=dataset.columns,
            ),
            ignore_index=True,
        )

        for remote_image_url in product.get_images():
            relative_output_path = os.path.join(
                "output", "images", product.get_reference()
            )
            relative_image_path = os.path.join(
                relative_output_path, os.path.basename(remote_image_url)
            )

            os_utils.create_folder(relative_output_path)

            logger.info(f'Extraindo a imagem para "{relative_image_path}"')
            image_data = requests.get(remote_image_url).content
            with open(relative_image_path, "wb") as handler:
                handler.write(image_data)

            try:
                logger.info('Redimensionando a imagem "{}"'.format(relative_image_path))
                image_utils.resize_image(os.path.join(os.getcwd(), relative_image_path))
            except Exception as error:
                logger.error(
                    '"{}" ao tentar redimensionar a imagem "{}"'.format(
                        error, relative_image_path
                    )
                )

            if os_utils.get_file_extension(relative_image_path).lower() != "jpg":
                try:
                    logger.info(
                        'Convertendo a imagem "{}" para JPG'.format(relative_image_path)
                    )
                    image_utils.convert_to_jpg(
                        os.path.join(os.getcwd(), relative_image_path),
                        os_utils.get_file_extension(relative_image_path),
                        relative_output_path,
                        False,
                    )
                except Exception as error:
                    logger.error(
                        '"{}" ao tentar converter a imagem "{}"'.format(
                            error, relative_image_path
                        )
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
