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
    products_sbws_array_objects = helpers.get_products_sbws_by_ref(token, product_resale_object.get_id())
    
    print("--")
    
    if len(products_sbws_array_objects) > 0:
        for product_sbws_object in products_sbws_array_objects:
            print(f"Atualizando o cadastro do produto na Superbid")
            helpers.update_product_sbws(token, product_resale_object, product_sbws_object)
            print("--")
    else:
        print(f"Inserindo um novo produto na Superbid")
        helpers.create_product_sbws(token, product_resale_object)
        print("--")
    
    product_resale_index = product_resale_index + 1
