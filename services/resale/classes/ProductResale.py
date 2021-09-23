class ProductResale:
    
    __id = None
    __nome = None
    __descricao = None
    __dossie = None
    __matricula = None
    __data_leilao = None
    __rgi = None
    __inscricao_prefeitura = None
    __consideracoes_importantes = None
    __tipo_imovel = None
    __finalidade = None
    __situacao = None
    __aceita_visita = None
    __status_venda = None
    __lote = None
    __url = None
    __endereco_completo = None
    __referencia_endereco = None
    __dormitorios_empregada = None
    __lavabos = None
    __salas = None
    __copas = None
    __vagas_garagem = None
    __dormitorios = None
    __suites = None
    __banheiros = None
    __cozinhas = None
    __despensas = None
    __banheiros_empregada = None
    __areas_servico = None
    __piscinas = None
    __escritorios = None
    __varandas = None
    __area_total = None
    __area_util = None
    __area_privativa = None
    __area_terreno = None
    __area_comum = None
    __valor_avaliado = None
    __valor_venda = None
    __condicoes_pagamento = None
    __pagamento_comissao = None
    __tx_comissao = None
    __tx_servico = None
    __tx_condominio = None
    __tx_iptu = None
    __campanha = None
    __exibir_preco = None
    __imagens = []
    __documentos = []
    __locais = []
    
    def __init__(self):
        pass

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
    
    def get_nome(self):
        return self.__nome

    def set_nome(self, nome):
        self.__nome = nome
    
    def get_descricao(self):
        return self.__descricao

    def set_descricao(self, descricao):
        self.__descricao = descricao
    
    def get_dossie(self):
        return self.__dossie

    def set_dossie(self, dossie):
        self.__dossie = dossie
    
    def get_matricula(self):
        return self.__matricula

    def set_matricula(self, matricula):
        self.__matricula = matricula
    
    def get_data_leilao(self):
        return self.__data_leilao

    def set_data_leilao(self, data_leilao):
        self.__data_leilao = data_leilao
    
    def get_rgi(self):
        return self.__rgi

    def set_rgi(self, rgi):
        self.__rgi = rgi

    def get_inscricao_prefeitura(self):
        return self.__inscricao_prefeitura

    def set_inscricao_prefeitura(self, inscricao_prefeitura):
        self.__inscricao_prefeitura = inscricao_prefeitura
    
    def get_consideracoes_importantes(self):
        return self.__consideracoes_importantes

    def set_consideracoes_importantes(self, consideracoes_importantes):
        self.__consideracoes_importantes = consideracoes_importantes
    
    def get_tipo_imovel(self):
        return self.__tipo_imovel

    def set_tipo_imovel(self, tipo_imovel):
        self.__tipo_imovel = tipo_imovel
    
    def get_finalidade(self):
        return self.__finalidade

    def set_finalidade(self, finalidade):
        self.__finalidade = finalidade
    
    def get_situacao(self):
        return self.__situacao

    def set_situacao(self, situacao):
        self.__situacao = situacao
    
    def get_aceita_visita(self):
        return self.__aceita_visita

    def set_aceita_visita(self, aceita_visita):
        self.__aceita_visita = aceita_visita
    
    def get_status_venda(self):
        return self.__status_venda

    def set_status_venda(self, status_venda):
        self.__status_venda = status_venda
    
    def get_lote(self):
        return self.__lote

    def set_lote(self, lote):
        self.__lote = lote
    
    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url
    
    def get_endereco_completo(self):
        return self.__endereco_completo

    def set_endereco_completo(self, endereco_completo):
        self.__endereco_completo = endereco_completo
    
    def get_referencia_endereco(self):
        return self.__referencia_endereco

    def set_referencia_endereco(self, referencia_endereco):
        self.__referencia_endereco = referencia_endereco
    
    def get_dormitorios_empregada(self):
        return self.__dormitorios_empregada

    def set_dormitorios_empregada(self, dormitorios_empregada):
        self.__dormitorios_empregada = dormitorios_empregada
    
    def get_lavabos(self):
        return self.__lavabos

    def set_lavabos(self, lavabos):
        self.__lavabos = lavabos
    
    def get_salas(self):
        return self.__salas

    def set_salas(self, salas):
        self.__salas = salas
    
    def get_copas(self):
        return self.__copas
    
    def set_copas(self, copas):
        self.__copas = copas

    def get_vagas_garagem(self):
        return self.__vagas_garagem
    
    def set_vagas_garagem(self, vagas_garagem):
        self.__vagas_garagem = vagas_garagem

    def get_dormitorios(self):
        return self.__dormitorios
    
    def set_dormitorios(self, dormitorios):
        self.__dormitorios = dormitorios
    
    def get_suites(self):
        return self.__suites
    
    def set_suites(self, suites):
        self.__suites = suites
    
    def get_banheiros(self):
        return self.__banheiros
    
    def set_banheiros(self, banheiros):
        self.__banheiros = banheiros
    
    def get_cozinhas(self):
        return self.__cozinhas
    
    def set_cozinhas(self, cozinhas):
        self.__cozinhas = cozinhas
    
    def get_despensas(self):
        return self.__despensas
    
    def set_despensas(self, despensas):
        self.__despensas = despensas
    
    def get_banheiros_empregada(self):
        return self.__banheiros_empregada
    
    def set_banheiros_empregada(self, banheiros_empregada):
        self.__banheiros_empregada = banheiros_empregada
    
    def get_areas_servico(self):
        return self.__areas_servico
    
    def set_areas_servico(self, areas_servico):
        self.__areas_servico = areas_servico
    
    def get_piscinas(self):
        return self.__piscinas
    
    def set_piscinas(self, piscinas):
        self.__piscinas = piscinas
    
    def get_escritorios(self):
        return self.__escritorios
    
    def set_escritorios(self, escritorios):
        self.__escritorios = escritorios
    
    def get_varandas(self):
        return self.__varandas
    
    def set_varandas(self, varandas):
        self.__varandas = varandas
    
    def get_area_total(self):
        return self.__area_total
    
    def set_area_total(self, area_total):
        self.__area_total = area_total
    
    def get_area_util(self):
        return self.__area_util
    
    def set_area_util(self, area_util):
        self.__area_util = area_util
    
    def get_area_privativa(self):
        return self.__area_privativa
    
    def set_area_privativa(self, area_privativa):
        self.__area_privativa = area_privativa
    
    def get_area_terreno(self):
        return self.__area_terreno
    
    def set_area_terreno(self, area_terreno):
        self.__area_terreno = area_terreno
    
    def get_area_comum(self):
        return self.__area_comum
    
    def set_area_comum(self, area_comum):
        self.__area_comum = area_comum
    
    def get_valor_avaliado(self):
        return self.__valor_avaliado
    
    def set_valor_avaliado(self, valor_avaliado):
        self.__valor_avaliado = valor_avaliado
    
    def get_valor_venda(self):
        return self.__valor_venda
    
    def set_valor_venda(self, valor_venda):
        self.__valor_venda = valor_venda
    
    def get_condicoes_pagamento(self):
        return self.__condicoes_pagamento
    
    def set_condicoes_pagamento(self, condicoes_pagamento):
        self.__condicoes_pagamento = condicoes_pagamento
    
    def get_pagamento_comissao(self):
        return self.__pagamento_comissao
    
    def set_pagamento_comissao(self, pagamento_comissao):
        self.__pagamento_comissao = pagamento_comissao
    
    def get_tx_comissao(self):
        return self.__tx_comissao
    
    def set_tx_comissao(self, tx_comissao):
        self.__tx_comissao = tx_comissao
    
    def get_tx_servico(self):
        return self.__tx_servico
    
    def set_tx_servico(self, tx_servico):
        self.__tx_servico = tx_servico
    
    def get_tx_condominio(self):
        return self.__tx_condominio
    
    def set_tx_condominio(self, tx_condominio):
        self.__tx_condominio = tx_condominio
    
    def get_tx_iptu(self):
        return self.__tx_iptu
    
    def set_tx_iptu(self, tx_iptu):
        self.__tx_iptu = tx_iptu
    
    def get_campanha(self):
        return self.__campanha
    
    def set_campanha(self, campanha):
        self.__campanha = campanha
    
    def get_exibir_preco(self):
        return self.__exibir_preco
    
    def set_exibir_preco(self, exibir_preco):
        self.__exibir_preco = exibir_preco
    
    def get_imagens(self):
        return self.__imagens
    
    def set_imagens(self, imagens):
        self.__imagens = imagens
    
    def get_documentos(self):
        return self.__documentos
    
    def set_documentos(self, documentos):
        self.__documentos = documentos
    
    def get_locais(self):
        return self.__locais
    
    def set_locais(self, locais):
        self.__locais = locais
    
    def to_string(self):
        return f"[Produto Resale] - ID: {self.get_id()} - Nome: {self.get_nome()} - Descrição: {self.get_descricao()} - Dossiê: {self.get_dossie()} - Matrícula: {self.get_matricula()} - Data Leilão: {self.get_data_leilao()} - RGI: {self.get_rgi()} - Inscrição Prefeitura: {self.get_inscricao_prefeitura()} - Considerações Importantes: {self.get_consideracoes_importantes()} - Tipo Imóvel: {self.get_tipo_imovel()} - Finalidade: {self.get_finalidade()} - Situação: {self.get_situacao()} - Aceita Visita: {self.get_aceita_visita()} - Status Venda: {self.get_status_venda()} - Lote: {self.get_lote()} - URL: {self.get_url()} - Endereço Completo: {self.get_endereco_completo()} - Referência Endereço: {self.get_referencia_endereco()} - Dormitórios Empregada: {self.get_dormitorios_empregada()} - Lavabos: {self.get_lavabos()} - Salas: {self.get_salas()} - Copas: {self.get_copas()} - Vagas Garagem: {self.get_vagas_garagem()} - Dormitórios: {self.get_dormitorios()} - Suítes: {self.get_suites()} - Banheiros: {self.get_banheiros()} - Cozinhas: {self.get_cozinhas()} - Despensas: {self.get_despensas()} - Banheiros Empregada: {self.get_banheiros_empregada()} - Áreas Serviço: {self.get_areas_servico()} - Piscinas: {self.get_piscinas()} - Escritórios: {self.get_escritorios()} - Varandas: {self.get_varandas()} - Área Total: {self.get_area_total()} - Área Útil: {self.get_area_util()} - Área Privativa: {self.get_area_privativa()} - Área Terreno: {self.get_area_terreno()} - Área Comum: {self.get_area_comum()} - Valor Avaliado: {self.get_valor_avaliado()} - Valor Venda: {self.get_valor_venda()} - Condições Pagamento: {self.get_condicoes_pagamento()} - Pagamento Comissão: {self.get_pagamento_comissao()} - Taxa Comissão: {self.get_tx_comissao()} - Taxa Serviço: {self.get_tx_servico()} - Taxa Condomínio: {self.get_tx_condominio()} - Taxa IPTU: {self.get_tx_iptu()} - Campanha: {self.get_campanha()} - Exibir Preço: {self.get_exibir_preco()} - Imagens: {len(self.get_imagens())} - Documentos: {len(self.get_documentos())} - Locais: {len(self.get_locais())}"