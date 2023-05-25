import common
import convert
import xml.etree.ElementTree as ET


CONST_BASE_ESTADUAL = "BaseEstadual_B"


def request_by_chassi(chassi):
    infocar_response = common.request_endpoint(CONST_BASE_ESTADUAL, None, chassi)
    return BaseEstadual(infocar_response)


def request_by_placa(placa):
    infocar_response = common.request_endpoint(CONST_BASE_ESTADUAL, placa, None)
    return BaseEstadual(infocar_response)


class BaseEstadual:
    def __init__(self, infocar_response):
        self.solicitacao = None
        self.dados_veiculo = None
        self.especificacoes = None
        self.restricoes = None
        self.intencao_financiamento = None
        self.debitos = None
        self.comunicacao_venda = None
        self.proprietario = None

        solicitacao_tag = None
        resposta_tag = None
        dados_veiculo_tag = None
        especificacoes_tag = None
        restricoes_tag = None
        restricoes_arr = []
        intencao_financiamento_tag = None
        debitos_tag = None
        comunicacao_venda_tag = None
        proprietario_tag = None

        envelope_tag = ET.fromstring(infocar_response)
        for body_tag in envelope_tag:
            for response_tag in body_tag:
                for result_tag in response_tag:
                    for info_xml_tag in result_tag:
                        for child in info_xml_tag:
                            if child.tag == "SOLICITACAO":
                                solicitacao_tag = child
                            if child.tag == "RESPOSTA":
                                resposta_tag = child

        for base_estadual_tag in resposta_tag:
            for child in base_estadual_tag:
                if child.tag == "DADOS_DO_VEICULO":
                    dados_veiculo_tag = child
                if child.tag == "INFORMACOES_TECNICAS_E_ADICIONAIS":
                    especificacoes_tag = child
                if child.tag == "RESTRICOES_E_IMPEDIMENTOS":
                    restricoes_tag = child
                    for restricao_inner in restricoes_tag:
                        if restricao_inner.tag == "RESTRICOES":
                            for restricoes in restricao_inner:
                                restricoes_arr.append(
                                    convert.to_string(restricoes.text)
                                )
                        if restricao_inner.tag == "INTENCAO_DE_FINANCIAMENTO":
                            intencao_financiamento_tag = restricao_inner
                if child.tag == "DEBITOS_ESTADUAIS":
                    debitos_tag = child
                if child.tag == "COMUNICACAO_DE_VENDAS":
                    comunicacao_venda_tag = child
                if child.tag == "PROPRIETARIO_S_":
                    proprietario_tag = child

        if solicitacao_tag is not None:
            self.solicitacao = Solicitacao(solicitacao_tag)
        if self.solicitacao.mensagem != "1":
            raise Exception(
                f"Erro na resposta da Infocar: {self.solicitacao.mensagem_extenso}"
            )
        if dados_veiculo_tag is not None:
            self.dados_veiculo = DadosVeiculo(dados_veiculo_tag)
        if especificacoes_tag is not None:
            self.especificacoes = Especificacoes(especificacoes_tag)
        if restricoes_tag is not None:
            self.restricoes = Restricoes(restricoes_tag, restricoes_arr)
        if intencao_financiamento_tag is not None:
            self.intencao_financiamento = IntencaoFinanciamento(
                intencao_financiamento_tag
            )
        if debitos_tag is not None:
            self.debitos = Debitos(debitos_tag)
        if comunicacao_venda_tag is not None:
            self.comunicacao_venda = ComunicacaoVenda(comunicacao_venda_tag)
        if proprietario_tag is not None:
            self.proprietario = Proprietario(proprietario_tag)

    def to_string(self):
        return f"{self.solicitacao.to_string()}{self.dados_veiculo.to_string()}{self.especificacoes.to_string()}{self.restricoes.to_string()}{self.intencao_financiamento.to_string()}{self.debitos.to_string()}{self.comunicacao_venda.to_string()}{self.proprietario.to_string()}"


class Solicitacao:
    def __init__(self, solicitacao_tag):
        dado = common.find_element(solicitacao_tag, "DADO")
        numero_resposta = common.find_element(solicitacao_tag, "NUMERO_RESPOSTA")
        tempo = common.find_element(solicitacao_tag, "TEMPO")
        mensagem = common.find_element(solicitacao_tag, "MENSAGEM")
        horario = common.find_element(solicitacao_tag, "HORARIO")

        mensagem_extenso = ""
        match (int(mensagem)):
            case 0:
                mensagem_extenso = "Não Possui Registro"
            case 1:
                mensagem_extenso = "Possui Registro"
            case 2:
                mensagem_extenso = "Falha de Autenticação"
            case 3:
                mensagem_extenso = "Dado/Tipo Incorreto"
            case 4:
                mensagem_extenso = "Erro na Pesquisa/Sistema Indisponível"
            case 5:
                mensagem_extenso = "Limite Diário Excedido"
            case _:
                mensagem_extenso = "Erro Desconhecido"

        self.dado = convert.to_string(dado)
        self.numero_resposta = convert.to_string(numero_resposta)
        self.tempo = convert.to_float(tempo, "US")
        self.mensagem = convert.to_string(mensagem)
        self.mensagem_extenso = convert.to_string(mensagem_extenso)
        self.horario = convert.to_datetime(horario)

    def to_string(self):
        return f"\nSOLICITACAO:\n* Dado: {self.dado}\n* Número Resposta: {self.numero_resposta}\n* Tempo: {convert.from_float_to_string(self.tempo, 4)}\n* Mensagem: {self.mensagem}\n* Mensagem Extenso: {self.mensagem_extenso}\n* Horário: {convert.from_datetime_to_string(self.horario)}"


class DadosVeiculo:
    def __init__(self, dados_veiculo_tag):
        placa = common.find_element(dados_veiculo_tag, "PLACA")
        chassi = common.find_element(dados_veiculo_tag, "CHASSI")
        municipio = common.find_element(dados_veiculo_tag, "MUNICIPIO")
        uf = common.find_element(dados_veiculo_tag, "UF")
        municipio_emplacado = common.find_element(
            dados_veiculo_tag, "ORIGEM_DE_EMPLACAMENTO"
        )
        renavam = common.find_element(dados_veiculo_tag, "RENAVAM")
        cor = common.find_element(dados_veiculo_tag, "COR")
        modelo = common.find_element(dados_veiculo_tag, "MODELO")
        ano_modelo = common.find_element(dados_veiculo_tag, "ANOMODELO")
        ano_fabricacao = common.find_element(dados_veiculo_tag, "ANOFABRICACAO")
        combustivel = common.find_element(dados_veiculo_tag, "COMBUSTIVEL")
        tipo_veiculo = common.find_element(dados_veiculo_tag, "TIPOVEICULO")

        self.placa = convert.to_string(placa)
        self.chassi = convert.to_string(chassi)
        self.municipio = convert.to_string(municipio)
        self.uf = convert.to_string(uf)
        self.municipio_emplacado = convert.to_string(municipio_emplacado[0:-4])
        self.uf_emplacado = convert.to_string(municipio_emplacado[-3:-1])
        self.renavam = convert.to_string(renavam)
        self.cor = convert.to_string(cor)
        self.modelo = convert.to_string(modelo)
        self.ano_modelo = convert.to_int(ano_modelo)
        self.ano_fabricacao = convert.to_int(ano_fabricacao)
        self.combustivel = convert.to_string(combustivel)
        self.tipo_veiculo = convert.to_string(tipo_veiculo)

    def to_string(self):
        return f"\nDADOS VEICULO:\n* Placa: {self.placa}\n* Chassi: {self.chassi}\n* Município: {self.municipio}\n* UF: {self.uf}\n* Município Emplacado: {self.municipio_emplacado}\n* UF Emplacado: {self.uf_emplacado}\n* Renavam: {self.renavam}\n* Cor: {self.cor}\n* Modelo: {self.modelo}\n* Ano Modelo: {convert.from_int_to_string(self.ano_modelo)}\n* Ano Fabricação: {convert.from_int_to_string(self.ano_fabricacao)}\n* Combustível: {self.combustivel}\n* Tipo Veículo: {self.tipo_veiculo}"


class Especificacoes:
    def __init__(self, especificacoes_tag):
        motor = common.find_element(especificacoes_tag, "MOTOR")
        cambio = common.find_element(especificacoes_tag, "CAIXADECAMBIO")
        passageiros = common.find_element(especificacoes_tag, "CAPACIDADEDEPASSAGEIROS")
        potencia = common.find_element(especificacoes_tag, "POTENCIA")
        eixos = common.find_element(especificacoes_tag, "QUANTIDADEDEEIXOS")
        carga = common.find_element(especificacoes_tag, "CAPACIDADEDECARGA")
        cmt = common.find_element(especificacoes_tag, "CMT")
        pbt = common.find_element(especificacoes_tag, "PBT")
        num_carroceria = common.find_element(especificacoes_tag, "NCARROCERIA")
        eixo_traseiro = common.find_element(
            especificacoes_tag, "NDOEIXOTRASEIRODIFERENCIAL"
        )
        terceiro_eixo = common.find_element(especificacoes_tag, "NDOTERCEIROEIXO")
        cilindradas = common.find_element(especificacoes_tag, "CILINDRADAS")
        especie = common.find_element(especificacoes_tag, "ESPECIE")
        categoria = common.find_element(especificacoes_tag, "CATEGORIA")
        carroceria = common.find_element(especificacoes_tag, "CARROCERIA")
        procedencia = common.find_element(especificacoes_tag, "PROCEDENCIA")
        data_atualizacao = common.find_element(especificacoes_tag, "DATAATUALIZACAO")
        situacao_chassi = common.find_element(especificacoes_tag, "SITUACAODOCHASSI")
        tipo_docto_faturado = common.find_element(
            especificacoes_tag, "TIPODOCUMENTOFATURADO"
        )
        num_docto_faturado = common.find_element(
            especificacoes_tag, "DOCUMENTOFATURADO"
        )
        uf_docto_faturado = common.find_element(especificacoes_tag, "UFFATURADO")

        if cilindradas == "":
            cilindradas = common.find_element(especificacoes_tag, "NUMERO_CILINDRADAS")

        self.motor = convert.to_string(motor)
        self.cambio = convert.to_string(cambio)
        self.passageiros = convert.to_int(passageiros)
        self.potencia = convert.to_int(potencia)
        self.eixos = convert.to_int(eixos)
        self.carga = convert.to_int(carga)
        self.cmt = convert.to_int(cmt)
        self.pbt = convert.to_int(pbt)
        self.num_carroceria = convert.to_string(num_carroceria)
        self.eixo_traseiro = convert.to_string(eixo_traseiro)
        self.terceiro_eixo = convert.to_string(terceiro_eixo)
        self.cilindradas = convert.to_int(cilindradas)
        self.especie = convert.to_string(especie)
        self.categoria = convert.to_string(categoria)
        self.carroceria = convert.to_string(carroceria)
        self.procedencia = convert.to_string(procedencia)
        self.data_atualizacao = convert.to_date(data_atualizacao)
        self.situacao_chassi = convert.to_string(situacao_chassi)
        self.tipo_docto_faturado = convert.to_string(tipo_docto_faturado)
        self.num_docto_faturado = convert.to_string(num_docto_faturado)
        self.uf_docto_faturado = convert.to_string(uf_docto_faturado)

    def to_string(self):
        return f"\nESPECIFICAÇÕES:\n* Motor: {self.motor}\n* Câmbio: {self.cambio}\n* Passageiros: {convert.from_int_to_string(self.passageiros)}\n* Potência: {convert.from_int_to_string(self.potencia)}\n* Eixos: {convert.from_int_to_string(self.eixos)}\n* Carga: {convert.from_int_to_string(self.carga)}\n* CMT: {convert.from_int_to_string(self.cmt)}\n* PBT: {convert.from_int_to_string(self.pbt)}\n* Número Carroceria: {self.num_carroceria}\n* Eixo Traseiro: {self.eixo_traseiro}\n* Terceiro Eixo: {self.terceiro_eixo}\n* Cilindradas: {convert.from_int_to_string(self.cilindradas)}\n* Espécie: {self.especie}\n* Categoria: {self.categoria}\n* Carroceria: {self.carroceria}\n* Procedência: {self.procedencia}\n* Data Atualização: {convert.from_date_to_string(self.data_atualizacao)}\n* Situação Chassi: {self.situacao_chassi}\n* Tipo Documento Faturado: {self.tipo_docto_faturado}\n* Número Documento Faturado: {self.num_docto_faturado}\n* UF Documento Faturado: {self.uf_docto_faturado}"


class Restricoes:
    def __init__(self, restricoes_tag, restricoes_arr):
        situacao_veiculo = common.find_element(restricoes_tag, "SITUACAO_VEICULO")
        roubo_furto = common.find_element(restricoes_tag, "ROUBO_E_FURTO")

        self.situacao_veiculo = convert.to_string(situacao_veiculo)
        self.roubo_furto = convert.to_string(roubo_furto)
        self.restricoes = restricoes_arr

    def to_string(self):
        string = f"\nRESTRIÇÕES:\n* Situação do Veículo: {self.situacao_veiculo}\n* Roubo/Furto: {self.roubo_furto}\n* Lista de Restrições:"

        if len(self.restricoes) == 0:
            string = string + f"\n  * Nenhuma restrição encontrada"
        else:
            for restricao in self.restricoes:
                string = string + f"\n  * {restricao}"

        return string


class IntencaoFinanciamento:
    def __init__(self, intencao_financiamento_tag):
        nome_financiado = common.find_element(
            intencao_financiamento_tag, "NOMEDOFINANCIADO"
        )
        docto_financiado = common.find_element(
            intencao_financiamento_tag, "DOCUMENTOFINANCIADO"
        )
        restricao_documento = common.find_element(
            intencao_financiamento_tag, "RESTRICAODOCUMENTOARRENDATARIO"
        )
        data_inclusao = common.find_element(intencao_financiamento_tag, "DATAINCLUSAO")
        cod_financeira = common.find_element(
            intencao_financiamento_tag, "CODIGOAGENTEFINANCEIRO"
        )
        nome_financeira = common.find_element(intencao_financiamento_tag, "AGENTE")
        restricao_financeira = common.find_element(
            intencao_financiamento_tag, "RESTRICAOFINANCEIRA"
        )
        num_contrato = common.find_element(intencao_financiamento_tag, "NCONTRATO")
        dat_vigencia_contrato = common.find_element(
            intencao_financiamento_tag, "DATADAVIGENCIADOCONTRATOFINANCEIRA"
        )

        self.nome_financiado = convert.to_string(nome_financiado)
        self.docto_financiado = convert.to_string(docto_financiado)
        self.restricao_documento = convert.to_string(restricao_documento)
        self.data_inclusao = convert.to_date(data_inclusao)
        self.cod_financeira = convert.to_string(cod_financeira)
        self.nome_financeira = convert.to_string(nome_financeira)
        self.restricao_financeira = convert.to_string(restricao_financeira)
        self.num_contrato = convert.to_string(num_contrato)
        self.dat_vigencia_contrato = convert.to_date(dat_vigencia_contrato)

    def to_string(self):
        return f"\nINTENÇÃO DE FINANCIAMENTO:\n* Nome do Financiado: {self.nome_financiado}\n* Documento do Financiado: {self.docto_financiado}\n* Restrição no Documento: {self.restricao_documento}\n* Data de Inclusão: {convert.from_date_to_string(self.data_inclusao)}\n* Código da Financeira: {self.cod_financeira}\n* Nome da Financeira: {self.nome_financeira}\n* Restrição na Financeira: {self.restricao_financeira}\n* Número do Contrato: {self.num_contrato}\n* Data de Vigência do Contrato: {convert.from_date_to_string(self.dat_vigencia_contrato)}"


class Debitos:
    def __init__(self, debitos_tag):
        debitos_ipva = common.find_element(debitos_tag, "DEBITOSDEIPVA")
        debitos_licenciamento = common.find_element(
            debitos_tag, "DEBITOSDELICENCIAMENTO"
        )
        debitos_dpvat = common.find_element(debitos_tag, "DEBITOSDEDPVAT")
        debitos_multas = common.find_element(debitos_tag, "DEBITOSDEMULTAS")
        multas_detran = common.find_element(debitos_tag, "MULTASDETRAN")
        multas_cetesb = common.find_element(debitos_tag, "MULTASCETESB")
        multas_municipais = common.find_element(debitos_tag, "MULTASMUNICIPAIS")
        multas_renainf = common.find_element(debitos_tag, "MULTASRENAINF")
        multas_dersa = common.find_element(debitos_tag, "MULTASDERSA")
        multas_der = common.find_element(debitos_tag, "MULTASDER")
        multas_prf = common.find_element(debitos_tag, "MULTASPOLICIARODOVIARIAFEDERAL")
        data_licenciamento = common.find_element(debitos_tag, "DATALICENCIAMENTO")
        exercicio_licenciamento = common.find_element(
            debitos_tag, "EXERCICIOLICENCIAMENTO"
        )

        self.debitos_ipva = convert.to_float(debitos_ipva, "BR")
        self.debitos_licenciamento = convert.to_float(debitos_licenciamento, "BR")
        self.debitos_dpvat = convert.to_float(debitos_dpvat, "BR")
        self.debitos_multas = convert.to_float(debitos_multas, "BR")
        self.multas_detran = convert.to_float(multas_detran, "BR")
        self.multas_cetesb = convert.to_float(multas_cetesb, "BR")
        self.multas_municipais = convert.to_float(multas_municipais, "BR")
        self.multas_renainf = convert.to_float(multas_renainf, "BR")
        self.multas_municipais = convert.to_float(multas_municipais, "BR")
        self.multas_dersa = convert.to_float(multas_dersa, "BR")
        self.multas_der = convert.to_float(multas_der, "BR")
        self.multas_prf = convert.to_float(multas_prf, "BR")
        self.data_licenciamento = convert.to_date(data_licenciamento)
        self.exercicio_licenciamento = convert.to_date(exercicio_licenciamento)

    def to_string(self):
        return f"\nDÉBITOS:\n* Débitos de IPVA: {convert.from_float_to_string(self.debitos_ipva, 2)}\n* Débitos de Licenciamento: {convert.from_float_to_string(self.debitos_licenciamento, 2)}\n* Débitos de DPVAT: {convert.from_float_to_string(self.debitos_dpvat, 2)}\n* Débitos de Multas: {convert.from_float_to_string(self.debitos_multas, 2)}\n* Multas DETRAN: {convert.from_float_to_string(self.multas_detran, 2)}\n* Multas CETESB: {convert.from_float_to_string(self.multas_cetesb, 2)}\n* Multas Municipais: {convert.from_float_to_string(self.multas_municipais, 2)}\n* Multas RENAINF: {convert.from_float_to_string(self.multas_renainf, 2)}\n* Multas DERSA: {convert.from_float_to_string(self.multas_dersa, 2)}\n* Multas DER: {convert.from_float_to_string(self.multas_der, 2)}\n* Multas PRF: {convert.from_float_to_string(self.multas_prf, 2)}\n* Data de Licenciamento: {convert.from_date_to_string(self.data_licenciamento)}\n* Exercício do Licenciamento: {convert.from_date_to_string(self.exercicio_licenciamento)}"


class ComunicacaoVenda:
    def __init__(self, comunicacao_venda_tag):
        comunicado = common.find_element(comunicacao_venda_tag, "COMUNICACAODEVENDAS")
        data_comunicado = common.find_element(comunicacao_venda_tag, "DATACOMUNICACAO")
        data_venda = common.find_element(comunicacao_venda_tag, "DATADEVENDAS")

        self.comunicado = convert.to_string(comunicado)
        self.data_comunicado = convert.to_datetime(data_comunicado)
        self.data_venda = convert.to_datetime(data_venda)

    def to_string(self):
        return f"\nCOMUNICAÇÃO DE VENDA:\n* Comunicado: {self.comunicado}\n* Data Comunicado: {convert.from_datetime_to_string(self.data_comunicado)}\n* Data Venda: {convert.from_datetime_to_string(self.data_venda)}"


class Proprietario:
    def __init__(self, proprietario_tag):
        nome = common.find_element(proprietario_tag, "PROPRIETARIO_ATUAL")
        documento = common.find_element(proprietario_tag, "DOCUMENTO")

        if nome == "":
            nome = common.find_element(proprietario_tag, "PROP_ATUAL")
        if documento == "":
            documento = common.find_element(proprietario_tag, "DOC_PROP_ATUAL")

        self.nome = convert.to_string(nome)
        self.documento = convert.to_string(documento)

    def to_string(self):
        return f"\nPROPRIETÁRIO:\n* Nome: {self.nome}\n* Documento: {self.documento}"
