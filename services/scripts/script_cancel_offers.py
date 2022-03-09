import services


if __name__ == "__main__":
    token = services.get_token_sbws()    
    event = 102147
    total = services.get_event_offers_total(token, event)
    limit = 50
    start = 0
    while (total >= limit + start):
        offers = services.get_event_offers(token, event, limit, start)
        services.cancel_offers(token, offers)
        services.cancel_products(token, offers)
        start = start + limit