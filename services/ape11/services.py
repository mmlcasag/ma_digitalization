import api


def get_dossies_ape11():
    print("Buscando os dossiês na Apê11")
    
    dossies_local = []
    dossies_ape11 = 999999
    while(len(dossies_local) < dossies_ape11):
        elements = api.call_api_ape11(len(dossies_local))
        
        if dossies_ape11 == 999999:
            dossies_ape11 = elements["pagination"]["total_items"]
        
        for element in elements["imoveis"]:
            dossies_local.append(str(element["id_banco"]))

    print(f"Encontrou {dossies_ape11} dossiês na Apê11")
    
    return dossies_local


def get_token_sbws():
    print("Buscando o token de autenticação")

    response = api.call_api_sbws_auth()

    token = response["access_token"]
    
    print(f"Token de autenticação: {token}")

    return token


def get_product_offers_sbws(token, dossie):
    print(f"Buscando as ofertas do dossiê {dossie}")

    product_offers = []
    response = api.call_api_sbws_product_offer(token, dossie)
    
    if "productOffers" in response:
        for product_offer in response["productOffers"]:
            offer_id = ""
            if "offerId" in product_offer:
                offer_id = str(product_offer["offerId"])

            auction_id = ""
            if "auctionId" in product_offer:
                auction_id = str(product_offer["auctionId"])
            
            offer_status = ""
            if "statusDesc" in product_offer:
                offer_status = str(product_offer["statusDesc"])
            
            created_at = ""
            if "createdAt" in product_offer:
                created_at = str(product_offer["createdAt"])

            updated_at = ""
            if "updatedAt" in product_offer:
                updated_at = str(product_offer["updatedAt"])

            offer = {
                "externalId": dossie,
                "offerId": offer_id,
                "auctionId": auction_id,
                "offerStatus": offer_status,
                "createdAt": created_at,
                "updatedAt": updated_at
            }
            
            product_offers.append(offer)
    
    print(f"Encontrou {len(product_offers)} ofertas para o dossiê")

    return product_offers


def get_latest_product_offer(dossie, product_offers):
    print(f"Buscando a oferta mais recente do dossiê {dossie}")

    if len(product_offers) > 0:
        print(f"Considerou a oferta\n{product_offers[0]}")
        return product_offers[0]
    else:
        print(f"Não encontrou ofertas para o dossiê. Vai criar uma com dados em branco")
        return { "externalId": dossie, "offerId": "", "auctionId": "", "offerStatus": "", "createdAt": "", "updatedAt": "" }


def write_csv_file(audit_data):
    print(f"Gerando arquivo CSV")

    file = open("audit_file.csv", "w")
    
    file.write(
        "Dossiê"        + ";" + 
        "Oferta"        + ";" + 
        "Evento"        + ";" + 
        "Status"        + ";" + 
        "Inserido em"   + ";" + 
        "Atualizado em" + ";" +
        "Inseriu?"      + ";" +
        "Atualizou?"    + ";" +
        "Nem nem?"      + ";" + "\n"
    )
    for data in audit_data:
        file.write(
            data["externalId"]  + ";" +
            data["offerId"]     + ";" +
            data["auctionId"]   + ";" +
            data["offerStatus"] + ";" +
            data["createdAt"]   + ";" +
            data["updatedAt"]   + ";" +
            ""                  + ";" +
            ""                  + ";" +
            ""                  + ";" + "\n"
        )

    file.close()

    print(f"Arquivo CSV gerado com sucesso")