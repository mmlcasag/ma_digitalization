import time
import requests


def call_api_sbws_auth():
    try:
        print("Chamando a API de Autenticação")
        
        time.sleep(10)

        response = requests.post(
            url = "https://api.s4bdigital.net/account/oauth/token",
            headers = { 
                "Accept": "application/json", 
                "Content-Type": "application/x-www-form-urlencoded", 
                "User-Agent": "PostmanRuntime/7.29.0",
                "Cache-Control": "no-cache",
                "Host": "api.s4bdigital.net",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br"
            },
            data = { 
                "grant_type": "password", 
                "username": "nws.integracao", 
                "password": "F9uq^&MhBl^@", 
                "client_id": "dzqC3VodSoXukD45BQKg3NQU6-central-ativos"
            },
            timeout = 30
        )

        if response.status_code == 200:
            print("Respondeu corretamente")
        else:
            raise Exception(f"Respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao chamar a API de Autenticação: {error}")

        raise


def call_api_get_offers(token, event, limit, start):
    try:
        print(f"Chamando o GET /productOffer")
        
        time.sleep(10)

        response = requests.get(
            url = f"https://api.s4bdigital.net/auction-lotting/productOffer/?q=aid:{event}&sort=id%20desc&limit={limit}&start={start}",
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "PostmanRuntime/7.29.0",
                "Cache-Control": "no-cache",
                "Host": "api.s4bdigital.net",
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br",
                "Authorization": f"Bearer {token}"
            },
            timeout = 30
        )

        if response.status_code == 200:
            print("Respondeu corretamente")
        else:
            raise Exception(f"Respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao chamar o GET /productOffer: {error}")

        raise


def call_api_put_offer(token, payload):
    try:
        print(f"Chamando o PUT /offer")
        
        time.sleep(10)

        response = requests.put(
            url = f"https://api.s4bdigital.net/auction-lotting/offer/",
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "PostmanRuntime/7.29.0",
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "Host": "api.s4bdigital.net",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            },
            data = payload,
            timeout = 30
        )
        
        if response.status_code == 200:
            print("Respondeu corretamente")
        else:
            raise Exception(f"Respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao chamar o PUT /offer: {error}")

        raise


def call_api_put_product(token, payload):
    try:
        print(f"Chamando o PUT /product")
        
        time.sleep(10)

        response = requests.put(
            url = f"https://api.s4bdigital.net/auction-lotting/product/",
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "PostmanRuntime/7.29.0",
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "Host": "api.s4bdigital.net",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            },
            data = payload,
            timeout = 30
        )

        if response.status_code == 200:
            print("Respondeu corretamente")
        else:
            raise Exception(f"Respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao chamar o PUT /product: {error}")

        raise