import json
import requests

from classes.ProductResale import ProductResale
from classes.ProductResaleFile import ProductResaleFile
from classes.ProductResaleImage import ProductResaleImage
from classes.ProductResaleLocation import ProductResaleLocation

def call_api_resale(page, offset):
    try:
        print("Chamando a API da Resale")
        
        response = requests.get(
            url = f"https://api.repex.resale.com.br/v1/santander/property?page={page}&offset={offset}",
            headers = { "x-api-key": "41y3m4r0iev0xx28q4ssa52ogmwwiqnz" },
            timeout = 30
        )

        if response.status_code == 200:
            print("A API da Resale respondeu corretamente")
        else:
            raise Exception(f"A API da Resale respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao tentar chamar a API da Resale: {error}")

        raise


def call_api_auth_sbws():
    try:
        print("Chamando a API de Autenticação da Superbid")
        
        response = requests.post(
            url = "https://stgapi.s4bdigital.net/account/oauth/token",
            headers = { "Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "client_id": "dzqC3VodSoXukD45BQKg3NQU6-central-ativos", "Cookie": "__cfduid=dffb2772ede38fd3f510a4da93b62efe61603216549" },
            data = { "username": "rcarvalh", "password": "unicornio", "grant_type": "password", "client_id": "dzqC3VodSoXukD45BQKg3NQU6-central-ativos" },
            timeout = 30
        )

        if response.status_code == 200:
            print("A API de Autenticação da Superbid respondeu corretamente")
        else:
            raise Exception(f"A API de Autenticação da Superbid respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao tentar chamar a API de Autenticação da Superbid: {error}")

        raise


def call_api_get_product_sbws(token, product_ref, start=0, limit=1):
    try:
        print("Chamando o GET produto da Superbid")
        
        response = requests.get(
            url = f"https://stgapi.s4bdigital.net/auction-lotting/productV2/?q=productYourRef:[{product_ref}]&start={start}&limit={limit}&sort=productId%20desc",
            headers = { "Authorization": f"Bearer {token}" },
            timeout = 30
        )

        if response.status_code == 200:
            print("O GET produto da Superbid respondeu corretamente")
        else:
            raise Exception(f"O GET produto da Superbid respondeu com um código diferente do esperado: {response.status_code}")
        
        return response.json()
    except Exception as error:
        print(f"Erro ao tentar chamar o GET produto da Superbid: {error}")

        raise


def get_total_products_resale():
    print("Buscando o total de produtos na Resale")

    response = call_api_resale(1, 1)
    
    total_products = response["pagination"]["total_items"]

    print(f"Total de produtos: {total_products}")

    return int(total_products)


def to_product_resale_object(response):
    product_resale_object = ProductResale()

    #TODO: esse ID está mockado apenas para testar corretamente em STG
    #product_resale_object.set_id(response['imoveis'][0]['id'])
    product_resale_object.set_id("d52f007d-7736-7fee-402c-5f91e8d4d5c0")
    product_resale_object.set_nome(response['imoveis'][0]['nome'])
    product_resale_object.set_descricao(response['imoveis'][0]['descricao'])
    product_resale_object.set_dossie(response['imoveis'][0]['id_banco'])
    product_resale_object.set_matricula(response['imoveis'][0]['matricula'])
    product_resale_object.set_data_leilao(response['imoveis'][0]['data_leilao'])
    product_resale_object.set_rgi(response['imoveis'][0]['rgi'])
    product_resale_object.set_inscricao_prefeitura(response['imoveis'][0]['inscricao_prefeitura'])
    product_resale_object.set_consideracoes_importantes(response['imoveis'][0]['consideracoes_importantes'])
    product_resale_object.set_tipo_imovel(response['imoveis'][0]['tipo_imovel'])
    product_resale_object.set_finalidade(response['imoveis'][0]['finalidade'])
    product_resale_object.set_situacao(response['imoveis'][0]['situacao'])
    product_resale_object.set_aceita_visita(response['imoveis'][0]['aceita_visita'])
    product_resale_object.set_status_venda(response['imoveis'][0]['status_da_venda'])
    product_resale_object.set_lote(response['imoveis'][0]['lote'])
    product_resale_object.set_url(response['imoveis'][0]['url'])
    product_resale_object.set_endereco_completo(response['imoveis'][0]['endereco_completo'])
    product_resale_object.set_referencia_endereco(response['imoveis'][0]['referencia_endereco'])
    product_resale_object.set_dormitorios_empregada(response['imoveis'][0]['dormitorio_empregada'])
    product_resale_object.set_lavabos(response['imoveis'][0]['lavabos'])
    product_resale_object.set_salas(response['imoveis'][0]['salas'])
    product_resale_object.set_copas(response['imoveis'][0]['copas'])
    product_resale_object.set_vagas_garagem(response['imoveis'][0]['vagas_garagem'])
    product_resale_object.set_dormitorios(response['imoveis'][0]['dormitorios'])
    product_resale_object.set_suites(response['imoveis'][0]['suites'])
    product_resale_object.set_banheiros(response['imoveis'][0]['banheiros'])
    product_resale_object.set_cozinhas(response['imoveis'][0]['cozinhas'])
    product_resale_object.set_despensas(response['imoveis'][0]['despensas'])
    product_resale_object.set_banheiros_empregada(response['imoveis'][0]['banheiro_empregada'])
    product_resale_object.set_areas_servico(response['imoveis'][0]['areas_servico'])
    product_resale_object.set_piscinas(response['imoveis'][0]['piscina'])
    product_resale_object.set_escritorios(response['imoveis'][0]['escritorio'])
    product_resale_object.set_varandas(response['imoveis'][0]['varanda'])
    product_resale_object.set_area_total(response['imoveis'][0]['area_total'])
    product_resale_object.set_area_util(response['imoveis'][0]['area_util'])
    product_resale_object.set_area_privativa(response['imoveis'][0]['area_privativa'])
    product_resale_object.set_area_terreno(response['imoveis'][0]['area_terreno'])
    product_resale_object.set_area_comum(response['imoveis'][0]['area_comum'])
    product_resale_object.set_valor_avaliado(response['imoveis'][0]['valor_avaliado'])
    product_resale_object.set_valor_venda(response['imoveis'][0]['valor_venda'])
    product_resale_object.set_condicoes_pagamento(response['imoveis'][0]['condicoes_pagamento'])
    product_resale_object.set_pagamento_comissao(response['imoveis'][0]['pagamento_comissao'])
    product_resale_object.set_tx_comissao(response['imoveis'][0]['tx_comissao'])
    product_resale_object.set_tx_servico(response['imoveis'][0]['tx_servico'])
    product_resale_object.set_tx_condominio(response['imoveis'][0]['tx_condominio'])
    product_resale_object.set_tx_iptu(response['imoveis'][0]['tx_iptu'])
    product_resale_object.set_campanha(response['imoveis'][0]['campanha'])
    product_resale_object.set_exibir_preco(response['imoveis'][0]['price_exibir'])
    
    product_resale_object_imagens = []
    for imagem in response['imoveis'][0]['imagens']:
        product_image_resale_object = ProductResaleImage()
        
        product_image_resale_object.set_id(imagem['id'])
        product_image_resale_object.set_nome(imagem['nome'])
        product_image_resale_object.set_mimetype(imagem['mimetype'])
        product_image_resale_object.set_url(imagem['url'])
        
        product_resale_object_imagens.append(product_image_resale_object)
    product_resale_object.set_imagens(product_resale_object_imagens)

    product_resale_object_documentos = []
    for documento in response['imoveis'][0]['documentos']:
        product_file_resale_object = ProductResaleFile()
        
        product_file_resale_object.set_id(documento['id'])
        product_file_resale_object.set_nome(documento['nome'])
        product_file_resale_object.set_tipo(documento['category_id'])
        product_file_resale_object.set_url(documento['url'])

        product_resale_object_documentos.append(product_file_resale_object)
    product_resale_object.set_documentos(product_resale_object_documentos)

    product_resale_object_locais = []
    for local in response['imoveis'][0]['locais']:
        product_location_resale_object = ProductResaleLocation()
        
        product_location_resale_object.set_id(local['id'])
        product_location_resale_object.set_endereco(local['endereco'])
        product_location_resale_object.set_cidade(local['cidade'])
        product_location_resale_object.set_cidade_id(local['city_id'])
        product_location_resale_object.set_estado(local['estado'])
        product_location_resale_object.set_latitude(local['latitude'])
        product_location_resale_object.set_longitude(local['longitude'])
        product_location_resale_object.set_regiao_id(local['region_id'])

        product_resale_object_locais.append(product_location_resale_object)
    product_resale_object.set_locais(product_resale_object_locais)

    return product_resale_object


def get_product_resale_by_index(product_index):
    print(f"Buscando na Resale o produto de índice {product_index}")

    response = call_api_resale(product_index, 1)
    
    product_resale_object = to_product_resale_object(response)
    
    return product_resale_object


def get_token_sbws():
    print("Buscando o token de autenticação da Superbid")

    response = call_api_auth_sbws()

    token = response['access_token']
    
    print(f"Token de autenticação: {token}")

    return token


def filter_products_with_no_auctionId(products):
    sanitized_products = []

    for product in products:
        try:
            activeOffer = product["activeOffer"]
            auctionId = product["activeOffer"]["auctionId"]
            sanitized_products.append(product)
        except:
            pass
    
    return sanitized_products

def get_products_sbws_by_ref(token, product_ref):
    print(f'Buscando todos os produtos na Superbid com código de referência "{product_ref}"')

    page = 0
    start = 0
    limit = 25
    total = 999
    
    products = []

    while(start < total):
        response = call_api_get_product_sbws(token, product_ref, start, limit)
        
        total = response["total"]
        
        if "products" not in response:
            break
        
        for product in response["products"]:
            products.append(product)

        page = page + 1
        start = page * limit

    print(f"Total de produtos na Superbid com este código de referência: {len(products)}")
    
    if len(products) == 0:
        return []
    else:
        print(f"Filtrando produtos não associados a nenhum evento")
        valid_products = filter_products_with_no_auctionId(products)
        
        print(f"Total de produtos após aplicar o filtro: {len(valid_products)}")

        if len(products) > 0 and len(valid_products) == 0:
            print("Como não encontrou nenhum registro, consideraremos o produto mais recente como o correto")
            valid_products.append(products[0])

        print(f"Total de produtos válidos na Superbid com este código de referência: {len(valid_products)}")

        return valid_products


def update_product(product_api_core, product_resale):
    print("Em desenvolvimento")

def create_product(product_resale):
    print("Em desenvolvimento")