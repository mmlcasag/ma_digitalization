import requests


def call_api_ape11(offset=0):
    try:
        print(f"Chamando a API da Apê11:")

        response = requests.get(
            url = f"https://api.santanderimoveis.com.br/ext/shi/v1/property?offset={offset}",
            headers = { 
                "x-api-key": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9wZXNzb2EiOjE2NDgyLCJlbWFpbF9sb2dpbiI6IiIsInJvbGUiOiJpbXZfbGVpbG9laXJvX3JvbGUiLCJhdWQiOiJpbW92ZWxfYmFja2VuZCJ9.4-MEyJO3RB-prIzzifqWpSposYDrEQu3rBd_JYOYiIA",
                "Accept": "*/*", 
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded", 
                "Host": "api.santanderimoveis.com.br",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            },
            timeout = 30
        )

        if response.status_code == 200:
            print("Respondeu corretamente")
        else:
            raise Exception(f"Respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao chamar a API da Apê11: {error}")

        raise


def call_api_sbws_auth():
    try:
        print("Chamando a API de Autenticação")

        response = requests.post(
            url = "https://api.s4bdigital.net/account/oauth/token",
            headers = { 
                "Content-Type": "application/x-www-form-urlencoded", 
                "Accept": "application/json", 
                "Cache-Control": "no-cache",
                "Host": "api.s4bdigital.net",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            },
            data = { 
                "grant_type": "password", 
                "username": "nws.integracao2", 
                "password": "9{!54w#18554A", 
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


def call_api_sbws_product_offer(token, dossie):
    try:
        print("Chamando a API de Product Offer")

        response = requests.get(
            url = f"https://api.s4bdigital.net/auction-lotting/productOffer/?q=partnerIntegrationId:[2,4],externalId:[{dossie}]&sort=id%20desc",
            headers = { 
                "Authorization": f"Bearer {token}",
                "Accept": "*/*", 
                "Cache-Control": "no-cache",
                "Host": "api.s4bdigital.net",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            },
            timeout = 30
        )

        if response.status_code == 200:
            print("Respondeu corretamente")
        else:
            raise Exception(f"Respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao chamar a API de Product Offer: {error}")

        raise