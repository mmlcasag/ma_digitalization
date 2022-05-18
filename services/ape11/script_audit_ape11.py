import services


if __name__ == "__main__":
    audit_data = []
    
    dossies = services.get_dossies_ape11()
    token = services.get_token_sbws()
    for dossie in dossies:
        product_offers = services.get_product_offers_sbws(token, dossie)
        product_offer = services.get_latest_product_offer(dossie, product_offers)
        
        audit_data.append(product_offer)
    
    services.write_csv_file(audit_data)