import helpers
import requests

total_products_resale = helpers.get_total_products_resale()
print("--")

token = helpers.get_token()
print("--")

product_resale_index = 1
while product_resale_index <= total_products_resale:
    print(f"Buscando na Resale os dados do produto {product_resale_index} de {total_products}")
    product_resale_object = helpers.get_product_resale_by_index(product_resale_index)
    
    print("--")

    print(f"Verificando se o produto existe na API Core")
    products_by_ref = helpers.get_products_by_ref(token, product_resale_object.get_id())
    
    print("--")
    
    if len(products_by_ref) > 0:
        for product in products_by_ref:
            print(f"Atualizando o cadastro do produto na API Core")
            helpers.update_product(product, product_resale_object)
            print("--")
    else:
        print(f"Inserindo um novo produto na API Core")
        helpers.create_product(product_resale_object)
        print("--")
    
    product_resale_index = product_resale_index + 1
