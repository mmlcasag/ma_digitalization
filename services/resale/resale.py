import helpers
import requests

total_products = helpers.get_total_products_resale()

token = helpers.get_token()

product_index = 1
while product_index <= total_products:
    print(f"Buscando na Resale os dados do produto {product_index} de {total_products}")
    
    product_resale_object = helpers.get_product_resale_by_index(product_index)

    print(f"Resposta: {product_resale_object.get_id()}")

    print(f"Verificando se o produto existe na API Core")

    total_products_by_ref = helpers.get_total_products_by_ref(token, product_resale_object.get_id())
    
    product_index = product_index + 1
