import helpers

token = helpers.get_token_sbws()
print("--")

total_products_resale = helpers.get_total_products_resale()
print("--")

product_resale_index = 1
while product_resale_index <= total_products_resale:
    print(f"Buscando na Resale os dados do produto {product_resale_index} de {total_products_resale}")
    product_resale_object = helpers.get_product_resale_by_index(product_resale_index)
    
    print("--")

    print(f"Verificando se o produto existe na Superbid")
    products_by_ref = helpers.get_products_sbws_by_ref(token, product_resale_object.get_id())
    
    print("--")
    
    if len(products_by_ref) > 0:
        for product in products_by_ref:
            print(f"Atualizando o cadastro do produto na Superbid")
            helpers.update_product(product, product_resale_object)
            print("--")
    else:
        print(f"Inserindo um novo produto na Superbid")
        helpers.create_product(product_resale_object)
        print("--")
    
    product_resale_index = product_resale_index + 1
