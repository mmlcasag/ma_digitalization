import os
import pandas
import requests

import utils.os as os_utils
import utils.ma as ma_utils

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
                    product.get_price(),
                    "",
                    50,
                    product.get_price(),
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

        for image_remote_path in product.get_images():
            os_utils.create_folder(
                os.path.join("output", "images", product.get_reference())
            )

            image_local_path = os.path.join(
                "output",
                "images",
                product.get_reference(),
                os.path.basename(image_remote_path),
            )

            logger.info(f'Extraindo a imagem "{image_local_path}"')
            image_data = requests.get(image_remote_path).content

            with open(image_local_path, "wb") as handler:
                handler.write(image_data)

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