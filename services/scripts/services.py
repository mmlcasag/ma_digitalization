import api


def get_token_sbws():
    print("Buscando o token de autenticação")

    response = api.call_api_sbws_auth()

    token = response["access_token"]
    
    print(f"Token de autenticação: {token}")

    return token


def get_event_offers_total(token, event):
    print(f"Buscando o total de ofertas do evento {event}")

    response = api.call_api_get_offers(token, event, 25, 0)
    
    if response:
        total = response["total"]
        print(f"Total de ofertas do evento: {total}")
    
    return total


def get_event_offers(token, event, limit, start):
    print(f"Buscando os registros {start}-{start + limit} do evento {event}")

    response = api.call_api_get_offers(token, event, limit, start)
    
    offers = []

    if response:
        for offer in response["productOffers"]:
            offer_id = offer["offerId"]
            product_id = offer["productId"]

            print(f"Oferta: {offer_id} / Produto: {product_id}")

            offers.append({ "offerId": offer_id, "productId": product_id })
    
    return offers


def sanitize_offers(elements):
    sanitized_offers = '['
    
    if len(elements) > 0:
        aux = 0
        for element in elements:
            aux = aux + 1
            if aux == 1:
                sanitized_offers = sanitized_offers + '{ "offerId": ' + str(element["offerId"]) + ', "statusId": 2 }'
            else:
                sanitized_offers = sanitized_offers + ', { "offerId": ' + str(element["offerId"]) + ', "statusId": 2 }'
    
    sanitized_offers = sanitized_offers + ']'
    
    return sanitized_offers
    

def cancel_offers(token, offers):
    payload = sanitize_offers(offers)
    
    print(f"Cancelando as ofertas {payload}")

    api.call_api_put_offer(token, payload)

    print("Ofertas canceladas com sucesso")


def sanitize_products(elements):
    sanitized_products = '['
    
    if len(elements) > 0:
        aux = 0
        for element in elements:
            aux = aux + 1
            if aux == 1:
                sanitized_products = sanitized_products + '{ "productId": ' + str(element["productId"]) + ', "statusId": 2 }'
            else:
                sanitized_products = sanitized_products + ', { "productId": ' + str(element["productId"]) + ', "statusId": 2 }'
    
    sanitized_products = sanitized_products + ']'
    
    return sanitized_products
    

def cancel_products(token, products):
    payload = sanitize_products(products)

    print(f"Cancelando os produtos {payload}")

    api.call_api_put_product(token, payload)

    print("Produtos cancelados com sucesso")
